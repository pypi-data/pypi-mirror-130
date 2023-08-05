/*
 * learn.c
 *
 *  Created on: Jan 19, 2017
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

#include "learn.h"
#include "dict.h"
#include "nfer.h"
#include "log.h"
#include "memory.h"

extern nfer_operator operators[];

void initialize_learning(learning *learn, int size) {
    learn->size = size;

    // allocate the matrix
    learn->matrix = (learning_cell *) malloc(size * size * sizeof(learning_cell));
    if (learn->matrix != NULL) {
        clear_memory(learn->matrix, size * size * sizeof(learning_cell));
    }
    // allocate the stats array
    learn->stats = (interval_stat *) malloc(size * sizeof(interval_stat));
    if (learn->stats != NULL) {
        clear_memory(learn->stats, size * sizeof(interval_stat));
    }
}

/**
 * Deallocates a learning, but does not destroy the related dictionary.
 */
void destroy_learning(learning *learn) {
    if (learn->matrix != NULL) {
        free(learn->matrix);
    }
    if (learn->stats != NULL) {
        free(learn->stats);
    }
    learn->size = 0;
    learn->matrix = NULL;
    learn->stats = NULL;
}

static word_id generate_interval_name(dictionary *dict) {
    static unsigned int count = 0;
    char buffer[MAX_WORD_LENGTH + 1];

    do {
        sprintf(buffer, "learned_%d", count++);
    } while (find_word(dict, buffer) != WORD_NOT_FOUND);

    return add_word(dict, buffer);
}

void add_learned_rules(learning *learn, dictionary *dict, nfer_specification *nfer, float confidence, float support) {
    int i, j, op;
    learning_cell *cell, *inverse;
    label combined;
    double variance, inverse_variance;

    filter_log_msg(LOG_LEVEL_DEBUG, "relation\tfailure\tsuccess\tconfidence\tav_length\tinv_length\tstd_ave\tinv_std_ave\tresult\n");

    for (i = 0; i < learn->size; i++) {
        for (j = 0; j < learn->size; j++) {
            if (i != j) {

                cell = &learn->matrix[i * learn->size + j];
                inverse = &learn->matrix[j * learn->size + i];

                // N_OPERATORS is defined in nfer.h
                //for (op = 0; op < N_OPERATORS; op++) {
                op = BEFORE_OPERATOR;
                {
                    // calculate variance for the cell
                    if (cell->success > 1) {
                        variance = cell->length_variance_s / ((double)cell->success - 1);
                    } else {
                        variance = 0.0;
                    }
                    // calculate variance for the inverse
                    if (inverse->success > 1) {
                        inverse_variance = inverse->length_variance_s / ((double)inverse->success - 1);
                    } else {
                        inverse_variance = 0.0;
                    }

                    // avoid divide by zero errors
                    if ((double)cell->failure + (double)cell->success > 0) {
                        filter_log_msg(LOG_LEVEL_DEBUG, "\"%s %s %s\"\t%u\t%u\t%f\t%f\t%f\t%f\t%f\t",
                                get_word(dict, i),
                                operators[op].name,
                                get_word(dict, j),
                                cell->failure,
                                cell->success,
                                (double)cell->success / ((double)cell->failure + (double)cell->success),
                                cell->average_length,
                                inverse->average_length,
                                variance / (double)cell->average_length,
                                inverse_variance / (double) inverse->average_length);
                    }

                    if (cell->success >= support) {

                        if ((double)cell->success / ((double)cell->failure + (double)cell->success) >= confidence) {
                            // only add the rule if it is shorter than the opposite version
                            if (cell->average_length <= inverse->average_length) {
                            //if (variance / (double) cell->average_length <= inverse_variance / (double) inverse->average_length) {
                                // put the interval names together and add to the dictionary
                                combined = generate_interval_name(dict);

                                // add the rule
                                add_rule_to_specification(nfer, combined, i, op, j, NULL);
                                filter_log_msg(LOG_LEVEL_DEBUG, "\"(ACCEPTED)\"\n");
                            } else {
                                filter_log_msg(LOG_LEVEL_DEBUG, "\"(REJECTED: length > inverse)\"\n");
                                //filter_log_msg(LOG_LEVEL_DEBUG, "(REJECTED: variance > inverse variance)\n");
                            }
                        } else {
                            filter_log_msg(LOG_LEVEL_DEBUG, "\"(REJECTED: confidence < %f)\"\n", confidence);
                        }

                    } else {
                        if ((double)cell->failure + (double)cell->success > 0) {
                            filter_log_msg(LOG_LEVEL_DEBUG, "\"(REJECTED: support < %f)\"\n", support);
                        }
                    }
                }
            }
        }
    }
}

void finish_learning(learning *learn) {
    int i, j;
    learning_cell *cell;

    for (i = 0; i < learn->size; i++) {
        for (j = 0; j < learn->size; j++) {
            cell = &learn->matrix[i * learn->size + j];

            if (cell->matched == 1) {
                cell->success++;
            } else if (cell->matched > 1) {
                cell->failure++;
            }
            cell->matched = 0;
        }
    }

    // clear the stats array
    if (learn->stats != NULL) {
        clear_memory(learn->stats, learn->size * sizeof(interval_stat));
    }
}

void learn_interval(learning *learn, interval *add) {
    int i, position;
    double new_average, new_variance_s;
    learning_cell *cell;
    interval_stat *left_stat;

    // the position is just the interval name
    position = add->name;
    // sanity check the position
    //assert(position >= 0 && position < learn->size);
    //printf("\nAdding interval %d\n----------------\n", add->label);

    // first do the column (add is B in A before B)
    for (i = 0; i < learn->size; i++) {
        // use left_stat to get the stats for the A interval
        left_stat = &learn->stats[i];

        if (left_stat->seen) {
            cell = &learn->matrix[i * learn->size + position];

            if (operators[BEFORE_OPERATOR].test(left_stat->start, left_stat->end, add->start, add->end)) {
                //printf("%d %s %d\n", i, operators[op].name, position);
                cell->matched++;
                // store the length of this match
                cell->last_length = operators[BEFORE_OPERATOR].end_time(left_stat->end, add->end) -
                                    operators[BEFORE_OPERATOR].start_time(left_stat->end, add->end);
            }

        } else {
            //printf("Haven't yet seen left side %s\n", get_word(learn->dict, i));
            // we haven't seen the left side, so that means we shouldn't make assumptions about it
        }

    }

    // then do the row (add is A in A before B)
    left_stat = &learn->stats[position];
    // set new start and end values
    left_stat->start = add->start;
    left_stat->end = add->end;

    // if this isn't the first time seeing this interval
    if (left_stat->seen) {
        for (i = 0; i < learn->size; i++) {
            cell = &learn->matrix[position * learn->size + i];

            if (cell->matched == 1) {
                cell->success++;

                // update the average length and variance
                if (cell->success == 1) {
                    cell->average_length = (double)cell->last_length;
                    cell->length_variance_s = 0.0;
                } else {
                    new_average = cell->average_length +
                            ((double)cell->last_length - cell->average_length) / (double)cell->success;
                    new_variance_s = cell->length_variance_s +
                            ((double)cell->last_length - cell->average_length) *
                            ((double)cell->last_length - new_average);
                    cell->average_length = new_average;
                    cell->length_variance_s = new_variance_s;
                }
                cell->last_length = 0;

            } else { //if (!cell->matched) {
                cell->failure++;
            }
            // always clear matched
            cell->matched = 0;
        }

    } else {
        left_stat->seen = true;
    }
}

void run_learner_on_pool(pool *input_pools,
        unsigned int num_pools,
        dictionary *name_dict,
        dictionary *UNUSED(key_dict),
        dictionary *UNUSED(val_dict),
        nfer_specification *spec,
        float confidence,
        float support) {

    pool_iterator pit;
    learning learn;
    unsigned int pool_index;
    pool *in;

    if (should_log(LOG_LEVEL_DEBUG)) {
        log_words(name_dict);
        log_msg("Running learner on %u pool(s)\n", num_pools);
    }

    // set up initial learning and nfer spec
    initialize_learning(&learn, name_dict->size);

    for (pool_index = 0; pool_index < num_pools; pool_index++) {
        in = &input_pools[pool_index];

        filter_log_msg(LOG_LEVEL_STATUS, "Adding intervals to learner...\n");
        // try adding the test intervals
        get_pool_iterator(in, &pit);
        while (has_next_interval(&pit)) {
            learn_interval(&learn, next_interval(&pit));
        }

        // break after every trace to facilitate non-contiguous traces
        finish_learning(&learn);
    }

    filter_log_msg(LOG_LEVEL_STATUS, "Adding learned rules to specification...\n");

    // add the rules to the specification
    add_learned_rules(&learn, name_dict, spec, confidence, support);

    // teardown learning
    destroy_learning(&learn);

}
