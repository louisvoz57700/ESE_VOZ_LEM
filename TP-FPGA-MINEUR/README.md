# 📝 README — TP FPGA  
**Auteurs :** Antoine Lemarignier, Louis Vozzzola

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
![WhatsApp Image 2025-12-12 à 10 37 48_b3b67c9f](https://github.com/user-attachments/assets/885d98dc-a522-4058-8c69-d7e5c6610f5b)

La clock FPGA_CLK1_50 est une 50MHz, et elle est placé sur le pin V11.
![alt text](/TP-FPGA-MINEUR/IMG/image.png)

![alt text](/TP-FPGA-MINEUR/IMG/image-1.png)
![WhatsApp Image 2025-12-12 à 10 37 48_571fd5b2](https://github.com/user-attachments/assets/ff54ca97-e1a9-49d1-bf60-13e0ae75aa39)


6. On peut réaliser 

7. On peut réaliser une première ébauche du compteur :


8. 
![alt text](image.png)


11. Le _n dans i_rst_n représente negated. Donc par défault il est inversé. Pour l'activer, il faut i_rst_n = 0.

Gestion des encodeurs

### 3. Simulation
- Création de testbenches.
- ![WhatsApp Image 2025-12-12 à 11 29 12_fdd79241](https://github.com/user-attachments/assets/3e0310cd-c0f9-460c-9311-552607601bd9)

- <img width="2212" height="864" alt="image" src="https://github.com/user-attachments/assets/03ddea3f-9e36-49ce-a7e2-ec6fecb05e71" />
'''VHDL
library ieee;
use ieee.std_logic_1164.all;

entity edge_detector is
    port (
        i_clk : in  std_logic;
        i_a   : in  std_logic;  --  A
        o_e   : out std_logic   --  E
    );
end entity edge_detector;

architecture rtl of edge_detector is
    signal r1_curr : std_logic := '0'; 
    signal r2_prev : std_logic := '0'; --  'b' 

begin
    process(i_clk)
    begin
        if rising_edge(i_clk) then
            r1_curr <= i_a;      
            r2_prev <= r1_curr;  
        end if;
    end process;
	 
    o_e <= r1_curr xor r2_prev;

end architecture rtl;
'''

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
