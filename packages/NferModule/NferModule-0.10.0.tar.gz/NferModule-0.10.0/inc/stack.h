/*
 * stack.h
 *
 *  Created on: Apr 29, 2017
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

#ifndef INC_STACK_H_
#define INC_STACK_H_

#include "types.h"

#define INITIAL_STACK_SPACE 8

typedef typed_value stack_value;

typedef struct _data_stack {
    unsigned int        space;
    unsigned int        tos;
    stack_value         *values;
} data_stack;

void initialize_stack(data_stack *);
void destroy_stack(data_stack *);
void push(data_stack *, stack_value *);
void pop(data_stack *, stack_value *);

#endif /* INC_STACK_H_ */
