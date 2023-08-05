/*
 * dsl.h
 *
 *  Created on: May 18, 2017
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

#ifndef INC_DSL_H_
#define INC_DSL_H_

#include "nfer.h"
#include "dict.h"

bool scan_specification(const char *, nfer_specification *, dictionary *, dictionary *, dictionary *);
bool load_specification(const char *, nfer_specification *, dictionary *, dictionary *, dictionary *);

#endif /* INC_DSL_H_ */
