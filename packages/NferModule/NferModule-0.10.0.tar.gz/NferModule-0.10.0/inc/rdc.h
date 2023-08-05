/*
 * rdc.h
 *
 *  Created on: Jul 12, 2018
 *      Author: skauffma
 */

#ifndef INC_RDC_H_
#define INC_RDC_H_

#define RDC_IO_BUFFER_LENGTH 16384     /* size of disk io buffer  */
#define RDC_HASH_TABLE_LENGTH  4096    /* # hash table entries    */

typedef enum {
    NO_ERROR,
    ERROR_BLOCK_LENGTH,
    ERROR_READ_UNCOMPRESSED,
    ERROR_READ_COMPRESSED,
    ERROR_WRITE_UNCOMPRESSED,
    ERROR_WRITE_COMPRESSED,
    ERROR_TRAILER
} rdc_error_code;

rdc_error_code decompress_file(FILE *, FILE *);
rdc_error_code decompress_array_to_file(uint8_t[], FILE *);
rdc_error_code compress_file(FILE *, FILE *);
void strip_comments_and_includes(FILE *, FILE *);

#endif /* INC_RDC_H_ */
