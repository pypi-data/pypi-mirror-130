/*
 * semantic.h
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

#ifndef INC_SEMANTIC_H_
#define INC_SEMANTIC_H_

#include "ast.h"
#include "dict.h"

typedef enum {
    null,
    boolean,
    integer,
    real,
    string,
    duck,
    error
} ast_value_type;

#define NOT_NESTED_IE false
#define NESTED_IE true
#define NOT_WHERE_EXPR false
#define WHERE_EXPR true

ast_value_type check_types(ast_node *);
bool determine_labels(ast_node *, dictionary *, dictionary *, dictionary *);
bool determine_fields(ast_node *, dictionary *, dictionary *, dictionary *);
void populate_string_literals(ast_node *, dictionary *, dictionary *);


#endif /* INC_SEMANTIC_H_ */
