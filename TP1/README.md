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
Cela permettra de gérer plusieurs tâches simultanément 
(par ex. clignotement LED + communication série).
</p>

<hr>

<h2>🔵 2. Le GPIO Expander et le VU-Mètre</h2>

<h3>2.1 Configuration</h3>

<p><em>(Section à compléter selon les instructions du TP.)</em><br>
Dans cette partie, on configure le <strong>GPIO Expander</strong> pour piloter le 
<strong>VU-mètre</strong>, en lien avec les entrées/sorties analogiques.
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