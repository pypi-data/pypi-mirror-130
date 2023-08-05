/*
 * fileparser.c
 *
 *  Created on: Feb 3, 2017
 *      Author: skauffma
 *
 *    nfer - a system for inferring abstractions of event streams
 *   Copyright (C) 2017  Sean Kauffman
 *
 *   This file is part of nfer.
 *   nfer is free software: you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation, either version 3 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#include <stdio.h>

#include "types.h"
#include "file.h"
#include "dict.h"
#include "pool.h"
#include "map.h"
#include "strings.h"
#include "log.h"

#ifndef NO_STDLIB
#ifndef NO_DYNAMIC_MEMORY
/**
 * Pool needs to be initialized before passing to this function.
 * This function won't currently work without dynamic allocation.
 */
bool read_event_file(char *filename, pool *p, dictionary *name_dict, dictionary *key_dict, dictionary *val_dict, bool filter) {
    bool success = false;
    FILE* file;
    char line[MAX_LINE_LENGTH];
    int line_number = 0;

    // try to open the file
    file = fopen(filename, "r");

    // if we failed to open the file, log an error and return failure
    if (file == NULL) {
        filter_log_msg(LOG_LEVEL_ERROR, "Error reading event file\n");
        return false;
    }

    // read as many line as you can
    while (fgets(line, MAX_LINE_LENGTH, file)) {
        line_number++;

        // we're ignoring success or failure here, because we don't need to do any cleanup if it fails
        read_event_from_csv(p, line, line_number, name_dict, key_dict, val_dict, filter);
    }

    if (feof(file)) {
        // hit the end of the file
        filter_log_msg(LOG_LEVEL_DEBUG, "EOF reached afer %d lines\n", line_number);
        success = true;
    } else {
        // found a line that does match this pattern
        // log a warning and move on
        filter_log_msg(LOG_LEVEL_WARN, "Line %d didn't match expected pattern, aborting.\n", line);
        success = false;
    }

    // make sure to close the file
    fclose(file);

    return success;
}
#endif

static void create_interval(pool *p, label name, timestamp ts, unsigned int map_length, map_key *keys, map_value *values) {
    unsigned int i;
    interval *result;

    // allocate the interval space in the pool
    result = allocate_interval(p);

    // if there's space, use it
    if (result != NULL) {
        result->name = name;
        result->start = ts;
        result->end = ts;

        // add the map key/value pairs to the interval map
        for (i = 0; i < map_length; i++) {
            // we filter out keys where the key is WORD_NOT_FOUND
            if (keys[i] != WORD_NOT_FOUND) {
                map_set(&result->map, keys[i], &values[i]);
            }
        }
    }
}

// state 0 is whitespace at the beginning of the line
// state 1 is during the event name and any trailing whitespace
// state 2 is the delimiter of the end of the name field, which can be , or |, plus whitespace
// state 3 is the event timestamp
// state 4 is the end of the line, including newlines
// state 5 is the beginning of a map key including whitespace
// state 6 the contents of a map key
// state 7 is the beginning of a map value
// state 8 is the contents of a map value
typedef enum {
    ROWBEGIN,
    EVENTNAME,
    NAMEDELIMETER,
    TIMESTAMP,
    EOL,
    MAPKEY_BEGIN,
    MAPKEY_CONTENTS,
    MAPVALUE_BEGIN,
    MAPVALUE_CONTENTS
} csv_row_states;

typedef enum {
    UNKNOWN,
    INT,
    ZERO,
    REAL,
    NEG,
    STRING,
    BOOLT,
    BOOLTR,
    BOOLTRU,
    BOOLTRUE,
    BOOLF,
    BOOLFA,
    BOOLFAL,
    BOOLFALS,
    BOOLFALSE,
    TRAILING_WS
} map_value_dfa_states;

bool read_event_from_csv(pool *p, char *line, int line_number, dictionary *name_dict, dictionary *key_dict, dictionary *val_dict, bool filter) {
    char *name, *ts_str = line, *key_str, *val_str;
    timestamp ts;

    char c;
    int i, last_non_ws, map_keys, map_values;
    csv_row_states state;
    map_value_dfa_states mvstate;
    bool mvbool, mverror;
    word_id name_id, key_id, value_id;
    map_key keys[MAX_MAP_PAIRS];
    map_value values[MAX_MAP_PAIRS];
    value_type mvtype;

    // set up the defaults for all the variables we will use to keep track of state
    state = ROWBEGIN;
    mvstate = UNKNOWN;
    map_keys = 0;
    map_values = 0;
    last_non_ws = 0;
    name = NULL;
    ts = 0;
    key_str = NULL;
    val_str = NULL;
    mvtype = null_type;
    mvbool = false;

    for (i = 0; i < MAX_LINE_LENGTH; i++) {
        c = line[i];
        if (c == '\0') {
            if (state == TIMESTAMP || state == MAPVALUE_CONTENTS) {
                // fake the newline so the last event in a file is parsed even if there's no newline
                c = '\n';
            } else {
                if (state != 4) {
                    filter_log_msg(LOG_LEVEL_WARN, "Unexpected NULL character encountered on Line %d column %d\n", line_number, i);
                }
                return false;
            }
        }
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "Line %d row %d state %d char %c last_non_ws %d mvtype %d\n", line_number, i, state, c, last_non_ws, mvtype);

        // DFA for scanning events
        // there is a second DFA for determining map value type
        if (state == ROWBEGIN && !IS_WHITESPACE(c)) {
            state = EVENTNAME;
            name = &line[i];
            last_non_ws = i;
        } else if (state == EVENTNAME && !IS_WHITESPACE(c) && !IS_DELIMETER(c)) {
            // we want to keep track of the last non-whitespace char position
            last_non_ws = i;
        } else if (state == EVENTNAME && IS_DELIMETER(c)) {
            state = NAMEDELIMETER;
            line[last_non_ws + 1] = 0;
        } else if (state == NAMEDELIMETER && !IS_WHITESPACE(c)) {
            state = TIMESTAMP;
            ts_str = &line[i];
        } else if (state == TIMESTAMP && IS_NEWLINE(c)) {
            line[i] = 0;
            // there is no error handling in our function, so we just get a number of some sort
            ts = string_to_u64(ts_str, &line[i] - ts_str);

            // if we're filtering, check the label to see if it is in the dictionary
            if (filter) {
                name_id = find_word(name_dict, name);
                // don't add the interval if the name isn't found
                if (name_id == WORD_NOT_FOUND) {
                    return false;
                }
            } else {
                // otherwise add the label to the dictionary
                name_id = add_word(name_dict, name);
            }
            // create an event without a map
            create_interval(p, name_id, ts, 0, NULL, NULL);
            return true;
        } else if (state == TIMESTAMP && IS_DELIMETER(c)) {
            // there is a map
            state = MAPKEY_BEGIN;
            line[i] = 0;
            // again, we don't test for errors
            ts = string_to_u64(ts_str, &line[i] - ts_str);

        } else if (state == MAPKEY_BEGIN && !IS_WHITESPACE(c)) {
            // first char of a map key
            state = MAPKEY_CONTENTS;
            key_str = &line[i];
            last_non_ws = i;
        } else if (state == MAPKEY_CONTENTS && !IS_WHITESPACE(c) && !IS_DELIMETER(c) && c != ';') {
            // we want to keep track of the last non-whitespace char position
            last_non_ws = i;
        } else if (state == MAPKEY_CONTENTS && c == ';') {
            // delimiters between map keys
            state = MAPKEY_BEGIN;
            line[last_non_ws + 1] = 0;
            // if filtering, look up the key and just add whatever it is: we'll skip it later (or not)
            // we need to do this so the indexes match up with the map values
            if (filter) {
                key_id = find_word(key_dict, key_str);
            } else {
                key_id = add_word(key_dict, key_str);
            }
            keys[map_keys] = key_id;
            map_keys++;
        } else if (state == MAPKEY_CONTENTS && IS_DELIMETER(c)) {
            // end of map keys, beginning of map values
            state = MAPVALUE_BEGIN;
            line[last_non_ws + 1] = 0;
            // if filtering, look up the key and just add whatever it is: we'll skip it later (or not)
            // we need to do this so the indexes match up with the map values
            if (filter) {
                key_id = find_word(key_dict, key_str);
            } else {
                key_id = add_word(key_dict, key_str);
            }
            keys[map_keys] = key_id;
            map_keys++;
        } else if (state == MAPVALUE_BEGIN && !IS_DELIMETER(c) && !IS_WHITESPACE(c)) {
            // first char of a map value
            state = MAPVALUE_CONTENTS;
            // initialize map value DFA
            mvstate = 0;
            mvtype = null_type;
            val_str = &line[i];
            last_non_ws = i;
        } else if (state == MAPVALUE_CONTENTS && !IS_WHITESPACE(c) && !IS_NEWLINE(c) && c != ';') {
            // we want to keep track of the last non-whitespace char position
            last_non_ws = i;
        } else if (state == MAPVALUE_CONTENTS && c == ';') {
            // delimiters between map keys
            state = MAPVALUE_BEGIN;
            line[last_non_ws + 1] = 0;
            // set the type
            values[map_values].type = mvtype;
            // set the value
            switch(mvtype) {
            case null_type:
                values[map_values].value.boolean = false;
                break;
            case boolean_type:
                values[map_values].value.boolean = mvbool;
                break;
            case integer_type:
                // we don't check for errors in the int parsing function
                values[map_values].value.integer = string_to_i64(val_str, &line[last_non_ws +1] - val_str);
                break;
            case real_type:
                // we don't check for errors here, we just return zero
                values[map_values].value.real = string_to_double(val_str, &line[last_non_ws +1] - val_str);
                break;
            case string_type:
                // note that we never filter values
                value_id = add_word(val_dict, val_str);
                values[map_values].value.string = value_id;
                break;
            default:
                filter_log_msg(LOG_LEVEL_WARN, "Line %d had an unknown field type: %d\n", line_number, mvtype);
            }
            map_values++;
        } else if (state == MAPVALUE_CONTENTS && IS_NEWLINE(c)) {
            // end of map keys, beginning of map values
            state = EOL;
            line[last_non_ws + 1] = 0;
            // set the type
            values[map_values].type = mvtype;
            // set the value
            switch(mvtype) {
            case null_type:
                values[map_values].value.boolean = false;
                break;
            case boolean_type:
                values[map_values].value.boolean = mvbool;
                break;
            case integer_type:
                // we don't check for errors in the int parsing function
                values[map_values].value.integer = string_to_i64(val_str, &line[last_non_ws +1] - val_str);
                break;
            case real_type:
                // we don't check for errors here, we just return zero
                values[map_values].value.real = string_to_double(val_str, &line[last_non_ws +1] - val_str);
                break;
            case string_type:
                value_id = add_word(val_dict, val_str);
                values[map_values].value.string = value_id;
                break;
            default:
                filter_log_msg(LOG_LEVEL_WARN, "Line %d had an unknown field type: %d\n", line_number, mvtype);
            }
            map_values++;

            // make sure the counts are the same
            if (map_keys == map_values) {
                // if we're filtering, check the label to see if it is in the dictionary
                if (filter) {
                    name_id = find_word(name_dict, name);
                    // don't add the interval if the name isn't found
                    if (name_id == WORD_NOT_FOUND) {
                        return false;
                    }
                } else {
                    // otherwise add the label to the dictionary
                    name_id = add_word(name_dict, name);
                }
                // create an event with a map
                create_interval(p, name_id, ts, map_keys, keys, values);
                return true;
            } else {
                filter_log_msg(LOG_LEVEL_WARN, "Line %d had unequal numbers of map keys (%d) and values (%d)\n", line_number, map_keys, map_values);
            }
        }

        // map value DFA for determining type
        if (state == MAPVALUE_CONTENTS) {
            mverror = false;
            if (mvstate == UNKNOWN) {
                if (IS_WHITESPACE(c)) {
                    // ignore leading whitespace
                    mvstate = UNKNOWN;
                } else if (c == '0') {
                    mvstate = ZERO;
                    mvtype = integer_type;
                } else if (c >= '1' && c <= '9') {
                    mvstate = INT;
                    mvtype = integer_type;
                } else if (c == 't') {
                    mvstate = BOOLT;
                    mvtype = string_type;
                } else if (c == 'f') {
                    mvstate = BOOLF;
                    mvtype = string_type;
                } else if (c == '-') {
                    // this is a little weird, since it could be any number or string
                    // for now its a string, but we have to treat it separately
                    mvstate = NEG;
                    mvtype = string_type;
                } else {
                    mvstate = STRING;
                    mvtype = string_type;
                } 

            } else if (mvstate == INT) {
                if (IS_WHITESPACE(c)) {
                    // don't assume because there is trailing whitespace that this is a string now
                    mvstate = TRAILING_WS;
                } else if (c == '.') {
                    mvstate = REAL;
                    mvtype = real_type;
                } else if (c < '0' || c > '9') {
                    // we have to just treat it as a string, as there were non-numerics
                    // note that, if we were to support parsing hex strings, it would need to be recognized here
                    mvstate = STRING;
                    mvtype = string_type;
                }
            } else if (mvstate == ZERO) {
                if (IS_WHITESPACE(c)) {
                    // don't assume because there is trailing whitespace that this is a string now
                    mvstate = TRAILING_WS;
                } else if (c == '.') {
                    mvstate = REAL;
                } else if (c < '0' || c > '9') {
                    // we have to just treat it as a string, as there were non-numerics
                    // note that, if we were to support parsing hex strings, it would need to be recognized here
                    mvstate = STRING;
                    mvtype = string_type;
                }
            } else if (mvstate == REAL) {
                if (IS_WHITESPACE(c)) {
                    // don't assume because there is trailing whitespace that this is a string now
                    mvstate = TRAILING_WS;
                } else if (c < '0' || c > '9') {
                    // we have to just treat it as a string, as there were non-numerics
                    // note that, if we were to support parsing hex strings, it would need to be recognized here
                    mvstate = STRING;
                    mvtype = string_type;
                }
            } else if (mvstate == STRING) {
                // strings can have numbers too
                if (IS_WHITESPACE(c)) {
                    mvstate = TRAILING_WS;
                } else {
                    mvtype = string_type;
                } 

            } else if (mvstate == BOOLT && c == 'r') {
                mvstate = BOOLTR;
            } else if (mvstate == BOOLTR && c == 'u') {
                mvstate = BOOLTRU;
            } else if (mvstate == BOOLTRU && c == 'e') {
                mvstate = STRING;
                mvtype = boolean_type;
                mvbool = true;

            } else if (mvstate == BOOLF && c == 'a') {
                mvstate = BOOLFA;
            } else if (mvstate == BOOLFA && c == 'l') {
                mvstate = BOOLFAL;
            } else if (mvstate == BOOLFAL && c == 's') {
                mvstate = BOOLFALS;
            } else if (mvstate == BOOLFALS && c == 'e') {
                mvstate = STRING;
                mvtype = boolean_type;
                mvbool = false;

            } else if (mvstate == NEG) {
                // this is if we saw a negative sign/hyphen first
                if (IS_WHITESPACE(c)) {
                    // this is a bit weird, but we will accept ws between the - and numbers...
                    mvstate = NEG;
                } else if (c == '0') {
                    mvstate = ZERO;
                    mvtype = real_type;
                } else if (c >= '1' && c <= '9') {
                    mvstate = INT;
                    mvtype = integer_type;
                } else {
                    mvstate = STRING;
                    mvtype = string_type;
                } 
                
            } else if (mvstate == TRAILING_WS) {
                if (IS_WHITESPACE(c)) {
                    mvstate = TRAILING_WS;
                } else {
                    // otherwise, it is a string
                    mvstate = STRING;
                    mvtype = string_type;
                }
            }

            if (mverror) {
                filter_log_msg(LOG_LEVEL_WARN, "Line %d had an invalid character %c in map value %d (0 based)\n", line_number, c, map_values);
                return false;
            }
        }

        if (map_keys == MAX_MAP_PAIRS || map_values == MAX_MAP_PAIRS) {
            filter_log_msg(LOG_LEVEL_WARN, "Line %d had too many map key/value pairs (max %d)\n", line_number, MAX_MAP_PAIRS);
            return false;
        }
    }
    return false;
}
#endif
