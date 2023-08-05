/*
 * expression.h
 *
 *  Created on: Apr 24, 2017
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

#ifndef INC_EXPRESSION_H_
#define INC_EXPRESSION_H_

#include <stdint.h>
#include "dict.h"
#include "map.h"
#include "pool.h"
#include "stack.h"


typedef map_value value_stack;

typedef enum {
    action_add,
    action_sub,
    action_mul,
    action_div,
    action_mod,

    action_lt,
    action_gt,
    action_lte,
    action_gte,
    action_eq,
    action_ne,

    action_and,
    action_or,

    action_neg,
    action_not,

    param_boollit,
    param_intlit,
    param_reallit,
    param_strlit,

    param_left_field,
    param_right_field,

    param_left_begin,
    param_left_end,
    param_right_begin,
    param_right_end

} expression_action;

typedef union {
    unsigned int        length;
    expression_action   action;
    bool                boolean_value;
    int64_t             integer_value;
    double              real_value;
    word_id             string_value;
    map_key             field_name;
} expression_input;

void initialize_expression_input(expression_input **, unsigned int);
void destroy_expression_input(expression_input **);
void evaluate_expression(expression_input *, typed_value *, data_stack *,
        timestamp, timestamp, data_map *, timestamp , timestamp , data_map *);
unsigned int max_expression_stack_depth(expression_input *);
void write_expression(expression_input *, dictionary *, dictionary *, const char *, const char *, int);

#endif /* INC_EXPRESSION_H_ */
