/*
 * word.c
 * Implements a (initially very bad) data structure for holding the alphabet.
 *
 *  Created on: Jan 19, 2017
 *      Author: seanmk
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

#include <stdlib.h>
#include <stdio.h>

#include "types.h"
#include "dict.h"
#include "log.h"
#include "memory.h"
#include "strings.h"

#ifndef NO_DYNAMIC_MEMORY
void initialize_dictionary(dictionary *dict) {
    dict->words = (word*) malloc(sizeof(word) * INITIAL_DICTIONARY_SIZE);
    if (dict->words != NULL) {
        dict->dynamic = true;
        dict->space = INITIAL_DICTIONARY_SIZE;
        dict->size = 0;
        // set it to 0, since there are pointers involved
        clear_memory(dict->words, sizeof(word) * dict->space);

        // set up the initial hash table
        // the hash table should always be space * 2
        dict->hash = (word_id *) malloc(sizeof(word_id) * dict->space * 2);
        if (dict->hash != NULL) {
            // set to all 1's, so the default value for index and next is -1
            set_memory(dict->hash, sizeof(word_id) * dict->space * 2);
        } else {
            // if hash is null, free words since the dict is unusable
            free(dict->words);
            dict->words = NULL;
            dict->space = 0;
        }

    } else {
        dict->dynamic = false;
        dict->space = 0;
        dict->size = 0;
    }
}
#endif

void destroy_dictionary(dictionary *dict) {
#ifndef NO_DYNAMIC_MEMORY
    if (dict->words != NULL && dict->dynamic) {
        free(dict->words);
    }
    if (dict->hash != NULL && dict->dynamic) {
        free(dict->hash);
    }
#endif

    dict->words = NULL;
    dict->hash = NULL;
    dict->space = 0;
    dict->size = 0;
}

static unsigned int crc(const char *string) {
    const char *c = string;
    unsigned int high;
    unsigned int result = 0;

    //printf("crc reached, c is %d", (unsigned int)*c);
    while (*c != 0) {
        // extract high-order 5 bits from h
        high = result & 0xf8000000;
        // shift left by 5 bits
        result <<= 5;
        // move the high-order bits to the low order and XOR
        result ^= (high >> 27);
        // XOR with the input character
        result ^= *c++;
    }
    return result;
}

word_id find_word(dictionary *dict, const char *needle) {
    word_id candidate_id;
    word *candidate;
    unsigned int key;

    key = crc(needle) % (dict->space * 2);

    candidate_id = dict->hash[key];
    filter_log_msg(LOG_LEVEL_SUPERDEBUG, "find_word: needle %s, key %d, candidate_id %d\n", needle, key, candidate_id);
    // candidate_id should be -1 by default
    while (candidate_id != WORD_NOT_FOUND) {
        candidate = &dict->words[candidate_id];

        if (string_equals(candidate->string, needle, MAX_WORD_LENGTH)) {
            return candidate_id;
        }
        candidate_id = candidate->next_with_same_hash;
    }

    return WORD_NOT_FOUND;
}

word_id add_word(dictionary *dict, const char *add) {
    unsigned int key;
    word_id rebuild, index, *hash_realloc;
    word *words_realloc;
    bool is_space;

    // by default there is space
    is_space = true;

#ifndef NO_DYNAMIC_MEMORY
    if (dict->size >= dict->space && dict->dynamic) {
        // there's no room.  Try to make more
        is_space = false;

        if (dict->words != NULL) {
            words_realloc = realloc(dict->words, sizeof(word) * dict->space * 2);
            if (words_realloc != NULL) {
                // only set the words pointer if it isn't null
                dict->words = words_realloc;
                clear_memory(dict->words + dict->space, sizeof(word) * dict->space);
                dict->space = dict->space * 2;
                // there's room now
                is_space = true;
            }
        }
        if (is_space && dict->hash != NULL) {
            // rebuild the hash (space is now hopefully already doubled from resizing words)
            hash_realloc = realloc(dict->hash, sizeof(word_id) * dict->space * 2);
            if (hash_realloc != NULL) {
                dict->hash = hash_realloc;
                // first set all the bits
                set_memory(dict->hash, sizeof(word_id) * dict->space * 2);
                // now replace all the entries
                for (rebuild = 0; rebuild < dict->size; rebuild++) {
                    key = crc(dict->words[rebuild].string) % (dict->space * 2);
                    dict->words[rebuild].next_with_same_hash = dict->hash[key];
                    dict->hash[key] = rebuild;
                }
            } else {
                // reallocation didn't work
                is_space = false;
                // reset space to size, so we will try to resize if this is called again
                dict->space = dict->size;
            }
        }
    }
#endif

    if (is_space && dict->words != NULL && dict->hash != NULL) {
        // search for it first to make sure we avoid duplicate entries
        index = find_word(dict, add);

        // if the entry was not found
        if (index == WORD_NOT_FOUND) {
            // calculate the key
            key = crc(add) % (dict->space * 2);

            // it is not already present, so insert it
            copy_string(dict->words[dict->size].string, add, MAX_WORD_LENGTH);
            // insert into the hash
            dict->words[dict->size].next_with_same_hash = dict->hash[key];
            dict->hash[key] = dict->size;

            return dict->size++;
        } else {
            // if the word is already in the dictionary then just return its index
            return index;
        }
    }
    return WORD_NOT_FOUND;
}

char * get_word(dictionary *dict, word_id index) {
    if (index != WORD_NOT_FOUND && index < dict->size) {
        return dict->words[index].string;
    }
    return NULL;
}

/**
 * These are a little bit of overkill, since we actually just have a dense array of words
 */
void get_dictionary_iterator(dictionary *dict, dictionary_iterator *dit) {
    dit->dict = dict;
    dit->current = 0;
}
word_id next_word(dictionary_iterator *dit) {
    return dit->current++;
}
bool has_next_word(dictionary_iterator *dit) {
    return dit->current < dit->dict->size;
}

void log_words(dictionary *dict) {
    int i;
    log_msg("Dictionary(%d,%d,%p,%p)\n", dict->space, dict->size, dict->words, dict->hash);
    for (i = 0; i < dict->size; i++) {
        log_msg("[%d]%s ->(%d)\n", i, dict->words[i].string, dict->words[i].next_with_same_hash);
    }
}
