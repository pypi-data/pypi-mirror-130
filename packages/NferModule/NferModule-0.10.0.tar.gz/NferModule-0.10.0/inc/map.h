/*
 * map.h
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

#ifndef INC_MAP_H_
#define INC_MAP_H_


#include "types.h"
#include "dict.h"


#define COPY_MAP_SHALLOW    0
#define COPY_MAP_DEEP       1
#define EMPTY_MAP           ((data_map){0, NULL, MAP_MISSING_KEY})

typedef word_id map_key;
typedef typed_value map_value;

#define MAP_MISSING_KEY     WORD_NOT_FOUND
#define MAP_SIZE_INCREMENT  1

typedef struct _map_value_node {
    map_value       entry;
    map_key         prior;
    map_key         next;
    bool            set; // this is used so we don't have to rely on next to know if the node is in the linked list
} map_value_node;

typedef struct _data_map {
    int             space;
    map_value_node  *values;
    map_key         start;
} data_map;

typedef struct _map_iterator {
    data_map        *map;
    map_key         current;
} map_iterator;

void initialize_map(data_map *);
void destroy_map(data_map *);
void map_set(data_map *, map_key, map_value *);
void map_get(data_map *, map_key, map_value *);
map_key map_find(data_map *, map_value *);
void copy_map(data_map *, data_map *, bool);
bool is_map_empty(data_map *);
bool map_has_key(data_map*, map_key);

void get_map_iterator(data_map *, map_iterator *);
map_key next_map_key(map_iterator *);
bool has_next_map_key(map_iterator *);

void log_map(data_map *);
void output_map_strings(data_map *, dictionary *, dictionary *, int);

#endif /* INC_MAP_H_ */
