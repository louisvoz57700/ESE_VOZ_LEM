/*
 * chip_id.c
 *
 *  Created on: Nov 21, 2025
 *      Author: Antle
 */

#include "chip_id.h"
#include <stdio.h>
#include "i2c.h"

uint8_t Lire_CHIP_ID(void)
{
    uint8_t valeur_CHIP_ID = 0;
    HAL_StatusTypeDef ret;

    ret = HAL_I2C_Mem_Read(&hi2c2,
                           0x14,
                           0x0000,
                           I2C_MEMADD_SIZE_16BIT,
                           &valeur_CHIP_ID,
                           1,
                           HAL_MAX_DELAY);

    if (ret == HAL_OK) {
        printf("Valeur du registre CHIP ID : 0x%02X\r\n", valeur_CHIP_ID);
    } else {
        printf("Erreur de lecture I2C\r\n");
    }

    return valeur_CHIP_ID;
}

