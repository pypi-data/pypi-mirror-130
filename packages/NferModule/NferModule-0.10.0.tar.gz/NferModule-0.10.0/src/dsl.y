%code requires {
/*
 * dsl.y
 *
 *  Created on: Apr 20, 2017
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

#include "types.h"
#include "dict.h"
#include "log.h"
#include "ast.h"
#include "semantic.h"
}

%define api.pure full 
%define parse.error verbose
%locations
%lex-param { void * scanner } { dictionary *parser_dict }
%parse-param { void * scanner } { dictionary *parser_dict } { ast_node **ast_root }

%union {
    int64_t int_value;
    double float_value;
    word_id string_value;
    ast_node *node;
};

%code requires {
    #define YYLTYPE YYLTYPE
    typedef location_type YYLTYPE;
}

%code provides {
int yylex(YYSTYPE * yylval_param, YYLTYPE * llocp, void * yyscanner, dictionary *parser_dict);
void yyerror(YYLTYPE * yylloc, void * scanner, dictionary *parser_dict, ast_node **ast_root, const char* message);
}

%token <int_value> INTLITERAL
%token <float_value> FLOATLITERAL
%token <string_value> IDENTIFIER STRINGLITERAL
%token LPAREN RPAREN LBRACE RBRACE LISTSEP MAPSTO LABELS MODULE IMPORT WHERE MAP BEGINTOKEN ENDTOKEN FIELD YIELDS TRUE FALSE EOL

%nonassoc UNLESS
%nonassoc ALSO BEFORE MEET DURING START FINISH OVERLAP SLICE COINCIDE AFTER FOLLOW CONTAIN

%left AND OR
%left GE LE EQ NE GT LT
%left PLUS MINUS
%left MUL DIV MOD
%nonassoc UMINUS BANG

%type <node> module_list imports identifier_list rule_list rule interval_expr where_expr map_expr map_expr_list end_points expr


%%

specification:
          rule_list                { *ast_root = $1; }
        | module_list              { *ast_root = $1; }
        ;


module_list:
          MODULE IDENTIFIER LBRACE imports rule_list RBRACE              { $$ = new_module_list($2, $4, $5, NULL, &@1); }
        | MODULE IDENTIFIER LBRACE imports rule_list RBRACE module_list  { $$ = new_module_list($2, $4, $5, $7, &@1); }
        ;

imports:
          IMPORT identifier_list EOL            { $$ = $2; }
        |   /* NULL */                          { $$ = NULL; }
        ;
          
identifier_list:
          IDENTIFIER                            { $$ = new_import_list($1, NULL, &@1); }
        | IDENTIFIER LISTSEP identifier_list    { $$ = new_import_list($1, $3, &@1); }

rule_list: 
          rule rule_list                        { $$ = new_rule_list($1, $2); }
        |   /* NULL */                          { $$ = NULL; }
        ;

rule: 
          IDENTIFIER YIELDS interval_expr where_expr map_expr end_points { $$ = new_rule($1, $3, $4, $5, $6, &@1); }

where_expr:
          WHERE expr                            { $$ = $2; }
        |   /* NULL */                          { $$ = NULL; }
        ;

map_expr:
          MAP LBRACE map_expr_list RBRACE       { $$ = $3; }
        |   /* NULL */                          { $$ = NULL; }
        ;

map_expr_list:
          IDENTIFIER MAPSTO expr                        { $$ = new_map_expr_list($1, $3, NULL, &@1); }
        | IDENTIFIER MAPSTO expr LISTSEP map_expr_list  { $$ = new_map_expr_list($1, $3, $5, &@1); }
        ;

end_points:
          BEGINTOKEN expr ENDTOKEN expr         { $$ = new_end_points($2, $4, &@1); }
        |   /* NULL */                          { $$ = NULL; }
        ;

interval_expr:
          IDENTIFIER LABELS IDENTIFIER          { $$ = new_atomic_interval_expr($1, $3, &@1, &@3); }
        | IDENTIFIER                            { $$ = new_atomic_interval_expr(WORD_NOT_FOUND, $1, &@1, NULL); }
        | interval_expr ALSO     interval_expr  { $$ = new_binary_interval_expr(ALSO, false, $1, $3); }
        | interval_expr BEFORE   interval_expr  { $$ = new_binary_interval_expr(BEFORE, false, $1, $3); }
        | interval_expr MEET     interval_expr  { $$ = new_binary_interval_expr(MEET, false, $1, $3); }
        | interval_expr DURING   interval_expr  { $$ = new_binary_interval_expr(DURING, false, $1, $3); }
        | interval_expr START    interval_expr  { $$ = new_binary_interval_expr(START, false, $1, $3); }
        | interval_expr FINISH   interval_expr  { $$ = new_binary_interval_expr(FINISH, false, $1, $3); }
        | interval_expr OVERLAP  interval_expr  { $$ = new_binary_interval_expr(OVERLAP, false, $1, $3); }
        | interval_expr SLICE    interval_expr  { $$ = new_binary_interval_expr(SLICE, false, $1, $3); }
        | interval_expr COINCIDE interval_expr  { $$ = new_binary_interval_expr(COINCIDE, false, $1, $3); }
        | interval_expr UNLESS AFTER   interval_expr { $$ = new_binary_interval_expr(AFTER, true, $1, $4); }
        | interval_expr UNLESS FOLLOW  interval_expr { $$ = new_binary_interval_expr(FOLLOW, true, $1, $4);}
        | interval_expr UNLESS CONTAIN interval_expr { $$ = new_binary_interval_expr(CONTAIN, true, $1, $4);}
        | LPAREN interval_expr RPAREN           { $$ = $2; }
        ;

expr:
          INTLITERAL            { $$ = new_int_literal($1, &@1); }
        | FLOATLITERAL          { $$ = new_float_literal($1, &@1); }
        | STRINGLITERAL         { $$ = new_string_literal($1, &@1); }
        | TRUE                  { $$ = new_boolean_literal(true, &@1); }
        | FALSE                 { $$ = new_boolean_literal(false, &@1); }
        | MINUS expr %prec UMINUS { $$ = new_unary_expr(UMINUS, $2, &@1); }
        | BANG expr             { $$ = new_unary_expr(BANG, $2, &@1); }
        | expr MUL   expr       { $$ = new_binary_expr(MUL, $1, $3); }
        | expr DIV   expr       { $$ = new_binary_expr(DIV, $1, $3); }
        | expr MOD   expr       { $$ = new_binary_expr(MOD, $1, $3); }
        | expr PLUS  expr       { $$ = new_binary_expr(PLUS, $1, $3); }
        | expr MINUS expr       { $$ = new_binary_expr(MINUS, $1, $3); }
        | expr LT    expr       { $$ = new_binary_expr(LT, $1, $3); }
        | expr GT    expr       { $$ = new_binary_expr(GT, $1, $3); }
        | expr GE    expr       { $$ = new_binary_expr(GE, $1, $3); }
        | expr LE    expr       { $$ = new_binary_expr(LE, $1, $3); }
        | expr NE    expr       { $$ = new_binary_expr(NE, $1, $3); }
        | expr EQ    expr       { $$ = new_binary_expr(EQ, $1, $3); }
        | expr AND   expr       { $$ = new_binary_expr(AND, $1, $3); }
        | expr OR    expr       { $$ = new_binary_expr(OR, $1, $3); }
        | IDENTIFIER FIELD IDENTIFIER  { $$ = new_map_field($1, $3, &@1, &@3); }
        | IDENTIFIER FIELD BEGINTOKEN  { $$ = new_time_field(BEGINTOKEN, $1, &@1, &@3); }
        | IDENTIFIER FIELD ENDTOKEN    { $$ = new_time_field(ENDTOKEN, $1, &@1, &@3); }
        | LPAREN expr RPAREN           { $$ = $2; }
        ;

%%

void yyerror(YYLTYPE * yylloc, void * UNUSED(scanner), dictionary *UNUSED(parser_dict), ast_node **UNUSED(ast_root), const char *msg) {
    filter_log_msg(LOG_LEVEL_ERROR, "Parse error on lines %d:%d to %d:%d: %s\n", 
                   yylloc->first_line, yylloc->first_column, yylloc->last_line, yylloc->last_column, msg);
}


