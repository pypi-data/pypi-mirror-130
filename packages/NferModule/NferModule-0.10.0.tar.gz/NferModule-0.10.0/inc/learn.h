/*
 * learn.h
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

#ifndef LEARN_H_
#define LEARN_H_

#include "types.h"
#include "nfer.h"
#include "dict.h"
#include "pool.h"

#define DEFAULT_CONFIDENCE 0.90
#define DEFAULT_SUPPORT 10

typedef struct _interval_stat {
    bool            seen;
    timestamp       start;
    timestamp       end;
} interval_stat;

typedef struct _learning_cell {
    unsigned int        matched;
    unsigned int        success;
    unsigned int        failure;
    unsigned long int   last_length;
    double              average_length;
    double              length_variance_s;
} learning_cell;

typedef struct _learning {
    int             size;
    learning_cell   *matrix;
    interval_stat   *stats;
} learning;

void initialize_learning(learning *, int);
void destroy_learning(learning *);
void add_learned_rules(learning *, dictionary *, nfer_specification *, float, float);
void finish_learning(learning *);
void learn_interval(learning *, interval *);
void run_learner_on_pool(pool *,
        unsigned int,
        dictionary *,
        dictionary *,
        dictionary *,
        nfer_specification *,
        float,
        float);


#endif /* LEARN_H_ */
