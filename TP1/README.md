# ESE_VOZ_LEM
# 📘 TP 1– README AUTO RADIO

Bienvenue dans le dépôt de notre premier  **TP**.  
Chaque dossier correspond à un TP individuel avec son propre fichier `README.md` décrivant le contenu, les objectifs et les instructions spécifiques.

# 🟢 1. Démarrage

1. **Créez un nouveau projet** pour la carte **NUCLEO-L476RG**.  
   Initialisez les périphériques avec leurs **modes par défaut**, mais **n’activez pas la BSP**.

2. **Testez la LED LD2** (connectée à la broche **PA5**) avec le code suivant :

   ```c
   while (1)
   {
       // Question 2 : Clignotement de la LED LD2
       HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
       HAL_Delay(1000); // Délai de 1 seconde
   }
![LED LD2 en fonctionnement](./IMG/IMG_5638.JPG)
