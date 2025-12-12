# 📝 README — TP FPGA  
**Auteurs :** Antoine Le Marignier, Louis Vozzzola

## 📌 Présentation du projet
Ce TP a pour objectif de se familiariser avec le développement sur **FPGA**, depuis la description matérielle jusqu’à la synthèse et la mise en œuvre sur carte.

**Matériel et outils utilisés :**
- Carte FPGA : *(à compléter, ex : Basys 3 / Nexys A7 / DE10-Lite...)*
- Langage HDL : *(VHDL / Verilog)*
- Environnement : *(Vivado / Quartus)*

L’objectif principal est d’apprendre à concevoir un circuit numérique, le simuler et le déployer sur FPGA.

---

## 🧩 Contenu du TP

### 1. Premier Test
On suit toute la démarche est on arrive bien éteindre la LED quand on appuie sur le bouton :
<img width="480" height="848" alt="image" src="https://github.com/user-attachments/assets/f406379a-df81-4ad0-8d79-7b6d797983c3" />


On change alors notre en code en mettant not pushl, la led s'allume lorsque l'on appuie sur le bouton.




### 2. Faire clignoter une LED
Voici notre porposition de schéma : 
![WhatsApp Image 2025-12-12 à 10 37 48_c125ae2b](https://github.com/user-attachments/assets/00c05668-78a3-4917-9643-138d6cc16473)

La clock FPGA_CLK1_50 est une 50MHz
Voici ce que propose quartus
![alt text](/TP-FPGA-MINEUR/IMG/image.png)

![alt text](/TP-FPGA-MINEUR/IMG/image-1.png)


Avec réduction de fréquence :
![WhatsApp Image 2025-12-12 à 10 37 48_a5b12a4e](https://github.com/user-attachments/assets/94e73190-fb9f-4d3a-807c-1f922b99e5cf)



### 3. Simulation
- Création de testbenches.
- Vérification fonctionnelle.

### 4. Synthèse & Implémentation
- Synthèse.
- Placement & routage.
- Résolution des warnings/erreurs.

### 5. Téléversement sur FPGA
- Génération du bitstream.
- Programmation de la carte.

### 6. Tests et validation
- Comparaison simulation vs matériel.
- Analyse des écarts éventuels.

---

## 📂 Arborescence du projet
