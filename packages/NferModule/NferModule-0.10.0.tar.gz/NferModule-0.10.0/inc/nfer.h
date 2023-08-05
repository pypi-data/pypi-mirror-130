/*
 * nfer.h
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

#ifndef NFER_H_
#define NFER_H_

#include "expression.h"
#include "types.h"
#include "dict.h"
#include "pool.h"
#include "map.h"
#include "stack.h"

#define NFER_VERSION "1.5"

typedef bool (*temporal_test)(timestamp, timestamp, timestamp, timestamp);
typedef timestamp (*start_end)(timestamp, timestamp);
typedef bool (*map_test)(timestamp, timestamp, data_map *, timestamp, timestamp, data_map *);
typedef void (*map_generator)(data_map *, timestamp, timestamp, data_map *, timestamp, timestamp, data_map *);

typedef unsigned int rule_id;
#define MISSING_RULE_ID      ((rule_id)-1)

#define RULE_LIST_SIZE_ON_EMPTY 2

// define some optimization flag settings
#define NO_WINDOW 0

// these correspond to the indices of the operators array
typedef enum {
    ALSO_OPERATOR,
    BEFORE_OPERATOR,
    MEET_OPERATOR,
    DURING_OPERATOR,
    COINCIDE_OPERATOR,
    START_OPERATOR,
    FINISH_OPERATOR,
    OVERLAP_OPERATOR,
    SLICE_OPERATOR,
    AFTER_OPERATOR,
    FOLLOW_OPERATOR,
    CONTAIN_OPERATOR,
    N_OPERATORS
} operator_code;

typedef struct _nfer_operator {
    char            *name;
    temporal_test   test;
    start_end       start_time;
    start_end       end_time;
    bool            exclusion;
} nfer_operator;

typedef struct _phi_function {
    char                *name;
    map_test            test;
    map_generator       result;
} phi_function;

typedef struct _nfer_rule {
    operator_code       op_code;
    label               left_label;
    label               right_label;
    label               result_label;
    bool                exclusion;
    phi_function        *phi;
    pool                new_intervals;
    pool                left_cache;
    pool                right_cache;
    pool                produced;
    rule_id             next;

    bool                hidden;  // this is a hidden rule, caused by nesting in specifications
    expression_input    *where_expression;
    expression_input    *begin_expression;
    expression_input    *end_expression;
    data_map            map_expressions;
    data_stack          expression_stack;
} nfer_rule;

typedef struct _nfer_specification {
    nfer_rule       *rules;
    unsigned int    size;
    unsigned int    space;
} nfer_specification;

void initialize_specification(nfer_specification *spec, unsigned int size);
void destroy_specification(nfer_specification *spec);

nfer_rule * add_rule_to_specification(nfer_specification *spec,
        label result_label_index, label left_label_index, operator_code op_code, label right_label_index, phi_function *phi);
bool is_subscribed(nfer_specification *, label);
bool is_published(nfer_specification *, label);
bool is_mapped(nfer_specification *, map_key);

void add_interval_to_specification(nfer_specification *spec, interval *add, pool *out);

void run_nfer(nfer_specification *spec, pool *input_pool, pool *output_pool);

void log_specification(nfer_specification *, dictionary *, dictionary *, dictionary *);
void output_specification(nfer_specification *, dictionary *, dictionary *, dictionary *);

#endif /* NFER_H_ */
