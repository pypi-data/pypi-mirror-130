/*
 * expression.c
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

#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>

#include "types.h"
#include "strings.h"
#include "memory.h"
#include "expression.h"
#include "log.h"
#include "dict.h"
#include "map.h"
#include "pool.h"
#include "stack.h"

#ifndef NO_DYNAMIC_MEMORY
void initialize_expression_input(expression_input **input, unsigned int size) {
    *input = NULL;
    if (size > 0) {
        *input = malloc((sizeof(expression_input) * size) + (sizeof(unsigned int) * 2));
        (*input)[0].length = size;
    }
}
void destroy_expression_input(expression_input **input) {
    if (*input != NULL) {
        free(*input);
        *input = NULL;
    }
}
#endif

void evaluate_expression(expression_input *input, typed_value *result, data_stack *stack,
        /* runtime supplied data */
        timestamp left_begin, timestamp left_end, data_map *left_map,
        timestamp right_begin, timestamp right_end, data_map *right_map) {

    unsigned int position, length;
    expression_action action;
    map_key key;
    stack_value typed, left_value, right_value;

    // length is stored as the first element in the action list
    length = input[0].length;

    position = 1;

    while (position < length) {
        action = input[position++].action;

        switch(action) {
        case action_add:
            pop(stack, &right_value);
            pop(stack, &left_value);
            if (left_value.type == real_type) {
                typed.type = real_type;

                if (right_value.type == real_type) {
                    typed.value.real = left_value.value.real + right_value.value.real;
                } else if (right_value.type == integer_type) {
                    typed.value.real = left_value.value.real + right_value.value.integer;
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on right side of add\n");
                }
            } else if (left_value.type == integer_type) {
                if (right_value.type == real_type) {
                    typed.type = real_type;
                    typed.value.real = left_value.value.integer + right_value.value.real;
                } else if (right_value.type == integer_type) {
                    typed.type = integer_type;
                    typed.value.integer = left_value.value.integer + right_value.value.integer;
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on right side of add\n");
                }
            } else {
                filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on left side of add\n");
            }
            push(stack, &typed);
            break;
        case action_sub:
            pop(stack, &right_value);
            pop(stack, &left_value);
            if (left_value.type == real_type) {
                typed.type = real_type;

                if (right_value.type == real_type) {
                    typed.value.real = left_value.value.real - right_value.value.real;
                } else if (right_value.type == integer_type) {
                    typed.value.real = left_value.value.real - right_value.value.integer;
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on right side of sub\n");
                }
            } else if (left_value.type == integer_type) {
                if (right_value.type == real_type) {
                    typed.type = real_type;
                    typed.value.real = left_value.value.integer - right_value.value.real;
                } else if (right_value.type == integer_type) {
                    typed.type = integer_type;
                    typed.value.integer = left_value.value.integer - right_value.value.integer;
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on right side of sub\n");
                }
            } else {
                filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on left side of sub\n");
            }
            push(stack, &typed);
            break;
        case action_mul:
            pop(stack, &right_value);
            pop(stack, &left_value);
            if (left_value.type == real_type) {
                typed.type = real_type;

                if (right_value.type == real_type) {
                    typed.value.real = left_value.value.real * right_value.value.real;
                } else if (right_value.type == integer_type) {
                    typed.value.real = left_value.value.real * right_value.value.integer;
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on right side of mul\n");
                }
            } else if (left_value.type == integer_type) {
                if (right_value.type == real_type) {
                    typed.type = real_type;
                    typed.value.real = left_value.value.integer * right_value.value.real;
                } else if (right_value.type == integer_type) {
                    typed.type = integer_type;
                    typed.value.integer = left_value.value.integer * right_value.value.integer;
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on right side of mul\n");
                }
            } else {
                filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on left side of mul\n");
            }
            push(stack, &typed);
            break;
        case action_div:
            pop(stack, &right_value);
            pop(stack, &left_value);
            if (left_value.type == real_type) {
                typed.type = real_type;

                if (right_value.type == real_type) {
                    if (right_value.value.real != 0.0) {
                        typed.value.real = left_value.value.real / right_value.value.real;
                    } else {
                        filter_log_msg(LOG_LEVEL_WARN, "Divide by zero error in expression evaluation\n");
                        typed.value.real = 0.0;
                    }
                } else if (right_value.type == integer_type) {
                    if (right_value.value.integer != 0) {
                        typed.value.real = left_value.value.real / right_value.value.integer;
                    } else {
                        filter_log_msg(LOG_LEVEL_WARN, "Divide by zero error in expression evaluation\n");
                        typed.value.real = 0.0;
                    }
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on right side of div\n");
                }
            } else if (left_value.type == integer_type) {
                if (right_value.type == real_type) {
                    typed.type = real_type;
                    if (right_value.value.real != 0.0) {
                        typed.value.real = left_value.value.integer / right_value.value.real;
                    } else {
                        filter_log_msg(LOG_LEVEL_WARN, "Divide by zero error in expression evaluation\n");
                        typed.value.real = 0.0;
                    }
                } else if (right_value.type == integer_type) {
                    typed.type = integer_type;
                    if (right_value.value.integer != 0) {
                        typed.value.integer = left_value.value.integer / right_value.value.integer;
                    } else {
                        filter_log_msg(LOG_LEVEL_WARN, "Divide by zero error in expression evaluation\n");
                        typed.value.integer = 0.0;
                    }
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on right side of div\n");
                }
            } else {
                filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on left side of div\n");
            }
            push(stack, &typed);
            break;
        case action_mod:
            pop(stack, &right_value);
            pop(stack, &left_value);
            if (left_value.type == integer_type) {
                if (right_value.type == integer_type) {
                    typed.type = integer_type;
                    if (right_value.value.integer != 0) {
                        typed.value.integer = left_value.value.integer % right_value.value.integer;
                    } else {
                        filter_log_msg(LOG_LEVEL_WARN, "Divide by zero error in expression evaluation\n");
                        typed.value.integer = 0.0;
                    }
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-integer value on right side of mod\n");
                }
            } else {
                filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-integer value on left side of mod\n");
            }
            push(stack, &typed);
            break;

        case action_lt:
            pop(stack, &right_value);
            pop(stack, &left_value);
            typed.type = boolean_type;
            // default to false if there is an error
            typed.value.boolean = false;

            if (left_value.type == real_type) {
                if (right_value.type == real_type) {
                    typed.value.boolean = left_value.value.real < right_value.value.real;
                } else if (right_value.type == integer_type) {
                    typed.value.boolean = left_value.value.real < right_value.value.integer;
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on right side of <\n");
                }
            } else if (left_value.type == integer_type) {
                if (right_value.type == real_type) {
                    typed.value.boolean = left_value.value.integer < right_value.value.real;
                } else if (right_value.type == integer_type) {
                    typed.value.boolean = left_value.value.integer < right_value.value.integer;
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on right side of <\n");
                }
            } else {
                filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on left side of <\n");
            }
            push(stack, &typed);
            break;

        case action_gt:
            pop(stack, &right_value);
            pop(stack, &left_value);
            typed.type = boolean_type;
            // default to false if there is an error
            typed.value.boolean = false;

            if (left_value.type == real_type) {
                if (right_value.type == real_type) {
                    typed.value.boolean = left_value.value.real > right_value.value.real;
                } else if (right_value.type == integer_type) {
                    typed.value.boolean = left_value.value.real > right_value.value.integer;
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on right side of >\n");
                }
            } else if (left_value.type == integer_type) {
                if (right_value.type == real_type) {
                    typed.value.boolean = left_value.value.integer > right_value.value.real;
                } else if (right_value.type == integer_type) {
                    typed.value.boolean = left_value.value.integer > right_value.value.integer;
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on right side of >\n");
                }
            } else {
                filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on left side of >\n");
            }
            push(stack, &typed);
            break;

        case action_lte:
            pop(stack, &right_value);
            pop(stack, &left_value);
            typed.type = boolean_type;
            // default to false if there is an error
            typed.value.boolean = false;

            if (left_value.type == real_type) {
                if (right_value.type == real_type) {
                    typed.value.boolean = left_value.value.real <= right_value.value.real;
                } else if (right_value.type == integer_type) {
                    typed.value.boolean = left_value.value.real <= right_value.value.integer;
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on right side of <=\n");
                }
            } else if (left_value.type == integer_type) {
                if (right_value.type == real_type) {
                    typed.value.boolean = left_value.value.integer <= right_value.value.real;
                } else if (right_value.type == integer_type) {
                    typed.value.boolean = left_value.value.integer <= right_value.value.integer;
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on right side of <=\n");
                }
            } else {
                filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on left side of <=\n");
            }
            push(stack, &typed);
            break;

        case action_gte:
            pop(stack, &right_value);
            pop(stack, &left_value);
            typed.type = boolean_type;
            // default to false if there is an error
            typed.value.boolean = false;

            if (left_value.type == real_type) {
                if (right_value.type == real_type) {
                    typed.value.boolean = left_value.value.real >= right_value.value.real;
                } else if (right_value.type == integer_type) {
                    typed.value.boolean = left_value.value.real >= right_value.value.integer;
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on right side of >=\n");
                }
            } else if (left_value.type == integer_type) {
                if (right_value.type == real_type) {
                    typed.value.boolean = left_value.value.integer >= right_value.value.real;
                } else if (right_value.type == integer_type) {
                    typed.value.boolean = left_value.value.integer >= right_value.value.integer;
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on right side of >=\n");
                }
            } else {
                filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on left side of >=\n");
            }
            push(stack, &typed);
            break;

        case action_eq:
            pop(stack, &right_value);
            pop(stack, &left_value);
            typed.type = boolean_type;
            // default to false if there is an error
            typed.value.boolean = false;

            if (left_value.type == real_type) {
                if (right_value.type == real_type) {
                    typed.value.boolean = left_value.value.real == right_value.value.real;
                } else if (right_value.type == integer_type) {
                    typed.value.boolean = left_value.value.real == right_value.value.integer;
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on right side of = but numeric on left\n");
                }
            } else if (left_value.type == integer_type) {
                if (right_value.type == real_type) {
                    typed.value.boolean = left_value.value.integer == right_value.value.real;
                } else if (right_value.type == integer_type) {
                    typed.value.boolean = left_value.value.integer == right_value.value.integer;
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on right side of = but numeric on left\n");
                }
            } else if (left_value.type == string_type) {
                if (right_value.type == string_type) {
                    typed.value.boolean = left_value.value.string == right_value.value.string;
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-string value on right side of = but string on left\n");
                }
            } else if (left_value.type == boolean_type) {
                if (right_value.type == boolean_type) {
                    typed.value.boolean = left_value.value.boolean == right_value.value.boolean;
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-Boolean value on right side of = but Boolean on left\n");
                }
            } else {
                // it isn't possible to get a pointer type
                filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: NULL on left side of =\n");
            }
            push(stack, &typed);
            break;

        case action_ne:
            pop(stack, &right_value);
            pop(stack, &left_value);
            typed.type = boolean_type;
            // default to false if there is an error
            typed.value.boolean = false;

            if (left_value.type == real_type) {
                if (right_value.type == real_type) {
                    typed.value.boolean = left_value.value.real != right_value.value.real;
                } else if (right_value.type == integer_type) {
                    typed.value.boolean = left_value.value.real != right_value.value.integer;
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on right side of != but numeric on left\n");
                }
            } else if (left_value.type == integer_type) {
                if (right_value.type == real_type) {
                    typed.value.boolean = left_value.value.integer != right_value.value.real;
                } else if (right_value.type == integer_type) {
                    typed.value.boolean = left_value.value.integer != right_value.value.integer;
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value on right side of != but numeric on left\n");
                }
            } else if (left_value.type == string_type) {
                if (right_value.type == string_type) {
                    typed.value.boolean = left_value.value.string != right_value.value.string;
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-string value on right side of != but string on left\n");
                }
            } else if (left_value.type == boolean_type) {
                if (right_value.type == boolean_type) {
                    typed.value.boolean = left_value.value.boolean != right_value.value.boolean;
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-Boolean value on right side of = but Boolean on left\n");
                }
            } else {
                // it isn't possible to get a pointer type
                filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: NULL on left side of !=\n");
            }
            push(stack, &typed);
            break;

        case action_and:
            pop(stack, &right_value);
            pop(stack, &left_value);
            typed.type = boolean_type;
            // default to false if there is an error
            typed.value.boolean = false;

            if (left_value.type == boolean_type) {
                if (right_value.type == boolean_type) {
                    typed.value.boolean = left_value.value.boolean && right_value.value.boolean;
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-Boolean value on right side of &\n");
                }
            } else {
                filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-Boolean value on left side of &\n");
            }
            push(stack, &typed);
            break;

        case action_or:
            pop(stack, &right_value);
            pop(stack, &left_value);
            typed.type = boolean_type;
            // default to false if there is an error
            typed.value.boolean = false;

            if (left_value.type == boolean_type) {
                if (right_value.type == boolean_type) {
                    typed.value.boolean = left_value.value.boolean || right_value.value.boolean;
                } else {
                    filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-Boolean value on right side of |\n");
                }
            } else {
                filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-Boolean value on left side of |\n");
            }
            push(stack, &typed);
            break;

        case action_neg:
            pop(stack, &left_value);

            if (left_value.type == integer_type) {
                typed.type = integer_type;
                typed.value.integer = -left_value.value.integer;
            } else if (left_value.type == real_type) {
                typed.type = real_type;
                typed.value.real = -left_value.value.real;
            } else {
                filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-numeric value modified by unary -\n");
                typed.type = integer_type;
                typed.value.integer = 0;
            }
            push(stack, &typed);
            break;

        case action_not:
            pop(stack, &left_value);
            typed.type = boolean_type;
            // default to false if there is an error
            typed.value.boolean = false;

            if (left_value.type == boolean_type) {
                typed.value.boolean = !left_value.value.boolean;
            } else {
                filter_log_msg(LOG_LEVEL_ERROR, "Type error in expression evaluation: non-Boolean value modified by unary !\n");
            }
            push(stack, &typed);
            break;

        case param_boollit:
            typed.type = boolean_type;
            typed.value.boolean = input[position++].boolean_value;
            push(stack, &typed);
            break;
        case param_intlit:
            typed.type = integer_type;
            typed.value.integer = input[position++].integer_value;
            push(stack, &typed);
            break;
        case param_reallit:
            typed.type = real_type;
            typed.value.real = input[position++].real_value;
            push(stack, &typed);
            break;
        case param_strlit:
            typed.type = string_type;
            typed.value.string = input[position++].string_value;
            push(stack, &typed);
            break;
        case param_left_field:
            key = input[position++].field_name;
            map_get(left_map, key, &typed);
            if (typed.type == null_type) {
                filter_log_msg(LOG_LEVEL_WARN, "Type error in expression evaluation: Null type for %d\n", key);
            }
            push(stack, &typed);
            break;
        case param_right_field:
            key = input[position++].field_name;
            map_get(right_map, key, &typed);
            if (typed.type == null_type) {
                filter_log_msg(LOG_LEVEL_WARN, "Type error in expression evaluation: Null type for %d\n", key);
            }
            push(stack, &typed);
            break;
        case param_left_begin:
            typed.type = integer_type;
            typed.value.integer = left_begin;
            push(stack, &typed);
            break;
        case param_left_end:
            typed.type = integer_type;
            typed.value.integer = left_end;
            push(stack, &typed);
            break;
        case param_right_begin:
            typed.type = integer_type;
            typed.value.integer = right_begin;
            push(stack, &typed);
            break;
        case param_right_end:
            typed.type = integer_type;
            typed.value.integer = right_end;
            push(stack, &typed);
            break;
        }

    }

    pop(stack, result);
}

unsigned int max_expression_stack_depth(expression_input *input) {
    unsigned int position, length, depth, max;
    expression_action action;

    // length is stored as the first element in the action list
    length = input[0].length;

    position = 1;
    depth = 0;
    max = 0;

    while (position < length) {
        action = input[position++].action;

        switch(action) {
        case action_add:
        case action_sub:
        case action_mul:
        case action_div:
        case action_mod:
        case action_lt:
        case action_gt:
        case action_lte:
        case action_gte:
        case action_eq:
        case action_ne:
        case action_and:
        case action_or:
            depth -= 1;
            break;

        case action_neg:
        case action_not:
            depth += 0;
            break;

        case param_boollit:
        case param_intlit:
        case param_reallit:
        case param_strlit:
        case param_left_field:
        case param_right_field:
            position++;
            /* falls through */
        case param_left_begin:
        case param_left_end:
        case param_right_begin:
        case param_right_end:
            depth += 1;
            break;
        }

        if (depth > max) {
            max = depth;
        }

    }

    return max;
}

#ifndef NO_DYNAMIC_MEMORY
void write_expression(expression_input *input,
                      dictionary *key_dict,
                      dictionary *val_dict,
                      const char *left_name,
                      const char *right_name,
                      int log_to) {
    char *begin = "begin", *end = "end", *true_str = "true", *false_str = "false";
    unsigned int position, length;
    expression_action action;
    /* this is so we can keep track of string lengths
     * it is, admittedly, a bit of an over-optimization */
    typedef struct _pstring {
        int  length;
        char *str;
    } pstring;

    pstring *stack;
    /* top of stack */
    unsigned int tos;
    pstring buffer, lstring, rstring;
    char *field_string, operator_char;
    int left_name_length, right_name_length, field_string_length, extra_space;

    // stack is used for storing pointers to strings and reordering them
    // we shouldn't need to realloc this since we have the max depth
    stack = malloc(sizeof(pstring) * max_expression_stack_depth(input));
    if (stack == NULL) {
        // if we can't allocate space, bail
        return;
    }
    // top of stack is zero - stack is empty ascending
    tos = 0;

    // get the length of the left and right names
    left_name_length = string_length(left_name, MAX_WORD_LENGTH);
    right_name_length = string_length(right_name, MAX_WORD_LENGTH);

    // length is stored as the first element in the action list
    length = input[0].length;

    position = 1;

    while (position < length) {
        action = input[position++].action;
        // extra_space designates two char operators (>=, <=, !=)
        extra_space = 0;
        // field_string is for both fields and begin/end
        field_string = NULL;
        field_string_length = 0;
        // operator_char is the char for the operator (duh)
        operator_char = '\0';
        // make sure right and left string variables are cleared
        rstring.length = 0;
        rstring.str = NULL;
        lstring.length = 0;
        lstring.str = NULL;
        // same with buffer
        buffer.length = 0;
        buffer.str = NULL;

        /* this switch is to calculate how much space we need in the buffer */
        switch(action) {
        case action_lte:
        case action_gte:
        case action_ne:
            /* these operators are two characters wide */
            extra_space = 1;
            /* falls through */

        case action_add:
        case action_sub:
        case action_mul:
        case action_div:
        case action_mod:
        case action_lt:
        case action_gt:
        case action_eq:
        case action_and:
        case action_or:
            // pop the right value
            rstring.length = stack[--tos].length;
            rstring.str    = stack[tos].str;
            // pop the left value
            lstring.length = stack[--tos].length;
            lstring.str    = stack[tos].str;

            // allocate space for the buffer string
            // the two sides plus enough for ( X )
            buffer.length = lstring.length + rstring.length + 5 + extra_space;
            break;

        case action_neg:
        case action_not:
            // just pop the right value
            rstring.length = stack[--tos].length;
            rstring.str    = stack[tos].str;

            // allocate space for the buffer string
            // the right side plus enough for (X )
            buffer.length = rstring.length + 4;
            break;

        case param_left_begin:
            // allocate buffer space for the name and temporal parameter (.begin)
            field_string_length = 5;
            field_string = begin;
            buffer.length = left_name_length + 6;
            break;
        case param_left_end:
            // allocate buffer space for the name and temporal parameter (.end)
            field_string_length = 3;
            field_string = end;
            buffer.length = left_name_length + 4;
            break;
        case param_right_begin:
            // allocate buffer space for the name and temporal parameter (.begin)
            field_string_length = 5;
            field_string = begin;
            buffer.length = right_name_length + 6;
            break;
        case param_right_end:
            // allocate buffer space for the name and temporal parameter (.end)
            field_string_length = 3;
            field_string = end;
            buffer.length = right_name_length + 4;
            break;
        case param_strlit:
            // get the string parameter and find its length
            field_string = get_word(val_dict, input[position++].string_value);
            field_string_length = string_length(field_string, MAX_WORD_LENGTH);
            // then add 2 for the quotes
            buffer.length = field_string_length + 2;
            break;
        case param_left_field:
            // get the string parameter and find its length
            field_string = get_word(key_dict, input[position++].string_value);
            field_string_length = string_length(field_string, MAX_WORD_LENGTH);
            // then add space for the left name and a dot
            buffer.length = left_name_length + 1 + field_string_length;
            break;
        case param_right_field:
            // get the string parameter and find its length
            field_string = get_word(key_dict, input[position++].string_value);
            field_string_length = string_length(field_string, MAX_WORD_LENGTH);
            // then add space for the right name and a dot
            buffer.length = right_name_length + 1 + field_string_length;
            break;
        case param_intlit:
        case param_reallit:
            /* we don't know how long they will be, so allocate enough space */
            buffer.length = MAX_WORD_LENGTH + 1;
            break;
        case param_boollit:
            /* space for true or false */
            if (input[position++].boolean_value) {
                buffer.length = 4;
            } else {
                buffer.length = 5;
            }
            break;
        default:
            /* set the buffer length to zero for cases where we need to allocate later
             * this is just for the intlit and reallit cases, now
             */
            buffer.length = 0;
            break;
        }

        /* if we need to allocate space, try to do so */
        if (buffer.length > 0) {
            buffer.str = malloc(sizeof(char) * buffer.length);
            if (buffer.str == NULL) {
                // there was an allocation error, so break out of the loop
                break;
            }
        }

        switch(action) {
        case action_add:
            operator_char = '+';
            break;
        case action_sub:
        case action_neg:
            operator_char = '-';
            break;
        case action_mul:
            operator_char = '*';
            break;
        case action_div:
            operator_char = '/';
            break;
        case action_mod:
            operator_char = '%';
            break;
        case action_lt:
        case action_lte:
            operator_char = '<';
            break;
        case action_gt:
        case action_gte:
            operator_char = '>';
            break;
        case action_eq:
            operator_char = '=';
            break;
        case action_ne:
        case action_not:
            operator_char = '!';
            break;
        case action_and:
            operator_char = '&';
            break;
        case action_or:
            operator_char = '|';
            break;

        default:
            // do nothing...
            break;
        }

        /* write expressions to the buffer */
        switch(action) {
        case action_add:
        case action_sub:
        case action_mul:
        case action_div:
        case action_mod:
        case action_lt:
        case action_gt:
        case action_lte:
        case action_gte:
        case action_eq:
        case action_ne:
        case action_and:
        case action_or:
            /* "(%.*s %c %.*s)" */
            *buffer.str = '(';
            copy_memory(buffer.str + 1, lstring.str, lstring.length);
            *(buffer.str + 1 + lstring.length) = ' ';
            *(buffer.str + 1 + lstring.length + 1) = operator_char;
            /* for the two char operators */
            if (extra_space) {
                *(buffer.str + 1 + lstring.length + 2) = '=';
            }
            *(buffer.str + 1 + lstring.length + 2 + extra_space) = ' ';
            copy_memory(buffer.str + 1 + lstring.length + 3 + extra_space, rstring.str, rstring.length);
            *(buffer.str + 1 + lstring.length + 3 + extra_space + rstring.length) = ')';

            free(rstring.str);
            free(lstring.str);
            break;

        case action_neg:
        case action_not:
            /* "(%c %.*s)" */
            *buffer.str = '(';
            *(buffer.str + 1) = operator_char;
            *(buffer.str + 2) = ' ';
            copy_memory(buffer.str + 3, rstring.str, rstring.length);
            *(buffer.str + 3 + rstring.length) = ')';

            free(rstring.str);
            break;

        case param_left_begin:
        case param_left_end:
        case param_left_field:
            copy_memory(buffer.str, left_name, left_name_length);
            *(buffer.str + left_name_length) = '.';
            copy_memory(buffer.str + left_name_length + 1, field_string, field_string_length);
            break;

        case param_right_begin:
        case param_right_end:
        case param_right_field:
            copy_memory(buffer.str, right_name, right_name_length);
            *(buffer.str + right_name_length) = '.';
            copy_memory(buffer.str + right_name_length + 1, field_string, field_string_length);
            break;

        case param_strlit:
            *buffer.str = '"';
            copy_memory(buffer.str + 1, field_string, field_string_length);
            *(buffer.str + 1 + field_string_length) = '"';
            break;

            /* below here things get messy, since it doesn't really work to preallocate space */
        case param_boollit:
            /* it is hacky to use 4 as a proxy for true here, but it works for now */
            if (buffer.length == 4) {
                copy_memory(buffer.str, true_str, 4);

            } else {
                copy_memory(buffer.str, false_str, 5);
            }
            break;

        case param_intlit:
            snprintf(buffer.str, buffer.length, "%" PRIi64, input[position++].integer_value);
            /* now figure out how long this actually is */
            buffer.length = string_length(buffer.str, buffer.length - 1);
            break;
        case param_reallit:
            snprintf(buffer.str, buffer.length, "%f", input[position++].real_value);
            /* now figure out how long this actually is */
            buffer.length = string_length(buffer.str, buffer.length - 1);
            break;
        }

        // push the string buffer
        stack[tos].length = buffer.length;
        stack[tos++].str  = buffer.str;
    }
    // actually print out the result
    if (tos > 0) {
        tos--;
        write_msg(log_to, "%.*s", stack[tos].length, stack[tos].str);

        // make sure the stack is empty
        while (tos > 0) {
            free(stack[--tos].str);
        }
    }

    // free the stack
    free(stack);
}
#endif