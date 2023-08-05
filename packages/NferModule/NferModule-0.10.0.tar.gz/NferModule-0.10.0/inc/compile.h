/*
 * compile.h
 *
 *  Created on: May 8, 2018
 *      Author: skauffma
 */

#ifndef INC_COMPILE_H_
#define INC_COMPILE_H_

#ifndef SKIP_INCLUDES
#include "ast.h"
#include "dict.h"
#endif

void compile_monitor(char *, nfer_specification *, dictionary *, dictionary *, dictionary *);

#endif /* INC_COMPILE_H_ */
