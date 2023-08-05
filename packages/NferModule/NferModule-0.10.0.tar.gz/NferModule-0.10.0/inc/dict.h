/*
 * dict.h
 *
 *  Created on: Jan 19, 2017
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

#ifndef DICT_H_
#define DICT_H_

#include "types.h"


typedef int word_id;

#define INITIAL_DICTIONARY_SIZE 8
#define MAX_WORD_LENGTH         63
#define WORD_NOT_FOUND          ((word_id)-1)
#define EXPORT_DICT_USE_SIZE    ((char *)NULL)

typedef struct _word {
    char            string[MAX_WORD_LENGTH + 1];
    word_id         next_with_same_hash;
} word;

typedef struct _dict {
    int             space;
    int             size;
    word            *words;
    word_id         *hash;
    bool            dynamic;
} dictionary;

typedef struct _dictionary_iterator {
    dictionary      *dict;
    word_id         current;
} dictionary_iterator;

void initialize_dictionary(dictionary *dict);
void destroy_dictionary(dictionary *dict);
word_id add_word(dictionary *dict, const char *add);
char * get_word(dictionary *dict, word_id index);
word_id find_word(dictionary *dict, const char *needle);

void get_dictionary_iterator(dictionary *, dictionary_iterator *);
word_id next_word(dictionary_iterator *);
bool has_next_word(dictionary_iterator *);

void log_words(dictionary *dict);

#endif /* DICT_H_ */
