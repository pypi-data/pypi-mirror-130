/*
 * debug.h
 *
 *  Created on: May 12, 2021
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

#ifndef INC_DEBUG_H_
#define INC_DEBUG_H_

#include "pool.h"
#include "dict.h"
#include "nfer.h"

unsigned int log_pool_use(const char *, pool *);
unsigned int log_dictionary_use(const char *, dictionary *);
void log_specification_use(dictionary *, nfer_specification *);

#endif /* INC_DEBUG_H_ */
