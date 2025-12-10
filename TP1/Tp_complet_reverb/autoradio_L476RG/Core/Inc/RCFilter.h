/*
 * RCFilter.h
 * Created on: Dec 5, 2025
 * Author: Antle
 */

#ifndef INC_RCFILTER_H_
#define INC_RCFILTER_H_

#include <stdint.h> // Nécessaire pour uint32_t et uint16_t

typedef struct {
    uint32_t coeff_A;
    float coeff_B;
    float coeff_D;
    float out_prev; // Mémorise la valeur précédente (y[n-1])
} h_RC_filter_t;

void RC_filter_init(h_RC_filter_t * h_RC_filter, uint16_t cutoff_frequency, uint16_t sampling_frequency);

uint16_t RC_filter_update(h_RC_filter_t * h_RC_filter, uint16_t input);

#endif /* INC_RCFILTER_H_ */
