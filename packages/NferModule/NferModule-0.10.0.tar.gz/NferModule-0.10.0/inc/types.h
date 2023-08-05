/*
 * types.h
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

#ifndef TYPES_H_
#define TYPES_H_

#include <stdint.h>
#include <stddef.h>

/* GCC and CLANG specific defines */
#ifdef __GNUC__
    /* this is for marking parameters as unused in functions */
#   define UNUSED(x) UNUSED_ ## x __attribute__((__unused__))
    /* this is for marking functions as unused */
#   define UNUSED_FUNCTION(x) __attribute__((__unused__)) UNUSED_ ## x
    /* this is for marking funcitons as deprecated */
#   define DEPRECATED __attribute__((deprecated))
    /* this is for functions that don't return */
#   define NORETURN __attribute__((noreturn))
#else
#   define UNUSED(x) UNUSED_ ## x
#   define UNUSED_FUNCTION(x) UNUSED_ ## x
#   define DEPRECATED
#   define NORETURN
#endif


// ifndef doesn't work for typedefs, so use a define if we know such a thing exists already
#ifndef HAS_BOOL
typedef char bool;
#define true  1
#define false 0
#endif

#ifndef NULL
#define NULL ((void*)0)
/* since NULL isn't defined, we assume stddef.h isn't included */
typedef unsigned int size_t;
#endif


typedef enum {
    null_type,
    boolean_type,
    integer_type,
    real_type,
    string_type,
    pointer_type
} value_type;

union value_types {
    bool            boolean;
    int64_t         integer;
    double          real;
    unsigned int    string;
    void            *pointer;
};

typedef struct {
    value_type  type;
    union value_types value;
} typed_value;

bool equals(typed_value *, typed_value *);

#endif /* TYPES_H_ */
