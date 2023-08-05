%{
/*
 * dsl.l
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
#include "strings.h"

#include "ast.h"
#include "semantic.h"
#include "generate.h"
#include "astutil.h"
#include "log.h"
#include "dsl.h"
#include "nfer.h"
#include "dsl.tab.h"

/* fileno is hidden in c11 compliance mode, so declare it here */
#ifndef fileno
int fileno(FILE *stream);
#endif

void yyerror(YYLTYPE * yylloc, void * scanner, dictionary *parser_dict, ast_node **, const char *);

#define YY_DECL int yylex(YYSTYPE * yylval_param, YYLTYPE * llocp, yyscan_t yyscanner, dictionary *parser_dict)

#define YY_USER_ACTION { \
    llocp->first_line = yylineno;                                  \
    llocp->first_column = yyget_column(yyscanner) + 1;             \
    yyset_column(yyget_column(yyscanner) + yyget_leng(yyscanner), yyscanner); \
    llocp->last_column = yyget_column(yyscanner) + 1;              \
    llocp->last_line = yylineno;                                   \
}

#ifdef RPACKAGE
void NORETURN Rf_error(const char *, ...);
void Rprintf(const char *, ...);
#define YY_FATAL_ERROR(msg) Rf_error( msg )
#define ECHO Rprintf(yytext)
#endif

%}

ASC     [\x00-\x7f]
ASCN    [\x00-\t\v-\x7f]
U       [\x80-\xbf]
U1      [\x80-\x8f]
U2      [\xc2-\xdf]
U3      [\xe0-\xef]
U4      [\xf0-\xf7]

UANY    {ASC}|{U2}{U}|{U3}{U}{U}|{U4}{U1}{U}{U}
UANYN   {ASCN}|{U2}{U}|{U3}{U}{U}|{U4}{U1}{U}{U} 
UONLY   {U2}{U}|{U3}{U}{U}|{U4}{U1}{U}{U}

%option reentrant bison-bridge yylineno nodefault noyywrap nounput noinput
%x BLOCK_COMMENT

%%

"module"        return MODULE;
"import"        return IMPORT;
"where"         return WHERE;
"map"           return MAP;
"begin"         return BEGINTOKEN;
"end"           return ENDTOKEN;
"true"          return TRUE;
"false"         return FALSE;
"unless"        return UNLESS;

"also"          return ALSO;
"before"        return BEFORE;
"meet"          return MEET;
"during"        return DURING;
"start"         return START;
"finish"        return FINISH;
"overlap"       return OVERLAP;
"slice"         return SLICE;
"coincide"      return COINCIDE;
"after"         return AFTER;
"follow"        return FOLLOW;
"contain"       return CONTAIN;

([a-zA-Z_]|{UONLY})([a-zA-Z0-9_-]|{UONLY})*   { 
                             yylval->string_value = add_word(parser_dict, yytext);
                             return IDENTIFIER;
                        }

0           {
                 yylval->int_value = 0;
                 return INTLITERAL;
            }

[1-9][0-9]* {
                 yylval->int_value = string_to_i64(yytext, yyleng);
                 return INTLITERAL;
            }

[0-9]+"."[0-9]+  {
                      yylval->float_value = string_to_double(yytext, yyleng);
                      return FLOATLITERAL;
                 }

\"([^\"])*\"     {
                      /* strip the quotes */
                      yytext[yyleng - 1] = 0;
                      yylval->string_value = add_word(parser_dict, yytext + 1);
                  	  return STRINGLITERAL;
                 }

">="            return GE;
"<="            return LE;
"="             return EQ;
"!="            return NE;
">"             return GT;
"<"             return LT;
"+"             return PLUS;
"-"             return MINUS;
"*"             return MUL;
"/"             return DIV;
"%"             return MOD;
"!"             return BANG;
"&"             return AND;
"|"             return OR;

"("             return LPAREN;
")"             return RPAREN;
"{"             return LBRACE;
"}"             return RBRACE;
","             return LISTSEP;
"->"            return MAPSTO;
":"             return LABELS;
"."             return FIELD;
":-"            return YIELDS;
";"             return EOL;

[ \t\n]+             ;       /* ignore whitespace */
"//".*               ;       /* ignore C-style comments */
"/*"                 BEGIN(BLOCK_COMMENT);
<BLOCK_COMMENT>"*/"  BEGIN(INITIAL);
<BLOCK_COMMENT>\n    ;
<BLOCK_COMMENT>.     ;

.               yyerror(llocp, yyscanner, parser_dict, NULL, "Unknown character");
%%

static bool read_specification(const char *string, 
                        nfer_specification *spec, 
                        dictionary *name_dict, 
                        dictionary *key_dict, 
                        dictionary *val_dict,
                        bool is_file) {
    dictionary parser_dict, label_dict;
    ast_node *root = NULL;
    yyscan_t scanner;
    int parse_result;
    bool success = true;
    FILE *specfile;
    
    filter_log_msg(LOG_LEVEL_DEBUG, "Loading specification\n");
    initialize_dictionary(&parser_dict);
    initialize_dictionary(&label_dict);

    yylex_init(&scanner);
    
    if (is_file) {
        specfile = fopen(string, "r");
        if (specfile == NULL) {
            // failed to open the file
            yylex_destroy(scanner);
            return false;
        }
        yyset_in(specfile, scanner);
    } else {
        yy_scan_string(string, scanner); 
    }
    
    filter_log_msg(LOG_LEVEL_DEBUG, "  Parsing\n");
    parse_result = yyparse(scanner, &parser_dict, &root);
    
    if (is_file) {
        fclose(specfile);
    }
    
    if (parse_result == 0 && root != NULL) {
        if (should_log(LOG_LEVEL_DEBUG)) {
            log_ast(root, &parser_dict);
            log_msg("\n");
        }
        filter_log_msg(LOG_LEVEL_DEBUG, "  Type checking\n");
        if (check_types(root) == error) {
            success = false;
        }
        if (success) {
            filter_log_msg(LOG_LEVEL_DEBUG, "  Determining labels\n");
            success = determine_labels(root, &parser_dict, &label_dict, name_dict);
        }
        if (success) {
            filter_log_msg(LOG_LEVEL_DEBUG, "  Determining fields\n");
            success = determine_fields(root, &parser_dict, &label_dict, key_dict);
        }
        if (success) {
            filter_log_msg(LOG_LEVEL_DEBUG, "  Interning string literals\n");
            populate_string_literals(root, &parser_dict, val_dict);
            filter_log_msg(LOG_LEVEL_DEBUG, "  Generating rules\n");
            generate_specification(root, spec);
        }
        
        if (should_log(LOG_LEVEL_DEBUG)) {
//            log_words(&label_dict);
            log_words(name_dict);
            log_words(key_dict);
            log_words(val_dict);
            
            if (should_log(LOG_LEVEL_SUPERDEBUG)) {
                // write dot files for debugging
                write_ast_graph(root, &parser_dict);
            }
        }
        
        free_node(root);
    } else {
        if (parse_result == 0) {
            filter_log_msg(LOG_LEVEL_ERROR, "Empty specification.  Is everything commented out?\n");
        } else if (parse_result == 1) {
            filter_log_msg(LOG_LEVEL_ERROR, "Parse failed due to invalid input\n");
        } else if (parse_result == 2) {
            filter_log_msg(LOG_LEVEL_ERROR, "Parse failed due to memory exhaustion\n");
        } else {
            filter_log_msg(LOG_LEVEL_ERROR, "Parse failed due to an unknown result: %d\n", parse_result);
        }
        success = false;
    }
    yylex_destroy(scanner);
    destroy_dictionary(&label_dict);
    destroy_dictionary(&parser_dict);
    
    return success;
}


bool scan_specification(const char *code, 
                        nfer_specification *spec, 
                        dictionary *name_dict, 
                        dictionary *key_dict, 
                        dictionary *val_dict) {
    return read_specification(code, spec, name_dict, key_dict, val_dict, false); 
}


bool load_specification(const char *filename, 
                        nfer_specification *spec, 
                        dictionary *name_dict, 
                        dictionary *key_dict, 
                        dictionary *val_dict) {
    return read_specification(filename, spec, name_dict, key_dict, val_dict, true);
}
