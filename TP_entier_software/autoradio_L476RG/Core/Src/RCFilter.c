/*
 * RCFilter.c
 * Created on: Dec 5, 2025
 * Author: Antle
 */

#include "RCFilter.h"


void RC_filter_init(h_RC_filter_t * h_RC_filter, uint16_t cutoff_frequency, uint16_t sampling_frequency)
{
    uint32_t b_value = 0;

    if (cutoff_frequency > 0) {
        b_value = (uint32_t)(sampling_frequency) / (2 * 3.14f * cutoff_frequency);
    }

    h_RC_filter->coeff_A = 1;
    h_RC_filter->coeff_B = b_value;
    h_RC_filter->coeff_D = 1 + b_value;

    h_RC_filter->out_prev = 0;
}

uint16_t RC_filter_update(h_RC_filter_t * h_RC_filter, uint16_t input)
{

    uint32_t acc = 0;

    acc = (h_RC_filter->coeff_A * input) + (h_RC_filter->coeff_B * h_RC_filter->out_prev);

    uint16_t output = (uint16_t)(acc / h_RC_filter->coeff_D);

    h_RC_filter->out_prev = output;

    return output;
}
