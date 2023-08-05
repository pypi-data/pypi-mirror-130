/*
 * generate.c
 *
 *  Created on: May 15, 2017
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

#include "types.h"
#include "dict.h"
#include "log.h"
#include "map.h"
#include "nfer.h"
#include "ast.h"
#include "generate.h"
#include "expression.h"
#include "astutil.h"

#include "dsl.tab.h"

operator_code get_operator_from_token(int token) {
    switch(token) {
    case ALSO:
        return ALSO_OPERATOR;
        break;
    case BEFORE:
        return BEFORE_OPERATOR;
        break;
    case MEET:
        return MEET_OPERATOR;
        break;
    case DURING:
        return DURING_OPERATOR;
        break;
    case START:
        return START_OPERATOR;
        break;
    case FINISH:
        return FINISH_OPERATOR;
        break;
    case OVERLAP:
        return OVERLAP_OPERATOR;
        break;
    case SLICE:
        return SLICE_OPERATOR;
        break;
    case COINCIDE:
        return COINCIDE_OPERATOR;
        break;
    case AFTER:
        return AFTER_OPERATOR;
        break;
    case FOLLOW:
        return FOLLOW_OPERATOR;
        break;
    case CONTAIN:
        return CONTAIN_OPERATOR;
        break;
    }
    return ALSO_OPERATOR;
}

/**
 * Returns true if this expr_node or any of its children belong in the passed BIE node
 */
static bool belongs_in_ie(ast_node *ie_node, ast_node *expr_node) {
    if (!ie_node || !expr_node) {
        return false;
    }

    switch(expr_node->type) {
    case type_unary_expr:
        return belongs_in_ie(ie_node, expr_node->unary_expr.operand);
        break;
    case type_binary_expr:
        /* if this is a Boolean type operator, we want to recurse */
        if (expr_node->binary_expr.operator == AND || expr_node->binary_expr.operator == OR) {
            return belongs_in_ie(ie_node, expr_node->binary_expr.left) ||
                    belongs_in_ie(ie_node, expr_node->binary_expr.right);
        } else {
            /* otherwise, just check if the belongs_in interval expression matches */
            return expr_node->binary_expr.belongs_in == ie_node;
        }

        break;
    case type_map_field:
        return expr_node->map_field.interval_expression == ie_node;
        break;
    case type_time_field:
        return expr_node->time_field.interval_expression == ie_node;
        break;
    default:
        return true;
    }
}

static unsigned int generate_eval_from_expr(ast_node *ie_node, ast_node *node, expression_input *input, unsigned int input_position) {
    unsigned int added = 0;
    if (!node) {
        return 0;
    }
    switch (node->type) {
    case type_int_literal:
        input[input_position++].action = param_intlit;
        input[input_position].integer_value = node->int_literal.value;
        added = 2;
        break;
    case type_float_literal:
        input[input_position++].action = param_reallit;
        input[input_position].real_value = node->float_literal.value;
        added = 2;
        break;
    case type_string_literal:
        input[input_position++].action = param_strlit;
        input[input_position].string_value = node->string_literal.val_dict_id;
        added = 2;
        break;
    case type_boolean_literal:
        input[input_position++].action = param_boollit;
        input[input_position].boolean_value = node->boolean_literal.value;
        added = 2;
        break;
    case type_unary_expr:
        added = generate_eval_from_expr(ie_node, node->unary_expr.operand, input, input_position);
        switch(node->unary_expr.operator) {
        case UMINUS:
            input[input_position + added].action = action_neg;
            break;
        case BANG:
            input[input_position + added].action = action_not;
            break;
        }
        added++;
        break;
    case type_binary_expr:
        /**
         * An expression node may be affiliated with a BIE, multiple BIEs or it may be neutral.
         * (also, now it may be affiliated witn an AIE, but only in special circumstances).
         * For children of binary Boolean operators (&, |), the affiliation of the children determine
         * whether or not they are included in nested rules.
         *
         * If a child (left or right) is affiliated with the node or is neutral, then it is included.
         * If a child is affiliated with another BIE, then it is replaced with the appropriate Boolean so that
         * only the other side is considered in the calculation.
         * If a child is affiliated with multiple BIE, then if any of them match the current one the
         * child is included.  If none of them match, then the child is replaced with the appropriate Boolean.
         *
         * So, at generation time we need to know IF the BIE for any given sub-tree matches the current one.
         * This is inefficient to store, so we can instead just calculate it during generation.
         *
         * The pseudocode during expression generation is basically this:
         * if (binary_boolean_expression) {
         *     if (left side doesn't include any matches for this BIE) {
         *         if (&) write true
         *         if (|) write false
         *     } else {
         *         recurse down the left side
         *     }
         *     if (right side doesn't include any matches for this BIE) {
         *         if (&) write true
         *         if (|) write false
         *     } else {
         *         recurse down the right side
         *     }
         *     write the operator
         * }
         *
         * We don't need to check for neither side including matches because we won't reach this node if that
         * is the case.  We won't recurse down the tree.
         */

        // if it is a Boolean binary expression
        if (node->binary_expr.operator == AND || node->binary_expr.operator == OR) {
            filter_log_msg(LOG_LEVEL_DEBUG, "      Generate eval: found Boolean binary expr\n");
            // if the left side doesn't reference the BIE
            if (!belongs_in_ie(ie_node, node->binary_expr.left)) {
                filter_log_msg(LOG_LEVEL_DEBUG, "      Generate eval: left doesn't belong in BIE\n");
                // not referenced on the left side! so just write a Boolean
                input[input_position].action = param_boollit;

                if (node->binary_expr.operator == AND) {
                    // write true
                    input[input_position + 1].boolean_value = true;

                } else if (node->binary_expr.operator == OR) {
                    // write false
                    input[input_position + 1].boolean_value = false;
                }
                added = 2;
            } else {
                filter_log_msg(LOG_LEVEL_DEBUG, "      Generate eval: left belongs in BIE\n");
                added = generate_eval_from_expr(ie_node, node->binary_expr.left, input, input_position);
            }

            // if the right side doesn't reference the BIE
            if (!belongs_in_ie(ie_node, node->binary_expr.right)) {
                filter_log_msg(LOG_LEVEL_DEBUG, "      Generate eval: right doesn't belong in BIE\n");
                // not referenced on the right side! so just write a Boolean
                input[input_position + added].action = param_boollit;

                if (node->binary_expr.operator == AND) {
                    // write true
                    input[input_position + added + 1].boolean_value = true;

                } else if (node->binary_expr.operator == OR) {
                    // write false
                    input[input_position + added + 1].boolean_value = false;
                }
                added += 2;
            } else {
                filter_log_msg(LOG_LEVEL_DEBUG, "      Generate eval: right belongs in BIE\n");
                added += generate_eval_from_expr(ie_node, node->binary_expr.right, input, input_position + added);
            }
        } else {
            // not a Boolean binary expression
            added = generate_eval_from_expr(ie_node, node->binary_expr.left, input, input_position);
            added += generate_eval_from_expr(ie_node, node->binary_expr.right, input, input_position + added);
        }

        switch(node->binary_expr.operator) {
        case PLUS:
            input[input_position + added].action = action_add;
            break;
        case MINUS:
            input[input_position + added].action = action_sub;
            break;
        case MUL:
            input[input_position + added].action = action_mul;
            break;
        case DIV:
            input[input_position + added].action = action_div;
            break;
        case MOD:
            input[input_position + added].action = action_mod;
            break;
        case AND:
            input[input_position + added].action = action_and;
            break;
        case OR:
            input[input_position + added].action = action_or;
            break;
        case EQ:
            input[input_position + added].action = action_eq;
            break;
        case NE:
            input[input_position + added].action = action_ne;
            break;
        case GT:
            input[input_position + added].action = action_gt;
            break;
        case LT:
            input[input_position + added].action = action_lt;
            break;
        case GE:
            input[input_position + added].action = action_gte;
            break;
        case LE:
            input[input_position + added].action = action_lte;
            break;
        }
        added++;
        break;
    case type_map_field:
        switch(node->map_field.side) {
        case left_side:
            input[input_position++].action = param_left_field;
            break;
        case right_side:
            input[input_position++].action = param_right_field;
            break;
        }
        // if the referenced BIE is this BIE, then use the original, not the remapped key
        // this should be handled in semantic analysis when determining which map key to set
        input[input_position].field_name = node->map_field.resulting_map_key;

        added = 2;
        break;
    case type_time_field:
        if (node->time_field.is_time || node->time_field.interval_expression == ie_node) {
            switch(node->time_field.side) {
            case left_side:
                switch(node->time_field.time_field) {
                case BEGINTOKEN:
                    input[input_position].action = param_left_begin;
                    break;
                case ENDTOKEN:
                    input[input_position].action = param_left_end;
                    break;
                }
                break;
            case right_side:
                switch(node->time_field.time_field) {
                case BEGINTOKEN:
                    input[input_position].action = param_right_begin;
                    break;
                case ENDTOKEN:
                    input[input_position].action = param_right_end;
                    break;
                }
                break;
            }
            added = 1;
        } else {
            switch(node->time_field.side) {
            case left_side:
                input[input_position++].action = param_left_field;
                break;
            case right_side:
                input[input_position++].action = param_right_field;
                break;
            }
            input[input_position].field_name = node->time_field.resulting_map_key;
            added = 2;
        }
        break;
    default:
        added = 0;
    }
    return added;
}

static unsigned int get_eval_size(ast_node *ie_node, ast_node *node) {
    unsigned int size = 0;
    if (!node) {
        return 0;
    }
    switch (node->type) {
    case type_int_literal:
        size = 2;
        break;
    case type_float_literal:
        size = 2;
        break;
    case type_string_literal:
        size = 2;
        break;
    case type_boolean_literal:
        size = 2;
        break;
    case type_unary_expr:
        size = 1 + get_eval_size(ie_node, node->unary_expr.operand);
        break;
    case type_binary_expr:
        if (node->binary_expr.operator == AND || node->binary_expr.operator == OR) {
            // if the left side doesn't reference the BIE
            if (!belongs_in_ie(ie_node, node->binary_expr.left)) {
                // not referenced on the left side!
                size = 2;
            } else {
                size = get_eval_size(ie_node, node->binary_expr.left);
            }

            // if the right side doesn't reference the BIE
            if (!belongs_in_ie(ie_node, node->binary_expr.right)) {
                // not referenced on the right side!
                size += 2;
            } else {
                size += get_eval_size(ie_node, node->binary_expr.right);
            }
        } else {
            // not a Boolean binary expression
            size = get_eval_size(ie_node, node->binary_expr.left);
            size += get_eval_size(ie_node, node->binary_expr.right);
        }
        size += 1;
        break;
    case type_map_field:
        size = 2;
        break;
    case type_time_field:
        // time field might become a map field if it is referring to a nested rule
        if (node->time_field.is_time) {
            size = 1;
        } else {
            size = 2;
        }
        break;
    default:
        size = 0;
        break;
    }
    return size;
}

static expression_input * generate_eval_from_map_field(ast_node *ie_node, map_value *field, side_enum side) {
    expression_input *expr = NULL;
    int size;
    ast_node *node;

    if (field->type == string_type) {
        initialize_expression_input(&expr, 3);
        expr[0].length = 3;
        switch(side) {
        case left_side:
            expr[1].action = param_left_field;
            break;
        case right_side:
            expr[1].action = param_right_field;
            break;
        }
        expr[2].string_value = field->value.string;
    } else if (field->type == pointer_type) {
        node = (ast_node *)field->value.pointer;
        size = 1 + get_eval_size(ie_node, node);
        initialize_expression_input(&expr, size);
        expr[0].length = size;
        generate_eval_from_expr(ie_node, node, expr, 1);
    } else if (field->type == boolean_type) {
        initialize_expression_input(&expr, 3);
        expr[0].length = 3;
        expr[1].action = param_boollit;
        expr[2].boolean_value = field->value.boolean;
    }

    return expr;
}

static void generate_evals_from_time_maps(data_map *map, word_id left_begin, word_id left_end, word_id right_begin, word_id right_end) {
    map_value value;
    expression_input *expression;

    value.type = pointer_type;
    if (left_begin != WORD_NOT_FOUND) {
        initialize_expression_input(&expression, 2);
        expression[0].length = 2;
        expression[1].action = param_left_begin;
        value.value.pointer = expression;
        map_set(map, left_begin, &value);
    }
    if (left_end != WORD_NOT_FOUND) {
        initialize_expression_input(&expression, 2);
        expression[0].length = 2;
        expression[1].action = param_left_end;
        value.value.pointer = expression;
        map_set(map, left_end, &value);
    }
    if (right_begin != WORD_NOT_FOUND) {
        initialize_expression_input(&expression, 2);
        expression[0].length = 2;
        expression[1].action = param_right_begin;
        value.value.pointer = expression;
        map_set(map, right_begin, &value);
    }
    if (right_end != WORD_NOT_FOUND) {
        initialize_expression_input(&expression, 2);
        expression[0].length = 2;
        expression[1].action = param_right_end;
        value.value.pointer = expression;
        map_set(map, right_end, &value);
    }
}

static nfer_rule * generate_each_rule(ast_node *node, nfer_specification *spec, word_id result, ast_node *where_node) {
    nfer_rule *rule;
    map_iterator mit;
    map_key key;
    map_value value, expression;
    int size;

    if (!node) {
        rule = NULL;
    } else {
        switch (node->type) {
        case type_atomic_interval_expr:
            // check to see if we have to generate a nested atomic rule
            if (node->atomic_interval_expr.separate) {
                // there's no nesting below this, so don't worry about that
                rule = add_rule_to_specification(spec, result, node->atomic_interval_expr.result_id, ALSO_OPERATOR, WORD_NOT_FOUND, NULL);
                // always hidden!
                rule->hidden = true;
                initialize_map(&rule->map_expressions);

                if (where_node) {
                    if (belongs_in_ie(node, where_node)) {
                        size = 1 + get_eval_size(node, where_node);
                        initialize_expression_input(&rule->where_expression, size);
                        rule->where_expression[0].length = size;
                        filter_log_msg(LOG_LEVEL_DEBUG, "    Generating eval for AIE where clause, eval size is %d\n", size);
                        generate_eval_from_expr(node, where_node, rule->where_expression, 1);
                    }
                }
                get_map_iterator(&node->atomic_interval_expr.field_map, &mit);
                while (has_next_map_key(&mit)) {
                    key = next_map_key(&mit);
                    map_get(&node->atomic_interval_expr.field_map, key, &value);

                    expression.type = pointer_type;
                    expression.value.pointer = generate_eval_from_map_field(node, &value, left_side);
                    map_set(&rule->map_expressions, key, &expression);
                }
                generate_evals_from_time_maps(&rule->map_expressions, node->atomic_interval_expr.begin_map, node->atomic_interval_expr.end_map,
                    WORD_NOT_FOUND, WORD_NOT_FOUND);
            } else {
                rule = NULL;
            }
            break;
        case type_binary_interval_expr:
            generate_each_rule(node->binary_interval_expr.left, spec, node->binary_interval_expr.left_name, where_node);
            generate_each_rule(node->binary_interval_expr.right, spec, node->binary_interval_expr.right_name, where_node);

            rule = add_rule_to_specification(spec, result, node->binary_interval_expr.left_name,
                        get_operator_from_token(node->binary_interval_expr.interval_op),
                        node->binary_interval_expr.right_name, NULL);
            // default to hidden, but the top level rule will set this back to false
            rule->hidden = true;
            initialize_map(&rule->map_expressions);

            if (where_node) {
                // verify that there is anything in the where expression that should occur in this rule
                if (belongs_in_ie(node, where_node)) {
                    size = 1 + get_eval_size(node, where_node);
                    initialize_expression_input(&rule->where_expression, size);
                    rule->where_expression[0].length = size;
                    filter_log_msg(LOG_LEVEL_DEBUG, "    Generating eval for BIE where clause, eval size is %d\n", size);
                    generate_eval_from_expr(node, where_node, rule->where_expression, 1);
                }
            }
            get_map_iterator(&node->binary_interval_expr.left_field_map, &mit);
            while (has_next_map_key(&mit)) {
                key = next_map_key(&mit);
                map_get(&node->binary_interval_expr.left_field_map, key, &value);

                expression.type = pointer_type;
                expression.value.pointer = generate_eval_from_map_field(node, &value, left_side);
                map_set(&rule->map_expressions, key, &expression);
            }
            get_map_iterator(&node->binary_interval_expr.right_field_map, &mit);
            while (has_next_map_key(&mit)) {
                key = next_map_key(&mit);
                map_get(&node->binary_interval_expr.right_field_map, key, &value);

                expression.type = pointer_type;
                expression.value.pointer = generate_eval_from_map_field(node, &value, right_side);
                map_set(&rule->map_expressions, key, &expression);
            }
            generate_evals_from_time_maps(&rule->map_expressions, node->binary_interval_expr.left_begin_map, node->binary_interval_expr.left_end_map,
                    node->binary_interval_expr.right_begin_map, node->binary_interval_expr.right_end_map);

            break;
        default:
            rule = NULL;
        }
    }
    return rule;
}

static void generate_eval_from_map_expr_list(ast_node *ie_node, ast_node *map_expr_list, data_map *map) {
    expression_input *expression;
    map_value value;
    int size;
    if (!map_expr_list) {
        return;
    }

    size = 1 + get_eval_size(ie_node, map_expr_list->map_expr_list.map_expr);
    initialize_expression_input(&expression, size);
    expression[0].length = size;
    generate_eval_from_expr(ie_node, map_expr_list->map_expr_list.map_expr, expression, 1);
    value.type = pointer_type;
    value.value.pointer = expression;
    map_set(map, map_expr_list->map_expr_list.resulting_map_key, &value);

    generate_eval_from_map_expr_list(ie_node, map_expr_list->map_expr_list.tail, map);
}

bool in_imports(ast_node *imports, word_id name) {
    if (!imports) {
        return false;
    }
    if (imports->import_list.import == name) {
        return true;
    } else {
        return in_imports(imports->import_list.tail, name);
    }
}

static void generate_rules(ast_node *node, nfer_specification *spec, bool first, ast_node *imports) {
    nfer_rule *rule;
    int size;

    if (!node) {
        return;
    }
    switch (node->type) {
    case type_rule:
        rule = generate_each_rule(node->rule.interval_expr, spec, node->rule.result_id, node->rule.where_expr);
        if (!rule) {
            // the rule is atomic, we need to generate it here
            rule = add_rule_to_specification(spec, node->rule.result_id, node->rule.interval_expr->atomic_interval_expr.result_id,
                        ALSO_OPERATOR, WORD_NOT_FOUND, NULL);

            if (node->rule.where_expr) {
                size = 1 + get_eval_size(node->rule.interval_expr, node->rule.where_expr);
                initialize_expression_input(&rule->where_expression, size);
                rule->where_expression[0].length = size;
                filter_log_msg(LOG_LEVEL_DEBUG, "    Generating eval for atomic rule where clause, eval size is %d\n", size);
                generate_eval_from_expr(node->rule.interval_expr, node->rule.where_expr, rule->where_expression, 1);
            }
        }

        // make sure this is not a hidden rule
        rule->hidden = false;
        if (node->rule.end_points) {
            size = 1 + get_eval_size(node->rule.interval_expr, node->rule.end_points->end_points.begin_expr);
            initialize_expression_input(&rule->begin_expression, size);
            rule->begin_expression[0].length = size;
            generate_eval_from_expr(node->rule.interval_expr, node->rule.end_points->end_points.begin_expr, rule->begin_expression, 1);

            size = 1 + get_eval_size(node->rule.interval_expr, node->rule.end_points->end_points.end_expr);
            initialize_expression_input(&rule->end_expression, size);
            rule->end_expression[0].length = size;
            generate_eval_from_expr(node->rule.interval_expr, node->rule.end_points->end_points.end_expr, rule->end_expression, 1);
        }
        if (node->rule.map_expr_list) {
            generate_eval_from_map_expr_list(node->rule.interval_expr, node->rule.map_expr_list, &rule->map_expressions);
        }


        break;
    case type_rule_list:
        generate_rules(node->rule_list.head, spec, false, imports);
        generate_rules(node->rule_list.tail, spec, false, imports);
        break;
    case type_module_list:

        if (first) {
            generate_rules(node->module_list.rules, spec, true, node->module_list.imports);
            generate_rules(node->module_list.tail, spec, false, node->module_list.imports);
        } else {
            if (in_imports(imports, node->module_list.id)) {
                generate_rules(node->module_list.rules, spec, false, node->module_list.imports);
            } else {
                filter_log_msg(LOG_LEVEL_DEBUG, "Ignoring non-imported module %d\n", node->module_list.id);
            }
            generate_rules(node->module_list.tail, spec, false, imports);
        }

        break;
    default:
        return;
    }
}

void generate_specification(ast_node *node, nfer_specification *spec) {
    generate_rules(node, spec, true, NULL);
}


