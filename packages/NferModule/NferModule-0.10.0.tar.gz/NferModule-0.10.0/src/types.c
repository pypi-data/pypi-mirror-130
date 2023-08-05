/*
 * types.c
 *
 *  Created on: Jun 7, 2017
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

// we need float.h for the DBL constants...
#include <float.h>

#include "types.h"

/**
 * Returns the absolute value of a double, r.
 * Needed for the nearly_equals function below.
 **/
static double dabs(double r) {
    if (r < 0) {
        return -r;
    }
    return r;
}

/**
 * Returns the lesser of the two values.
 * Needed for the nearly_equals function below.
 **/
static double dmin(double a, double b) {
    if (a < b) {
        return a;
    }
    return b;
}

/**
 * Adapted from https://floating-point-gui.de nearlyEqual.
 * Two things to note:
 *   1) We ignore the guidance to provide an epsilon parameter, hard-coding a value.
 *      This isn't great!  But I don't want to provide a mechanism to give an epsilon in various APIs for now.
 *   2) We use double because that's the type used in the typed_value for reals.
 **/
static bool nearly_equals(double a, double b) {
    double abs_a = dabs(a);
    double abs_b = dabs(b);
    double diff  = dabs(a - b);
    double epsilon = 0.00001f;

    if (a == b) { // shortcut, handles infinities
        return true;

    } else if (a == 0 || b == 0 || ((abs_a + abs_b) < DBL_MIN)) {
        // a or b is zero or both are extremely close to it
        // relative error is less meaningful here
        return diff < (epsilon * DBL_MIN);
    } else { // use relative error
        return (diff / dmin((abs_a + abs_b), DBL_MAX)) < epsilon;
    }
}

bool equals(typed_value *left, typed_value *right) {
    // if both are null pointers, then I suppose they're equal?
    if (left == NULL && right == NULL) {
        return true;
    }

    // if one is a null pointer, though, then they're definitely not equal
    if (left == NULL || right == NULL) {
        return false;
    }

    // if their types aren't equal, then they aren't equal
    if (left->type != right->type) {
        return false;
    }

    switch(left->type) {
    case null_type:
        // both are null, so they are equal
        return true;
        break;
    case boolean_type:
        // just compare the boolean values
        return left->value.boolean == right->value.boolean;
        break;
    case integer_type:
        // just compare the integer values
        return left->value.integer == right->value.integer;
        break;
    case real_type:
        // have to use the nearly_equals function above...
        return nearly_equals(left->value.real, right->value.real);
        break;
    case string_type:
        // just compare the string values
        return left->value.string == right->value.string;
        break;
    case pointer_type:
        // just compare the pointer values
        return left->value.pointer == right->value.pointer;
        break;
    }

    // provide a default case to make the compiler happy
    return false;
}
