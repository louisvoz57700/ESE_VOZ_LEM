<body>

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
<img src="./IMG/IMG_5638.JPG" alt="LED LD2 en fonctionnement" width="400">

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
<img src="https://github.com/user-attachments/assets/92725134-4f12-49b1-810d-fcdc11942f61" 
     alt="Sortie série visible" width="544">

<hr>

<h3>Étape 5 — Activation de FreeRTOS</h3>
<p>Activez <strong>FreeRTOS</strong> via <strong>CMSIS V1</strong>.</p>
<img src="https://github.com/user-attachments/assets/551afd50-894b-4634-ba9e-a02f31364b89" alt="FreeRTOS" width="624">

<hr>

<h3>Étape 6 — Faites fonctionner le shell</h3>
<p>Le projet est dans le dossier <strong>Shell</strong> :</p>
<img src="https://github.com/user-attachments/assets/8c44c48f-9402-4774-bd47-2c54fd7cf134" alt="Shell projet" width="946">

<hr>

<h2>🔵 2. Le GPIO Expander et le VU-Mètre</h2>

<h3>2.1 Configuration</h3>
<p><em>(1. Quelle est la référence du GPIO Expander ?)</em><br>
Le GPIO Expander est le <strong>MCP23S17</strong> et sa datasheet est dans le dossier <strong>Datasheet</strong>.</p>

<p><em>(2. Sur le STM32, quel SPI est utilisé ?)</em></p>
<img src="https://github.com/user-attachments/assets/3e514302-aa08-4476-8c48-a7a9a316898a" alt="SPI configuration" width="800">
<img src="https://github.com/user-attachments/assets/29e93bea-73fe-4a36-8c33-0d3e4cb3a556" alt="SPI configuration zoom" width="400">

<p>C'est donc le <strong>SPI3</strong> et nous le configurons sur CubeIDE :</p>
<img src="https://github.com/user-attachments/assets/a63aaa8f-a0f3-4909-8431-63d5fbe38934" alt="CubeIDE SPI3" width="600">

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

</body>
</html>