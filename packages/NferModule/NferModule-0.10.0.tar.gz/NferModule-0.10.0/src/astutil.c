/*
 * astutil.c
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
#include <inttypes.h>

#include "types.h"
#include "dict.h"
#include "log.h"
#include "ast.h"

#include "dsl.tab.h"

void log_ast(ast_node *node, dictionary *parser_dict) {
    if (!node) {
        return;
    }
    switch (node->type) {
    case type_int_literal:
        log_msg("%" PRIi64, node->int_literal.value);
        break;
    case type_float_literal:
        log_msg("%f", node->float_literal.value);
        break;
    case type_string_literal:
        log_msg("\"%s\"", get_word(parser_dict, node->string_literal.id));
        break;
    case type_boolean_literal:
        if (node->boolean_literal.value) {
            log_msg("TRUE");
        } else {
            log_msg("FALSE");
        }
        break;
    case type_unary_expr:
        switch (node->unary_expr.operator) {
        case UMINUS:
            log_msg(" -(");
            break;
        case BANG:
            log_msg(" !(");
            break;
        }
        log_ast(node->unary_expr.operand, parser_dict);
        log_msg(")");
        break;
    case type_binary_expr:
        log_msg("(");
        log_ast(node->binary_expr.left, parser_dict);
        switch (node->binary_expr.operator) {
        case PLUS:
            log_msg(" + ");
            break;
        case MINUS:
            log_msg(" - ");
            break;
        case MUL:
            log_msg(" * ");
            break;
        case DIV:
            log_msg(" / ");
            break;
        case MOD:
            log_msg(" %c ", '%');
            break;
        case AND:
            log_msg(" & ");
            break;
        case OR:
            log_msg(" | ");
            break;
        case EQ:
            log_msg(" = ");
            break;
        case NE:
            log_msg(" != ");
            break;
        case GT:
            log_msg(" > ");
            break;
        case LT:
            log_msg(" < ");
            break;
        case GE:
            log_msg(" >= ");
            break;
        case LE:
            log_msg(" <= ");
            break;
        }
        log_ast(node->binary_expr.right, parser_dict);
        log_msg(")");
        break;
    case type_map_field:
        log_msg("%s.%s", get_word(parser_dict, node->map_field.label), get_word(parser_dict, node->map_field.map_key));
        break;
    case type_time_field:
        log_msg("%s.", get_word(parser_dict, node->time_field.label));
        switch (node->time_field.time_field) {
        case BEGINTOKEN:
            log_msg("BEGIN");
            break;
        case ENDTOKEN:
            log_msg("END");
            break;
        }
        break;
    case type_atomic_interval_expr:
        if(node->atomic_interval_expr.label != WORD_NOT_FOUND) {
            log_msg("%s:", get_word(parser_dict, node->atomic_interval_expr.label));
        }
        log_msg("%s", get_word(parser_dict, node->atomic_interval_expr.id));
        break;
    case type_binary_interval_expr:
        log_msg("(");
        log_ast(node->binary_interval_expr.left, parser_dict);
        if (node->binary_interval_expr.exclusion) {
            log_msg(" UNLESS");
        }
        switch(node->binary_interval_expr.interval_op) {
        case ALSO:
            log_msg(" ALSO ");
            break;
        case BEFORE:
            log_msg(" BEFORE ");
            break;
        case MEET:
            log_msg(" MEET ");
            break;
        case DURING:
            log_msg(" DURING ");
            break;
        case START:
            log_msg(" START ");
            break;
        case FINISH:
            log_msg(" FINISH ");
            break;
        case OVERLAP:
            log_msg(" OVERLAP ");
            break;
        case SLICE:
            log_msg(" SLICE ");
            break;
        case COINCIDE:
            log_msg(" COINCIDE ");
            break;
        case AFTER:
            log_msg(" AFTER ");
            break;
        case FOLLOW:
            log_msg(" FOLLOW ");
            break;
        case CONTAIN:
            log_msg(" CONTAIN ");
            break;
        default:
            log_msg(" unknown(%d) ", node->binary_interval_expr.interval_op);
        }
        log_ast(node->binary_interval_expr.right, parser_dict);
        log_msg(")");
        break;
    case type_map_expr_list:
        log_msg("%s -> ", get_word(parser_dict, node->map_expr_list.map_key));
        log_ast(node->map_expr_list.map_expr, parser_dict);
        if (node->map_expr_list.tail) {
            log_msg(", ");
            log_ast(node->map_expr_list.tail, parser_dict);
        }
        break;
    case type_end_points:
        log_msg(" begin ");
        log_ast(node->end_points.begin_expr, parser_dict);
        log_msg(" end ");
        log_ast(node->end_points.end_expr, parser_dict);
        break;
    case type_rule:
        log_msg("%s :- ", get_word(parser_dict, node->rule.id));
        log_ast(node->rule.interval_expr, parser_dict);
        if (node->rule.where_expr) {
            log_msg(" where ");
            log_ast(node->rule.where_expr, parser_dict);
        }
        if (node->rule.map_expr_list) {
            log_msg(" map {");
            log_ast(node->rule.map_expr_list, parser_dict);
            log_msg("}");
        }
        if (node->rule.end_points) {
            log_ast(node->rule.end_points, parser_dict);
        }
        break;
    case type_rule_list:
        log_ast(node->rule_list.head, parser_dict);
        if (node->rule_list.tail) {
            log_msg("\n");
            log_ast(node->rule_list.tail, parser_dict);
        }
        break;
    case type_module_list:
        log_msg("module %s {\n", get_word(parser_dict, node->module_list.id));
        if (node->module_list.imports) {
            log_msg("import ");
            log_ast(node->module_list.imports, parser_dict);
            log_msg(";\n");
        }
        log_ast(node->module_list.rules, parser_dict);
        log_msg("\n}\n");
        log_ast(node->module_list.tail, parser_dict);
        break;
    case type_import_list:
        log_msg(get_word(parser_dict, node->import_list.import));
        if (node->import_list.tail) {
            log_msg(", ");
            log_ast(node->import_list.tail, parser_dict);
        }
        break;
    }
}

static word_id create_node(dictionary *dict, const char *type, ast_node *node) {
    char word[MAX_WORD_LENGTH + 1];

    sprintf(word, "%s%p", type, (void *)node);
    return add_word(dict, word);
}

static word_id write_nodes(FILE *dotfile, ast_node *node, dictionary *parser_dict, dictionary *dot_dict) {
    word_id node_id, child_id;
    ast_node *child_node;
    bool is_bie;
    if (!node) {
        return WORD_NOT_FOUND;
    }

    switch(node->type) {
    case type_int_literal:
        node_id = create_node(dot_dict, "IntLiteral", node);
        fprintf(dotfile, "%s [label=\"%" PRIi64 "\"];\n", get_word(dot_dict, node_id), node->int_literal.value);
        return node_id;
        break;
    case type_float_literal:
        node_id = create_node(dot_dict, "FloatLiteral", node);
        fprintf(dotfile, "%s [label=\"%f\"];\n", get_word(dot_dict, node_id), node->float_literal.value);
        return node_id;
        break;
    case type_string_literal:
        node_id = create_node(dot_dict, "StringLiteral", node);
        fprintf(dotfile, "%s [label=\"\\\"%s\\\"\"];\n", get_word(dot_dict, node_id), get_word(parser_dict, node->string_literal.id));
        return node_id;
        break;
    case type_boolean_literal:
        node_id = create_node(dot_dict, "BooleanLiteral", node);
        fprintf(dotfile, "%s [label=\"%s\"];\n", get_word(dot_dict, node_id), (node->boolean_literal.value ? "TRUE" : "FALSE"));
        return node_id;
        break;
    case type_unary_expr:
        node_id = create_node(dot_dict, "UnaryExpr", node);
        fprintf(dotfile, "%s [label=\"", get_word(dot_dict, node_id));
        switch (node->unary_expr.operator) {
        case UMINUS:
            fprintf(dotfile, "-");
            break;
        case BANG:
            fprintf(dotfile, "!");
            break;
        }
        fprintf(dotfile, "\"];\n");

        child_id = write_nodes(dotfile, node->unary_expr.operand, parser_dict, dot_dict);
        fprintf(dotfile, "%s -> %s;\n", get_word(dot_dict, node_id), get_word(dot_dict, child_id));
        return node_id;
        break;
    case type_binary_expr:
        node_id = create_node(dot_dict, "BinaryExpr", node);
        fprintf(dotfile, "%s [label=\"<l> left | ", get_word(dot_dict, node_id));

        switch (node->binary_expr.operator) {
        case PLUS:
            fprintf(dotfile, " + ");
            break;
        case MINUS:
            fprintf(dotfile, " - ");
            break;
        case MUL:
            fprintf(dotfile, " * ");
            break;
        case DIV:
            fprintf(dotfile, " / ");
            break;
        case MOD:
            fprintf(dotfile, " %c ", '%');
            break;
        case AND:
            fprintf(dotfile, " & ");
            break;
        case OR:
            fprintf(dotfile, " I "); // this is a dumb hack
            break;
        case EQ:
            fprintf(dotfile, " = ");
            break;
        case NE:
            fprintf(dotfile, " != ");
            break;
        case GT:
            fprintf(dotfile, " &gt; ");
            break;
        case LT:
            fprintf(dotfile, " &lt; ");
            break;
        case GE:
            fprintf(dotfile, " >= ");
            break;
        case LE:
            fprintf(dotfile, " <= ");
            break;
        }
        fprintf(dotfile, "| <r> right\"];\n");

        child_id = write_nodes(dotfile, node->binary_expr.left, parser_dict, dot_dict);
        fprintf(dotfile, "%s:l -> %s;\n", get_word(dot_dict, node_id), get_word(dot_dict, child_id));
        child_id = write_nodes(dotfile, node->binary_expr.right, parser_dict, dot_dict);
        fprintf(dotfile, "%s:r -> %s;\n", get_word(dot_dict, node_id), get_word(dot_dict, child_id));
        // write a dotted line to the associated binary interval expression
        if (node->binary_expr.belongs_in != NULL) {
            fprintf(dotfile, "%s -> %s%p [style=dotted];\n", get_word(dot_dict, node_id), "BinaryIntervalExpr", (void *)node->binary_expr.belongs_in);
        }
        return node_id;
        break;
    case type_map_field:
        node_id = create_node(dot_dict, "MapField", node);
        // write the node
        fprintf(dotfile, "%s [label=\"%s.%s\"];\n", get_word(dot_dict, node_id), get_word(parser_dict, node->map_field.label), get_word(parser_dict, node->map_field.map_key));
        // write a dashed line to the referred-to binary interval expression
        if (node->map_field.interval_expression != NULL) {
            is_bie = node->map_field.interval_expression->type == type_binary_interval_expr;
            fprintf(dotfile, "%s -> %s%p", get_word(dot_dict, node_id), is_bie ? "BinaryIntervalExpr" : "AtomicIntervalExpr", (void *)node->map_field.interval_expression);
            if (is_bie) {
                switch (node->map_field.side) {
                case left_side:
                    fprintf(dotfile, ":l");
                    break;
                case right_side:
                    fprintf(dotfile, ":r");
                    break;
                }
            }
            fprintf(dotfile, " [style=dashed];\n");
        }
        return node_id;
        break;
    case type_time_field:
        node_id = create_node(dot_dict, "MapField", node);
        // write the node
        fprintf(dotfile, "%s [label=\"%s.", get_word(dot_dict, node_id), get_word(parser_dict, node->time_field.label));
        switch (node->time_field.time_field) {
        case BEGINTOKEN:
            fprintf(dotfile, "BEGIN");
            break;
        case ENDTOKEN:
            fprintf(dotfile, "END");
            break;
        }
        fprintf(dotfile, "\"];\n");
        // write a dashed line to the referred-to binary interval expression
        if (node->time_field.interval_expression != NULL) {
            is_bie = node->time_field.interval_expression->type == type_binary_interval_expr;
            fprintf(dotfile, "%s -> %s%p", get_word(dot_dict, node_id), is_bie ? "BinaryIntervalExpr" : "AtomicIntervalExpr", (void *)node->time_field.interval_expression);
            if (is_bie) {
                switch (node->time_field.side) {
                case left_side:
                    fprintf(dotfile, ":l");
                    break;
                case right_side:
                    fprintf(dotfile, ":r");
                    break;
                }
            }
            fprintf(dotfile, " [style=dashed];\n");
        }
        return node_id;
        break;
    case type_atomic_interval_expr:
        node_id = create_node(dot_dict, "AtomicIntervalExpr", node);
        fprintf(dotfile, "%s [label=\"", get_word(dot_dict, node_id));
        if(node->atomic_interval_expr.label != WORD_NOT_FOUND) {
            fprintf(dotfile, "%s:", get_word(parser_dict, node->atomic_interval_expr.label));
        }
        fprintf(dotfile, "%s\"];\n", get_word(parser_dict, node->atomic_interval_expr.id));
        return node_id;
        break;
    case type_binary_interval_expr:
        node_id = create_node(dot_dict, "BinaryIntervalExpr", node);
        fprintf(dotfile, "%s [label=\"<l> left | <op> ", get_word(dot_dict, node_id));

        if (node->binary_interval_expr.exclusion) {
            fprintf(dotfile, " UNLESS");
        }
        switch(node->binary_interval_expr.interval_op) {
        case ALSO:
            fprintf(dotfile, " ALSO ");
            break;
        case BEFORE:
            fprintf(dotfile, " BEFORE ");
            break;
        case MEET:
            fprintf(dotfile, " MEET ");
            break;
        case DURING:
            fprintf(dotfile, " DURING ");
            break;
        case START:
            fprintf(dotfile, " START ");
            break;
        case FINISH:
            fprintf(dotfile, " FINISH ");
            break;
        case OVERLAP:
            fprintf(dotfile, " OVERLAP ");
            break;
        case SLICE:
            fprintf(dotfile, " SLICE ");
            break;
        case COINCIDE:
            fprintf(dotfile, " COINCIDE ");
            break;
        case AFTER:
            fprintf(dotfile, " AFTER ");
            break;
        case FOLLOW:
            fprintf(dotfile, " FOLLOW ");
            break;
        case CONTAIN:
            fprintf(dotfile, " CONTAIN ");
            break;
        default:
            fprintf(dotfile, " unknown(%d) ", node->binary_interval_expr.interval_op);
        }
        fprintf(dotfile, "| <r> right\"];\n");

        child_id = write_nodes(dotfile, node->binary_interval_expr.left, parser_dict, dot_dict);
        fprintf(dotfile, "%s:l -> %s\n", get_word(dot_dict, node_id), get_word(dot_dict, child_id));
        if (node->binary_interval_expr.right) {
            child_id = write_nodes(dotfile, node->binary_interval_expr.right, parser_dict, dot_dict);
            fprintf(dotfile, "%s:r -> %s\n", get_word(dot_dict, node_id), get_word(dot_dict, child_id));
        }

        return node_id;
        break;
    case type_map_expr_list:
        node_id = create_node(dot_dict, "MapExprList", node);
        fprintf(dotfile, "%s [label=\"{ ", get_word(dot_dict, node_id));
        // iterate instead of recurse over the list
        child_node = node;
        while (child_node) {
            // print the map keys
            fprintf(dotfile, "<m%d> %s", child_node->map_expr_list.map_key, get_word(parser_dict, child_node->map_expr_list.map_key));

            child_node = child_node->map_expr_list.tail;
            if (child_node) {
                fprintf(dotfile, " | ");
            }
        }
        fprintf(dotfile, " }\"];\n");
        // now print the expressions and edges
        child_node = node;
        while (child_node) {
            // print the map keys
            child_id = write_nodes(dotfile, child_node->map_expr_list.map_expr, parser_dict, dot_dict);
            fprintf(dotfile, "%s:m%d -> %s;\n", get_word(dot_dict, node_id), child_node->map_expr_list.map_key, get_word(dot_dict, child_id));

            child_node = child_node->map_expr_list.tail;
        }
        // this actually just prints the expressions and edges
        return node_id;
        break;
    case type_end_points:
        node_id = create_node(dot_dict, "Rule", node);
        fprintf(dotfile, "%s [label=\"<b> begin | <e> end\"];\n", get_word(dot_dict, node_id));
        child_id = write_nodes(dotfile, node->end_points.begin_expr, parser_dict, dot_dict);
        fprintf(dotfile, "%s:b -> %s\n", get_word(dot_dict, node_id), get_word(dot_dict, child_id));
        child_id = write_nodes(dotfile, node->end_points.end_expr, parser_dict, dot_dict);
        fprintf(dotfile, "%s:e -> %s\n", get_word(dot_dict, node_id), get_word(dot_dict, child_id));
        return node_id;
        break;
    case type_rule:
        node_id = create_node(dot_dict, "Rule", node);
        fprintf(dotfile, "%s [label=\"{ { <r> %s | <ie> iexpr } | ", get_word(dot_dict, node_id), get_word(parser_dict, node->rule.id));
        fprintf(dotfile, "{ <w> where | <m> map | <e> ends } }\"];\n");
        child_id = write_nodes(dotfile, node->rule.interval_expr, parser_dict, dot_dict);
        fprintf(dotfile, "%s:ie -> %s\n", get_word(dot_dict, node_id), get_word(dot_dict, child_id));
        if (node->rule.where_expr) {
            child_id = write_nodes(dotfile, node->rule.where_expr, parser_dict, dot_dict);
            fprintf(dotfile, "%s:w -> %s\n", get_word(dot_dict, node_id), get_word(dot_dict, child_id));
        }
        if (node->rule.map_expr_list) {
            child_id = write_nodes(dotfile, node->rule.map_expr_list, parser_dict, dot_dict);
            fprintf(dotfile, "%s:m -> %s\n", get_word(dot_dict, node_id), get_word(dot_dict, child_id));
        }
        if (node->rule.end_points) {
            child_id = write_nodes(dotfile, node->rule.end_points, parser_dict, dot_dict);
            fprintf(dotfile, "%s:e -> %s\n", get_word(dot_dict, node_id), get_word(dot_dict, child_id));
        }
        return node_id;
        break;
    case type_rule_list:
        write_nodes(dotfile, node->rule_list.head, parser_dict, dot_dict);
        write_nodes(dotfile, node->rule_list.tail, parser_dict, dot_dict);

        break;
    case type_module_list:
        // this should really be an error
        break;
    case type_import_list:
        fprintf(dotfile, "<i%d> %s", node->import_list.import, get_word(parser_dict, node->import_list.import));
        if (node->import_list.tail) {
            fprintf(dotfile, " | ");
            write_nodes(dotfile, node->import_list.tail, parser_dict, dot_dict);
        }
        break;
    }
    return WORD_NOT_FOUND;
}

void write_ast_graph(ast_node *node, dictionary *dict) {
    // make it big enough to add a .dot on the end
    char filename[MAX_WORD_LENGTH + 5];
    FILE *dotfile;
    dictionary dot_dict;

    if (!node) {
        return;
    }
    switch (node->type) {
    case type_module_list:
        // open a file to write the module to and call the write_nodes function, then recurse on other modules
        sprintf(filename, "%s.dot", get_word(dict, node->module_list.id));
        dotfile = fopen(filename, "w");
        initialize_dictionary(&dot_dict);
        fprintf(dotfile, "digraph \"%s\" {\n  node [shape=record]\n", get_word(dict, node->module_list.id));
        if (node->module_list.imports) {
            fprintf(dotfile, "Imports [label=\"{ Imports | {");
            write_nodes(dotfile, node->module_list.imports, dict, &dot_dict);
            fprintf(dotfile, "} }\"];\n");
        }
        write_nodes(dotfile, node->module_list.rules, dict, &dot_dict);
        fprintf(dotfile, "}\n");
        destroy_dictionary(&dot_dict);
        fclose(dotfile);
        write_ast_graph(node->module_list.tail, dict);
        break;
    case type_rule_list:
        // open a single file and call the write_nodes function
        dotfile = fopen("rules.dot", "w");
        initialize_dictionary(&dot_dict);
        fprintf(dotfile, "digraph \"rules\" {\n  node [shape=record]\n");
        write_nodes(dotfile, node, dict, &dot_dict);
        fprintf(dotfile, "}\n");
        destroy_dictionary(&dot_dict);
        fclose(dotfile);
        break;
    default:
        return;
    }
}
