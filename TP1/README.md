<h1>📘 TP1 – AUTO RADIO</h1>
<h3>Projet ESE_VOZ_LEM</h3>

<p>
Bienvenue dans le dépôt de notre premier <strong>Travail Pratique (TP1)</strong>.<br>
Ce projet est basé sur la carte <strong>NUCLEO-L476RG</strong> et a pour but d’explorer la configuration matérielle de base, 
le contrôle GPIO, la communication UART, et l’utilisation de FreeRTOS.
</p>

<hr>

<h2>🟢 1. Démarrage</h2>

<h3>Étape 1 — Création du projet</h3>
<ol>
  <li>Créez un <strong>nouveau projet</strong> pour la carte <strong>NUCLEO-L476RG</strong>.</li>
  <li>Initialisez les périphériques avec leurs <strong>modes par défaut</strong>, mais <strong>n’activez pas la BSP</strong>.</li>
</ol>

<hr>

<h3>Étape 2 — Test de la LED LD2</h3>

<p>La LED <strong>LD2</strong> est connectée à la broche <strong>PA5</strong>.<br>
Ajoutez le code suivant dans la boucle principale :</p>

<pre><code class="language-c">
while (1)
{
    // Question 2 : Clignotement de la LED LD2
    HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
    HAL_Delay(1000); // Délai de 1 seconde
}
</code></pre>

<p>📸 <strong>LED LD2 en fonctionnement :</strong></p>

<p>
  <img src="./IMG/IMG_5638.JPG" alt="LED LD2 en fonctionnement" width="400">
</p>

<hr>

<h3>Étape 3 & 4 — Test de l’USART2 (ST-Link interne)</h3>

<p>L’<strong>USART2</strong> est utilisé pour communiquer via le port série intégré à la carte.<br>
Ajoutez le code suivant pour rediriger <code>printf()</code> vers l’UART :</p>

<pre><code class="language-c">
/* USER CODE BEGIN 0 */
int __io_putchar(int ch) {
    HAL_UART_Transmit(&huart2, (uint8_t *)&ch, 1, HAL_MAX_DELAY);
    return ch;
}
/* USER CODE END 0 */

/* USER CODE BEGIN 2 */
printf("Bonjour Antonio y Louis\r\n");
/* USER CODE END 2 */
</code></pre>

<p><strong>Sortie série visible dans le terminal :</strong></p>
<p>
  <img src="https://github.com/user-attachments/assets/92725134-4f12-49b1-810d-fcdc11942f61" 
       alt="Sortie série visible" width="544" height="234">
</p>

<hr>

<h3>Étape 5 — Activation de FreeRTOS</h3>

<p>
Activez <strong>FreeRTOS</strong> via <strong>CMSIS V1</strong>.<br>
<img width="624" height="206" alt="FreeRtos" src="https://github.com/user-attachments/assets/551afd50-894b-4634-ba9e-a02f31364b89" />
</p>

<hr>

<h3>6. Faites fonctionner le shell :</h3>
<p>
<img width="494" height="196" alt="image" src="https://github.com/user-attachments/assets/11a05490-4c9f-4896-a64f-eee81310e1c3" />
</p>
<h2>🔵 2. Le GPIO Expander et le VU-Mètre</h2>

<h3>2.1 Configuration</h3>

<p><em>(1. Quelle est la référence du GPIO Expander ? Vous aurez besoin de sa datasheet, téléchargez-la.)</em><br>
Le GPIO Expander est le MCP23S17 et sa datasheet est téléchargé dans le dossier Datasheet.
</p>

<p><em>(2. Sur le STM32, quel SPI est utilisé ?)</em><br>
<img width="1382" height="964" alt="image" src="https://github.com/user-attachments/assets/3e514302-aa08-4476-8c48-a7a9a316898a" />
<img width="698" height="820" alt="image" src="https://github.com/user-attachments/assets/bd4ac86d-1cfa-422b-88c5-07ef3554d0c7" />

C'est donc le SPI3 et nous le configurons sur cubeIde:
<img width="454" height="520" alt="image" src="https://github.com/user-attachments/assets/a627610c-3d2b-4387-8414-3eb473f5d448" />



</p>

<hr>

<h2>🧩 Résumé des objectifs</h2>

<ul>
  <li>✅ Configuration initiale du projet STM32</li>
  <li>✅ Test du <strong>GPIO (LED LD2)</strong></li>
  <li>✅ Test de la <strong>liaison série (USART2)</strong></li>
  <li>✅ Mise en place de <strong>FreeRTOS</strong></li>
  <li>⏳ Configuration du <strong>GPIO Expander / VU-Mètre</strong></li>
</ul>

<hr>

<h2>👨‍💻 Auteurs</h2>

<ul>
  <li><strong>Antonio</strong></li>
  <li><strong>Louis</strong></li>
</ul>

<hr>

<p>
💡 <em>Astuce :</em> N’oubliez pas de vérifier que le port série (<code>COMx</code>) 
est bien sélectionné dans votre terminal (<strong>115200 bauds, 8N1</strong>).
</p>
