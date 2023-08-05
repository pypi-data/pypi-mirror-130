/*
 * ast.h
 *
 *  Created on: Apr 23, 2017
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

#ifndef _AST_H_
#define _AST_H_

#include <stdint.h>
#include "dict.h"
#include "map.h"

typedef enum {
    type_int_literal,
    type_float_literal,
    type_string_literal,
    type_boolean_literal,
    type_unary_expr,
    type_binary_expr,
    type_map_field,
    type_time_field,
    type_atomic_interval_expr,
    type_binary_interval_expr,
    type_map_expr_list,
    type_end_points,
    type_rule,
    type_rule_list,
    type_module_list,
    type_import_list
} node_enum;

typedef enum {
    left_side,
    right_side
} side_enum;

/* literals */
typedef struct {
    int64_t value;                      /* value of constant */
} int_literal_node;

typedef struct {
    double value;                        /* value of constant */
} float_literal_node;

typedef struct {
    word_id id;                          /* index into parser_dict */

    /* extra annotations to be set during semantic analysis */
    word_id val_dict_id;
} string_literal_node;

typedef struct {
    bool value;
} boolean_literal_node;

/* unary and binary expressions */
typedef struct {
    int operator;                   /* operator */
    struct _ast_node *operand;      /* operand */
} unary_expr_node;

typedef struct {
    int operator;                 /* operator */
    struct _ast_node *left;       /* operands */
    struct _ast_node *right;

    /* extra annotations to be set during semantic analysis */
    struct _ast_node *belongs_in;
} binary_expr_node;

/* map and time fields */
typedef struct {
    word_id label;
    word_id map_key;

    /* extra annotations to be set during semantic analysis */
    map_key resulting_map_key;
    side_enum side;
    struct _ast_node *interval_expression;
    map_key resulting_label_id;
    bool is_non_boolean;
} map_field_node;

typedef struct {
    int time_field;
    word_id label;

    /* extra annotations to be set during semantic analysis */
    map_key resulting_map_key;
    side_enum side;
    bool is_time;
    struct _ast_node *interval_expression;
    map_key resulting_label_id;
} time_field_node;

/* interval expressions */
typedef struct {
    word_id label;
    word_id id;

    /* extra annotations to be set during semantic analysis */
    word_id result_id;
    bool separate;
    data_map field_map;
    word_id begin_map;
    word_id end_map;

} atomic_interval_expr_node;

typedef struct {
    int interval_op;
    bool exclusion;
    struct _ast_node *left;
    struct _ast_node *right;

    /* extra annotations to be set during semantic analysis */
    word_id left_name;
    word_id right_name;
    data_map left_label_map;
    data_map right_label_map;
    data_map left_field_map;
    data_map right_field_map;
    word_id left_begin_map;
    word_id right_begin_map;
    word_id left_end_map;
    word_id right_end_map;

} binary_interval_expr_node;

/* rules */
typedef struct {
    word_id map_key;
    struct _ast_node *map_expr;
    struct _ast_node *tail;

    /* extra annotations to be set during semantic analysis */
    word_id resulting_map_key;
} map_expr_list_node;

typedef struct {
    struct _ast_node *begin_expr;
    struct _ast_node *end_expr;
} end_points_node;

typedef struct {
    word_id id;
    struct _ast_node *interval_expr;
    struct _ast_node *where_expr;
    struct _ast_node *map_expr_list;
    struct _ast_node *end_points;

    /* extra annotations to be set during semantic analysis */
    data_map label_map;
    word_id result_id;
} rule_node;

/* specification */
typedef struct {
    struct _ast_node *head;
    struct _ast_node *tail;
} rule_list_node;

typedef struct {
    word_id id;
    struct _ast_node *imports;
    struct _ast_node *rules;
    struct _ast_node *tail;
} module_list_node;

typedef struct {
    word_id import;
    struct _ast_node *tail;
} import_list_node;

typedef struct _location_type {
    int first_line;
    int first_column;
    int last_line;
    int last_column;
} location_type;

typedef struct _ast_node {
    node_enum type;                  /* type of node */
    location_type location;

    /* this all used to be in a union to save memory, but for now they will all just be struct members */
    /* if there is a desire to reduce the memory used by the DSL in the future this can be moved back out */
    int_literal_node int_literal;
    float_literal_node float_literal;
    string_literal_node string_literal;
    boolean_literal_node boolean_literal;
    unary_expr_node unary_expr;
    binary_expr_node binary_expr;
    map_field_node map_field;
    time_field_node time_field;
    atomic_interval_expr_node atomic_interval_expr;
    binary_interval_expr_node binary_interval_expr;
    map_expr_list_node map_expr_list;
    end_points_node end_points;
    rule_node rule;
    rule_list_node rule_list;
    module_list_node module_list;
    import_list_node import_list;

} ast_node;

/* prototypes */
ast_node *new_int_literal(long int, location_type *);
ast_node *new_float_literal(double, location_type *);
ast_node *new_string_literal(word_id, location_type *);
ast_node *new_boolean_literal(bool, location_type *);
ast_node *new_unary_expr(int, ast_node *, location_type *);
ast_node *new_binary_expr(int, ast_node *, ast_node *);
ast_node *new_map_field(word_id, word_id, location_type *, location_type *);
ast_node *new_time_field(int, word_id, location_type *, location_type *);
ast_node *new_atomic_interval_expr(word_id, word_id, location_type *, location_type *);
ast_node *new_binary_interval_expr(int, bool, ast_node *, ast_node *);
ast_node *new_map_expr_list(word_id, ast_node *, ast_node *, location_type *);
ast_node *new_end_points(ast_node *, ast_node *, location_type *);
ast_node *new_rule(word_id, ast_node *, ast_node *, ast_node *, ast_node *, location_type *);
ast_node *new_rule_list(ast_node *, ast_node *);
ast_node *new_module_list(word_id, ast_node *, ast_node *, ast_node *, location_type *);
ast_node *new_import_list(word_id, ast_node *, location_type *);

void parse_error(ast_node *, const char *);
void free_node(ast_node *);

#endif
