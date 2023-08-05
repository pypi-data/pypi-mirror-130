/*
 * map.c
 *
 *  Created on: Apr 3, 2017
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
#include <stdlib.h>

#include "types.h"
#include "dict.h"
#include "map.h"
#include "log.h"
#include "memory.h"


void initialize_map(data_map *map) {
#ifndef NO_DYNAMIC_MEMORY
    map->space = 0;
    map->values = NULL;
#endif
    map->start = MAP_MISSING_KEY;
}
void destroy_map(data_map *map) {
#ifndef NO_DYNAMIC_MEMORY
    if (map->space > 0) {
        map->space = 0;
    }

    if (map->values != NULL) {
        free(map->values);
        map->values = NULL;
    }
#else
    // just clear the map if there's no dynamic memory
    if (map->values != NULL) {
        clear_memory(map->values, map->space * sizeof(map_value_node));
    }
#endif
    map->start = MAP_MISSING_KEY;
}
void map_set(data_map *map, map_key key, map_value *value) {
    int new_space;
    map_value_node *values_alloc;

#ifndef NO_DYNAMIC_MEMORY
    // key is an index, so if the space is lower the storage needs to be expanded
    if (map->space <= key) {
        new_space = key + MAP_SIZE_INCREMENT;

        if (map->values == NULL) {
            values_alloc = (map_value_node *)malloc(sizeof(map_value_node) * new_space);
        } else {
            values_alloc = (map_value_node *)realloc(map->values, sizeof(map_value_node) * new_space);
        }

        if (values_alloc != NULL) {
            map->values = values_alloc;
            clear_memory(map->values + map->space, (new_space - map->space) * sizeof(map_value_node));
            map->space = new_space;
        }
    }
#endif

    if (map->values != NULL && map->space > key) {
        map->values[key].entry.type = value->type;
        switch(value->type) {
        case null_type:
            map->values[key].entry.value.boolean = false;
            // remove this key from the linked list if it is present in it

            break;
        case boolean_type:
            map->values[key].entry.value.boolean = value->value.boolean;
            break;
        case integer_type:
            map->values[key].entry.value.integer = value->value.integer;
            break;
        case real_type:
            map->values[key].entry.value.real = value->value.real;
            break;
        case string_type:
            map->values[key].entry.value.string = value->value.string;
            break;
        case pointer_type:
            map->values[key].entry.value.pointer = value->value.pointer;
            break;
        }

        // deal with linked list things separately
        switch(value->type) {
        case null_type:
            if (map->values[key].set) {
                // remove from the linked list
                map->values[key].set = false;
                if (map->values[key].next != MAP_MISSING_KEY) {
                    map->values[map->values[key].next].prior = map->values[key].prior;
                }
                if (map->values[key].prior != MAP_MISSING_KEY) {
                    map->values[map->values[key].prior].next = map->values[key].next;
                } else {
                    map->start = map->values[key].next;
                }
            }
            break;
        case boolean_type:
        case integer_type:
        case real_type:
        case string_type:
        case pointer_type:
            // don't re-add the key to the list if it is already present
            if (!map->values[key].set) {
                // keep a back reference for removal
                if (map->start != MAP_MISSING_KEY) {
                    map->values[map->start].prior = key;
                }
                map->values[key].set = true;
                map->values[key].next = map->start;
                map->values[key].prior = MAP_MISSING_KEY;
                map->start = key;
            }
        }
    }
}
void map_get(data_map *map, map_key key, map_value *result) {
    if (map->space > key && map->values != NULL) {
        result->type = map->values[key].entry.type;
        switch(map->values[key].entry.type) {
        case null_type:
            result->value.boolean = false;
            break;
        case boolean_type:
            result->value.boolean = map->values[key].entry.value.boolean;
            break;
        case integer_type:
            result->value.integer = map->values[key].entry.value.integer;
            break;
        case real_type:
            result->value.real = map->values[key].entry.value.real;
            break;
        case string_type:
            result->value.string = map->values[key].entry.value.string;
            break;
        case pointer_type:
            result->value.pointer = map->values[key].entry.value.pointer;
            break;
        }
    } else {
        result->type = null_type;
        result->value.boolean = false;
    }
}
/**
 * Search the map for the provided value and return the first key where it is found.
 *
 * Runs in linear time
 * @param map the data_map to search
 * @param value the value for which to search
 * @return the first key where value is found or MAP_MISSING_KEY if it is not found
 */
map_key map_find(data_map *map, map_value *value) {
    map_key k;
    map_value v;
    map_iterator mit;

    get_map_iterator(map, &mit);
    while(has_next_map_key(&mit)) {
        k = next_map_key(&mit);
        map_get(map, k, &v);

        if (equals(&v, value)) {
            return k;
        }
    }

    return MAP_MISSING_KEY;
}

void copy_map(data_map *dest, data_map *src, bool deep) {
    map_key k;
    map_value v;
    map_iterator mit;

#ifndef NO_DYNAMIC_MEMORY
    if (deep) {
        // allocate space for the new map all at once, so we don't end up calling realloc at all
        if (src->space > 0) {
            dest->values = (map_value_node *)malloc(sizeof(map_value_node) * src->space);

            if (dest->values != NULL) {
                clear_memory(dest->values, src->space * sizeof(map_value_node));
                dest->space = src->space;
            }
            dest->start = MAP_MISSING_KEY;
        }

        get_map_iterator(src, &mit);
        while(has_next_map_key(&mit)) {
            k = next_map_key(&mit);
            map_get(src, k, &v);
            map_set(dest, k, &v);
        }

    } else {
        // a shallow copy means to just copy the pointer
        dest->space = src->space;
        dest->values = src->values;
        dest->start = src->start;
    }
#else
    // first clear the destination map
    if (dest->values != NULL) {
        clear_memory(dest->values, dest->space * sizeof(map_value_node));
        dest->start = MAP_MISSING_KEY;

        if (src->values != NULL) {
            get_map_iterator(src, &mit);
            while(has_next_map_key(&mit)) {
                k = next_map_key(&mit);
                map_get(src, k, &v);
                map_set(dest, k, &v);
            }
        }
    }
#endif
}

void get_map_iterator(data_map *map, map_iterator *mit) {
    mit->map = map;
    mit->current = map->start;
}
map_key next_map_key(map_iterator *mit) {
    map_key k;

    k = mit->current;
    mit->current = mit->map->values[k].next;
    return k;
}
bool has_next_map_key(map_iterator *mit) {
    return mit->current != MAP_MISSING_KEY;
}
bool is_map_empty(data_map *map) {
    return map->start == MAP_MISSING_KEY;
}
/**
 * Returns true if the map has a key set, false if not.
 */
bool map_has_key(data_map *map, map_key key) {
    // this method is a little disingenuous, given how maps are implemented
    // however, it makes sense to do it this way since it hopefully
    // presents an interface that won't need to change if the implementation 
    // changes.
    if (map->space > key && map->values != NULL) {
        if(map->values[key].entry.type != null_type) {
            return true;
        }
    }
    return false;
}


void log_map(data_map *map) {
    map_key k;
    map_value v;
    map_iterator mit;
    bool first = true;

    log_msg("{");
    get_map_iterator(map, &mit);
    while (has_next_map_key(&mit)) {
        k = next_map_key(&mit);
        map_get(map, k, &v);
        if (!first) {
            log_msg(", ");
        }
        switch(v.type) {
        case null_type:
            // should never be reached
            log_msg("%d -> NULL", k);
            break;
        case boolean_type:
            log_msg("%d -> %s", k, (v.value.boolean ? "true" : "false"));
            break;
        case integer_type:
            log_msg("%d -> %d", k, v.value.integer);
            break;
        case real_type:
            log_msg("%d -> %f", k, v.value.real);
            break;
        case string_type:
            log_msg("%d -> %d", k, v.value.string);
            break;
        case pointer_type:
            log_msg("%d -> %p", k, v.value.pointer);
            break;
        }
        first = false;

    }
    log_msg("}");
}

void output_map_strings(data_map *map, dictionary *keys, dictionary *values, int log_to) {
    map_key k;
    map_value v;
    map_iterator mit;
    char *key_string, *value_string;
    bool first;

    if (!is_map_empty(map)) {
        write_msg(log_to, "|");
    }
    first = true;
    get_map_iterator(map, &mit);
    while (has_next_map_key(&mit)) {
        k = next_map_key(&mit);
        map_get(map, k, &v);

        key_string = get_word(keys, k);

        if (key_string != NULL) {
            if (!first) {
                write_msg(log_to, ";");
            }
            write_msg(log_to, key_string);
            first = false;
        }
    }
    if (!is_map_empty(map)) {
        write_msg(log_to, "|");
    }
    first = true;
    get_map_iterator(map, &mit);
    while (has_next_map_key(&mit)) {
        k = next_map_key(&mit);
        map_get(map, k, &v);
        if (!first) {
            write_msg(log_to, ";");
        }

        switch(v.type) {
        case null_type:
            // should never be reached
            write_msg(log_to, "NULL");
            break;
        case boolean_type:
            write_msg(log_to, "%s", (v.value.boolean ? "true" : "false"));
            break;
        case integer_type:
            write_msg(log_to, "%d", v.value.integer);
            break;
        case real_type:
            write_msg(log_to, "%f", v.value.real);
            break;
        case string_type:
            value_string = get_word(values, v.value.string);

            if (value_string != NULL) {
                write_msg(log_to, "%s", value_string);
            }
            break;
        case pointer_type:
            write_msg(log_to, "%p", k, v.value.pointer);
            break;
        }
        first = false;
    }
}

