/*
 * target.h
 *
 * This file is meant to be included at the top of a compiled monitor.
 * It is not target specific, but contains target specific defines.
 *
 *  Created on: Jul 11, 2018
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
 *   along with this program.  If not, see www.gnu.org/licenses/.
 */


/******************************************************************
 * This section should be configured for your application.
 ******************************************************************/

#define RULE_CACHE_SIZES 100
#define NEW_INTERVALS_SIZE 20
#define VALUE_DICTIONARY_SIZE  20

#define FULL_RESULTS 0
/* WINDOW_SIZE must be set unless the maximum trace size is known! */
#define WINDOW_SIZE 0
#define PURGE_THRESHOLD 0.5
#ifndef TARGET
#define TARGET linux
#endif

/******************************************************************
 * End of the configuration section.  Don't change anything below this line!
 ******************************************************************/

// We have a section here for includes that are dependent on the target OS
// The issue is that we might need these prior to the OS specific files
// It would be great if we could find a way to avoid this

// This, so far, is included for all OS targets
#include <stdarg.h>
#include <stdint.h>
#include <inttypes.h>
#include <float.h>
#define NO_DYNAMIC_MEMORY


// Linux defines
#if TARGET==linux
#include <stdio.h>
#endif

// other target defines go here
