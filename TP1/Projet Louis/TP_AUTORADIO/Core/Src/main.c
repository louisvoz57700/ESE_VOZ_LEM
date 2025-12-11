/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2025 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "cmsis_os.h"
#include "dma.h"
#include "i2c.h"
#include "sai.h"
#include "spi.h"
#include "usart.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include <stdio.h>
#include "shell.h"
#include "drv_uart1.h"
#include "GPIO_EXTANDER.h"
#include "sgtl5000.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */
#define AUDIO_BUFFER_SIZE 256
QueueHandle_t uartQueue;      // Queue pour les caractères UART
uint8_t rx_byte; // caractère reçu
int16_t txBuffer[AUDIO_BUFFER_SIZE];
int16_t rxBuffer[AUDIO_BUFFER_SIZE];

extern MCP23S17_HandleTypeDef hmcp23s17;
/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */


/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */
h_shell_t h_shell;
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
void PeriphCommonClock_Config(void);
void MX_FREERTOS_Init(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
int __io_putchar(int ch)
{
	HAL_UART_Transmit(&huart2, (uint8_t*)&ch, 1, HAL_MAX_DELAY);

	return ch;
}

int fonction(h_shell_t * h_shell, int argc, char ** argv)
{
	int size = snprintf (h_shell->print_buffer, BUFFER_SIZE, "Je suis une fonction bidon\r\n");
	h_shell->drv.transmit(h_shell->print_buffer, size);

	return 0;
}

int LED(h_shell_t * h_shell, int argc, char ** argv)
{
	int numero;
	int size;
	if (argv[1]=="\r")
	{
		numero = atoi(argv[0]);
		if (numero > 8)
		{
			Select_LED('B', 16-numero,1);
		}
		else
		{
			Select_LED('A', numero,1);
		}
		size = snprintf(h_shell->print_buffer,BUFFER_SIZE,"c'est fait chef");
	}
	else if (argv[1]=="1")
	{
		numero = atoi(argv[0]) * 10 + atoi(argv[1]);
		Select_LED('B', 16-numero,1);
		size = snprintf(h_shell->print_buffer,BUFFER_SIZE,"c'est fait chef");
	}
	else
	{
		size = snprintf(h_shell->print_buffer,BUFFER_SIZE,"Il y a pas assez de led");
	}
	drv_uart1_transmit(h_shell->print_buffer,size);
	return 0;

}


void Task_shell(void)
{
	  shell_init(&h_shell);
	  shell_add(&h_shell,'f', fonction, "Une fonction inutile");
	  shell_add(&h_shell,'L',LED,"Une fonction pour allumer les LEDs");
	  shell_run(&h_shell);
}

void Task_LED(void const *argument)
{
    (void)argument;  // Si tu utilises osThread

    for(;;)
    {
    	//generateTriangle(txBuffer, AUDIO_BUFFER_SIZE, 10000);  // amplitude ≈ 10k / 32767
    	Select_LED('A', 1,1);
    	Select_LED('A', 0,1);
    	Select_LED('A', 7,1);
    	Select_LED('B', 1,1);
    	vTaskDelay(200);
    	Select_LED('A', 1,0);
		Select_LED('A', 0,1);
		Select_LED('A', 7,0);
		Select_LED('B', 1,0);
    	vTaskDelay(200);


    }
}
/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{

  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* Configure the peripherals common clocks */
  PeriphCommonClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_DMA_Init();
  MX_USART2_UART_Init();
  MX_SPI3_Init();
  MX_I2C2_Init();
  MX_SAI2_Init();
  /* USER CODE BEGIN 2 */
  //h_shell.drv.receive = drv_uart1_receive;
  MCP23S17_Init();
  MCP23S17_SetAllPinsHigh();
  __HAL_SAI_ENABLE(&hsai_BlockA2);

  uint8_t chip_id = 0;
  HAL_StatusTypeDef status;

  status = HAL_I2C_Mem_Read(
      &hi2c2,              // Handle I2C2
      0x14,           // Adresse I2C du CODEC (décalée)
      0x0000,              // Adresse du registre CHIP_ID
      I2C_MEMADD_SIZE_16BIT,
      &chip_id,            // Buffer où stocker la donnée
      1,                   // Lire 1 octet
      100                  // Timeout
  );

  h_shell.drv.transmit = drv_uart1_transmit;
  uartQueue = xQueueCreate(32, sizeof(uint8_t));
  HAL_UART_Receive_IT(&huart2, &rx_byte, 1);

  uint16_t sgtl_address = 0x14;
  uint16_t data;

  h_sgtl5000_t h_sgtl5000;
  h_sgtl5000.hi2c = &hi2c2;
  h_sgtl5000.dev_address = sgtl_address;

  sgtl5000_init(&h_sgtl5000);

  generateTriangle(txBuffer, AUDIO_BUFFER_SIZE, 10000);
  //generateSquare(txBuffer, AUDIO_BUFFER_SIZE, 30000);
  HAL_SAI_Transmit_DMA(&hsai_BlockA2, (int16_t*)txBuffer, AUDIO_BUFFER_SIZE);
  HAL_SAI_Receive_DMA(&hsai_BlockB2, (int16_t*)rxBuffer, AUDIO_BUFFER_SIZE);



  xTaskCreate(Task_shell, "Shell", 256, NULL, 1, NULL);
  xTaskCreate(Task_LED, "LED", 256, NULL, 1, NULL);

  /* USER CODE END 2 */

  /* Call init function for freertos objects (in cmsis_os2.c) */
  MX_FREERTOS_Init();

  /* Start scheduler */
  osKernelStart();

  /* We should never get here as control is now taken by the scheduler */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */


  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  if (HAL_PWREx_ControlVoltageScaling(PWR_REGULATOR_VOLTAGE_SCALE1) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
  RCC_OscInitStruct.PLL.PLLM = 1;
  RCC_OscInitStruct.PLL.PLLN = 10;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV7;
  RCC_OscInitStruct.PLL.PLLQ = RCC_PLLQ_DIV2;
  RCC_OscInitStruct.PLL.PLLR = RCC_PLLR_DIV2;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_4) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief Peripherals Common Clock Configuration
  * @retval None
  */
void PeriphCommonClock_Config(void)
{
  RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};

  /** Initializes the peripherals clock
  */
  PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_SAI2;
  PeriphClkInit.Sai2ClockSelection = RCC_SAI2CLKSOURCE_PLLSAI1;
  PeriphClkInit.PLLSAI1.PLLSAI1Source = RCC_PLLSOURCE_HSI;
  PeriphClkInit.PLLSAI1.PLLSAI1M = 1;
  PeriphClkInit.PLLSAI1.PLLSAI1N = 13;
  PeriphClkInit.PLLSAI1.PLLSAI1P = RCC_PLLP_DIV17;
  PeriphClkInit.PLLSAI1.PLLSAI1Q = RCC_PLLQ_DIV2;
  PeriphClkInit.PLLSAI1.PLLSAI1R = RCC_PLLR_DIV2;
  PeriphClkInit.PLLSAI1.PLLSAI1ClockOut = RCC_PLLSAI1_SAI1CLK;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
    if(huart->Instance == USART2) // Vérifier qu'il s'agit bien de l'UART2
    {
    	BaseType_t xHigherPriorityTaskWoken = pdFALSE;
		xQueueSendFromISR(uartQueue, &rx_byte, &xHigherPriorityTaskWoken);

		// Relancer la réception
		HAL_UART_Receive_IT(&huart2, &rx_byte, 1);

		// Si une tâche a été réveillée par l’ISR, demander un switch
		portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
    }
}

void generateTriangle(int16_t *buffer, uint32_t bufferSize, int16_t amplitude)
{
    uint32_t i;

    // On travaille en fixed-point pour éviter les arrondis foireux
    for (i = 0; i < bufferSize; i++) {
        // Position dans le cycle : 0 → bufferSize-1
        // On utilise 4 * i pour avoir une résolution plus fine (évite les trous d'arrondi)
        int32_t phase = (int32_t)(4ULL * i * amplitude / bufferSize);

        if (i < bufferSize / 2) {
            // Montée : -amplitude → +amplitude
            buffer[i] = (int16_t)(phase - amplitude);
        } else {
            // Descente : +amplitude → -amplitude
            buffer[i] = (int16_t)(3 * amplitude - phase);
        }
    }
}

void generateSquare(int16_t *buf, uint32_t len, int16_t amp)
{
    uint32_t half = len / 2;
    for (uint32_t i = 0; i < len; i++) {
        buf[i] = (i < half) ? amp : -amp;
    }
}

void HAL_SAI_TxHalfCpltCallback(SAI_HandleTypeDef *hsai)
{
    //generateTriangle(&txBuffer[0], AUDIO_BUFFER_SIZE/2, 12000);
}

void HAL_SAI_TxCpltCallback(SAI_HandleTypeDef *hsai)
{
    //generateTriangle(&txBuffer[AUDIO_BUFFER_SIZE/2], AUDIO_BUFFER_SIZE/2, 12000);
}

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}
#ifdef USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
