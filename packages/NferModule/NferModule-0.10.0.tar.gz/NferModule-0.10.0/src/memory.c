/*
 * memory.c
 *
 *  Created on: May 14, 2018
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
#include "memory.h"

void set_memory(void *address, size_t size) {
    const long int two_words = -1L;
    const char byte = -1;
    int xlength, xpos, length, pos;
    xlength = 0;

    if (size >= sizeof(two_words)) {
        xlength = size / sizeof(two_words);
        xpos = xlength;

        while (xpos--) {
            ((long int *)address)[xpos] = two_words;
        }
    }

    length = size % sizeof(two_words);
    pos = length;
    while (pos--) {
        ((char *)address)[xlength * sizeof(two_words) + pos] = byte;
    }
}
void clear_memory(void *address, size_t size) {
    const long int two_words = 0L;
    const char byte = 0;
    int xlength, xpos, length, pos;
    xlength = 0;

    if (size >= sizeof(two_words)) {
        xlength = size / sizeof(two_words);
        xpos = xlength;

        while (xpos--) {
            ((long int *)address)[xpos] = two_words;
        }
    }

    length = size % sizeof(two_words);
    pos = length;
    while (pos--) {
        ((char *)address)[xlength * sizeof(two_words) + pos] = byte;
    }
}
void copy_memory(void *dest, const void *src, size_t size) {
    int xlength, xpos, length, pos, offset;
    xlength = 0;

    if (size >= sizeof(const long int)) {
        xlength = size / sizeof(const long int);
        xpos = xlength;

        while (xpos--) {
            ((long int *)dest)[xpos] = ((const long int *)src)[xpos];
        }
    }

    length = size % sizeof(const long int);
    pos = length;
    offset = xlength * sizeof(const long int);
    while (pos--) {
        ((char *)dest)[offset + pos] = ((const char *)src)[offset + pos];
    }
}
