# ESE_VOZ_LEM
# 📘 TP 1– README AUTO RADIO

Bienvenue dans le dépôt de notre premier  **TP**.  
Chaque dossier correspond à un TP individuel avec son propre fichier `README.md` décrivant le contenu, les objectifs et les instructions spécifiques.

1 Démarrage
1. Créez un projet pour la carte NUCLEO_L476RG. Initialisez les périphériques
avec leur mode par défaut, mais n’activez pas la BSP.
2. Testez la LED LD2. Code :
 while (1)
  {
	  // Question 2 clignotemement ledD2
	  HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
	  HAL_Delay(1000);
	  
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */

  } 
  Photo :
