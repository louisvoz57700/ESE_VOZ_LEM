/*
 * RCFilter.c
 *
 *  Created on: Dec 5, 2025
 *      Author: louisvoz
 */
#include "RCFilter.h"
#include "main.h"

// Calcule les coefficients A, B et D
// Et les stocke dans la structure
void RC_filter_init(h_RC_filter_t* h_RC_filter, uint16_t cutoff_frequency, uint16_t sampling_frequency)
{
	h_RC_filter->coeff_A = 1;
	h_RC_filter->coeff_B =(float)(sampling_frequency * (1 / (2.0 * 3.14 * cutoff_frequency)));
	h_RC_filter->coeff_D =(float) (1 + sampling_frequency / (2.0 * 3.14 * cutoff_frequency));
}
// Implémente l'équation de récurrence
// Faites attention au type des différentes variables
int16_t RC_filter_update(h_RC_filter_t* h_RC_filter, uint16_t input)
{
    float out = (h_RC_filter->coeff_A * input + h_RC_filter->coeff_B * h_RC_filter->out_prev) / h_RC_filter->coeff_D;
    h_RC_filter->out_prev = out;

    // Clamp pour retourner un int16_t positif
    if (out < 0)
        return 0;
    else if (out > 65535)  // uint16 max
        return 65535;
    else
        return (int16_t)out;
}

