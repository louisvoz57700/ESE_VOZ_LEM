/*
 * drv_uart1.h
 *
 *  Created on: Nov 13, 2025
 *      Author: louisvoz
 */
#ifndef DRV_UART1_H_
#define DRV_UART1_H_

#include <stdint.h>

uint8_t drv_uart1_receive(char * pData, uint16_t size);
uint8_t drv_uart1_transmit(const char * pData, uint16_t size);

#endif /* DRV_UART1_H_ */
