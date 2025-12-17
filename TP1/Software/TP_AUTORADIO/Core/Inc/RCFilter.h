/*
 * RCFilter.h
 *
 *  Created on: Dec 5, 2025
 *      Author: louisvoz
 */

#ifndef INC_RCFILTER_H_
#define INC_RCFILTER_H_

#include "main.h"

typedef struct {
	uint32_t coeff_A;
	float coeff_B;
	float coeff_D;
	uint16_t out_prev;
} h_RC_filter_t;

int16_t RC_filter_update(h_RC_filter_t* h_RC_filter, uint16_t input);
void RC_filter_init(h_RC_filter_t* h_RC_filter, uint16_t cutoff_frequency, uint16_t sampling_frequency);
void Process_Audio_Buffer(int16_t *src, int16_t *dst, uint32_t len_in_bytes);

#define DELAY_BUF_SIZE 20000

#endif /* INC_RCFILTER_H_ */
