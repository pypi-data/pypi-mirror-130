 /*
 * log.h
 *
 *  Created on: Feb 2, 2017
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

#ifndef LOG_H_
#define LOG_H_

#include "types.h"


#define LOG_LEVEL_NONE 0
#define LOG_LEVEL_ERROR -1
#define LOG_LEVEL_WARN 0
#define LOG_LEVEL_STATUS 1
#define LOG_LEVEL_INFO 2
#define LOG_LEVEL_DEBUG 3
#define LOG_LEVEL_SUPERDEBUG 4

#define DEFAULT_LOG_LEVEL LOG_LEVEL_NONE

#define WRITE_OUTPUT   0
#define WRITE_LOGGING  1
#define WRITE_TESTING  2

#define TEST_BUFFER_SIZE 255

void set_log_level(int level);
void set_log_file(const char *filename);
void set_output_file(const char *filename);
void stop_logging(void);
void stop_output(void);

void filter_log_msg(int level, const char *message, ...);
void log_msg(const char *message, ...);
bool should_log(int level);
void write_msg(int log_to, const char *message, ...);

#endif /* LOG_H_ */
