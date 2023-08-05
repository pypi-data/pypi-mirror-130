/*
 * pool.h
 *
 *  Created on: Jan 22, 2017
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

#ifndef POOL_H_
#define POOL_H_

#include <stdint.h>
#include "types.h"
#include "dict.h"
#include "map.h"

typedef uint64_t timestamp;
typedef int label;

typedef unsigned int pool_index;

#define INITIAL_POOL_SIZE         16

#define COPY_POOL_OVERWRITE       0
#define COPY_POOL_APPEND          1
#define COPY_POOL_EXCLUDE_HIDDEN  0
#define COPY_POOL_INCLUDE_HIDDEN  1

#define END_OF_POOL         ((pool_index)-1)

typedef struct _interval {
    label       name;
    timestamp   start;
    timestamp   end;
    data_map    map;
    bool        hidden;
} interval;

#define EMPTY_INTERVAL ((interval){WORD_NOT_FOUND,0,0,EMPTY_MAP})

typedef struct _interval_node {
    interval    i;
    pool_index  prior;
    pool_index  next;
} interval_node;

typedef struct _pool {
    pool_index      size;
    pool_index      space;
    pool_index      removed;
    interval_node   *intervals;
    pool_index      start;
    pool_index      end;
} pool;

typedef struct _pool_iterator {
    pool        *p;
    pool_index  current;
    pool_index  last;
} pool_iterator;

void initialize_pool(pool *p);
void destroy_pool(pool *p);

void add_interval(pool *p, interval *add);
interval * allocate_interval(pool *p);
void copy_pool(pool *dest, pool *src, bool append, bool include_hidden);
void purge_pool(pool *p);
void sort_pool(pool *p);
void clear_pool(pool *p);
void remove_from_pool(pool_iterator *remove);

void get_pool_iterator(pool *p, pool_iterator *pit);
interval * next_interval(pool_iterator *pit);
bool has_next_interval(pool_iterator *pit);

int64_t compare_intervals(interval *, interval *);
bool equal_intervals(interval *, interval *);
void log_interval(interval *);
void output_interval(interval *, dictionary *, dictionary *, dictionary *, int);
void output_pool(pool *, dictionary *, dictionary *, dictionary *, int);

#endif /* POOL_H_ */
