/*
 * RCFilter.c
 *
 *  Created on: Dec 5, 2025
 *      Author: louisvoz
 */
#include "RCFilter.h"
#include "main.h"

//-------- Delay Buffer pour l'écho --------
int16_t delay_buffer[DELAY_BUF_SIZE];
uint32_t delay_index=0;
//----------------------------------------

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

void Process_Audio_Buffer(int16_t *src, int16_t *dst, uint32_t len_in_bytes)
{
	uint16_t *pSrc = (uint16_t*)src;
	uint16_t *pDst = (uint16_t*)dst;

	uint32_t num_samples = len_in_bytes / 2;

	for (uint32_t i = 0; i < num_samples; i++)
	{

		int16_t input_sample=pSrc[i];

		// 1. Lire l'échantillon qui a été stocké il y a longtemps (l'écho)
		int16_t delayed_sample = delay_buffer[delay_index];

		// 2. Calculer la sortie : Son actuel + (Echo * volume)
		// On divise par 2 l'écho pour qu'il soit moins fort (decay)
		int16_t output_sample = input_sample + (delayed_sample / 2);

		// 3. Ecrire le son actuel dans la mémoire pour le futur
		delay_buffer[delay_index] = input_sample;

		// 4. Avancer l'index et boucler si on arrive au bout (Buffer Circulaire)
		delay_index++;
		if (delay_index >= DELAY_BUF_SIZE) {
			delay_index = 0;
		}

		// 5. Envoyer vers le DAC
		pDst[i] = output_sample;
	}
}

