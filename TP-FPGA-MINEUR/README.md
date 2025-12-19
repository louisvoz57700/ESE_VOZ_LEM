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

**Chenillard**


Gestion des encodeurs

### 3. Simulation
Gestion des encodeurs
- Création de testbenches.
- ![WhatsApp Image 2025-12-12 à 11 29 12_fdd79241](https://github.com/user-attachments/assets/3e0310cd-c0f9-460c-9311-552607601bd9)

- <img width="2212" height="864" alt="image" src="https://github.com/user-attachments/assets/03ddea3f-9e36-49ce-a7e2-ec6fecb05e71" />
```VHDL
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
```
Sur Modelsim :
<img width="2338" height="194" alt="image" src="https://github.com/user-attachments/assets/3843c69e-5392-47f0-a00e-400f1df53125" />

- Vérification fonctionnelle.
- Avec encodeur, il compte en binaire

```VHDL
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity encodeur is
    generic (
        C_WIDTH : integer := 10
    );
    port (
        i_clk        : in std_logic;
        i_rst_n      : in std_logic;
        i_a          : in std_logic;
        i_b          : in std_logic;
        o_led_vector : out std_logic_vector(C_WIDTH-1 downto 0) 
    );
end entity encodeur;

architecture rtl of encodeur is
    signal r_a_curr, r_a_prev : std_logic;
    signal r_b_curr, r_b_prev : std_logic;
    signal r_counter : unsigned(C_WIDTH-1 downto 0) := (others => '0');

    -- Signaux pour l'anti-rebond (Debounce)
    -- On veut échantillonner environ toutes les 2ms.
    -- Horloge 50MHz = 20ns. 
    -- 2ms / 20ns = 100 000 cycles.
    constant C_DEBOUNCE_LIMIT : integer := 100000; 
    signal r_debounce_cnt     : integer range 0 to C_DEBOUNCE_LIMIT := 0;
    signal r_tick_enable      : std_logic := '0';

begin

    -------------------------------------------------------------------------
    -- 1. GÉNÉRATEUR DE TICK (Anti-Rebond)
    -- Ce process crée une impulsion 'r_tick_enable' toutes les 2ms.
    -------------------------------------------------------------------------
    process(i_clk, i_rst_n)
    begin
        if i_rst_n = '0' then
            r_debounce_cnt <= 0;
            r_tick_enable  <= '0';
        elsif rising_edge(i_clk) then
            if r_debounce_cnt = C_DEBOUNCE_LIMIT then
                r_debounce_cnt <= 0;
                r_tick_enable  <= '1'; -- On autorise la lecture
            else
                r_debounce_cnt <= r_debounce_cnt + 1;
                r_tick_enable  <= '0';
            end if;
        end if;
    end process;

    -------------------------------------------------------------------------
    -- 2. LOGIQUE ENCODEUR (Synchronisée sur le Tick)
    -------------------------------------------------------------------------
    process(i_clk, i_rst_n)
    begin
        if i_rst_n = '0' then
            r_counter <= (others => '0');
            r_a_curr <= '0'; r_a_prev <= '0';
            r_b_curr <= '0'; r_b_prev <= '0';
            
        elsif rising_edge(i_clk) then
            
            -- ON NE FAIT RIEN TANT QUE LE TICK N'EST PAS LA
            if r_tick_enable = '1' then
            
                -- On capture les entrées UNIQUEMENT à ce moment là
                r_a_curr <= i_a; r_a_prev <= r_a_curr;
                r_b_curr <= i_b; r_b_prev <= r_b_curr;

                -- Logique d'incrémentation
                if (r_a_curr = '1' and r_a_prev = '0' and r_b_curr = '0') or
                   (r_a_curr = '0' and r_a_prev = '1' and r_b_curr = '1') then
                    r_counter <= r_counter + 1;
                
                -- Logique de décrémentation
                elsif (r_b_curr = '1' and r_b_prev = '0' and r_a_curr = '0') or
                      (r_b_curr = '0' and r_b_prev = '1' and r_a_curr = '1') then
                    r_counter <= r_counter - 1;
                end if;
                
            end if; -- Fin du if tick_enable
            
        end if;
    end process;
    
    o_led_vector <= std_logic_vector(r_counter);

end architecture rtl;
```

https://github.com/user-attachments/assets/a947c91c-28af-4d59-b5d8-64f5598171c0



**Contrôleur HDMI**

On refait le fichier hdmi_controler , et on peut donc changer ce qui s'affiche à l'écran :

<img width="1258" height="767" alt="image" src="https://github.com/user-attachments/assets/1c52c30a-5700-435d-8baa-ae291ab9909a" />

Effet à l’écran :


🔴 Rouge varie horizontalement (selon x)

🟢 Vert varie verticalement (selon y)

🔵 Bleu est constant à 0

➡️ On obtient un dégradé rouge/vert, noir en bleu.

## Déplacement d'un pixel



https://github.com/user-attachments/assets/c5d05790-0866-4dea-bc2f-7f806b71dd6d

```VHDL
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity hdmi_controler is
    generic (
        H_RES : natural := 720;
        V_RES : natural := 480
    );
    port (
        i_clk   : in  std_logic;  -- horloge pixel 27 MHz
        i_rst_n : in  std_logic;
		  i_X : in natural;
		  i_Y : in natural;

        -- HDMI output
        o_hdmi_tx_clk : out std_logic;
        o_hdmi_tx_d   : out std_logic_vector(23 downto 0);
        o_hdmi_tx_de  : out std_logic;
        o_hdmi_tx_hs  : out std_logic;
        o_hdmi_tx_vs  : out std_logic
    );
end entity hdmi_controler;

architecture rtl of hdmi_controler is

    -- Timings 480p (720x480 @ 60 Hz)
    constant H_FP    : natural := 16;
    constant H_PW    : natural := 62;
    constant H_BP    : natural := 60;
    constant H_TOTAL : natural := H_RES + H_FP + H_PW + H_BP;

    constant V_FP    : natural := 9;
    constant V_PW    : natural := 6;
    constant V_BP    : natural := 30;
    constant V_TOTAL : natural := V_RES + V_FP + V_PW + V_BP;

    signal h_cnt : natural range 0 to H_TOTAL-1 := 0;
    signal v_cnt : natural range 0 to V_TOTAL-1 := 0;

    signal de_int : std_logic;

begin

    ------------------------------------------------------------------
    -- Horloge pixel HDMI
    ------------------------------------------------------------------
    o_hdmi_tx_clk <= i_clk;

    ------------------------------------------------------------------
    -- Compteurs horizontal / vertical
    ------------------------------------------------------------------
    process(i_clk)
    begin
        if rising_edge(i_clk) then
            if i_rst_n = '0' then
                h_cnt <= 0;
                v_cnt <= 0;
            else
                if h_cnt = H_TOTAL-1 then
                    h_cnt <= 0;
                    if v_cnt = V_TOTAL-1 then
                        v_cnt <= 0;
                    else
                        v_cnt <= v_cnt + 1;
                    end if;
                else
                    h_cnt <= h_cnt + 1;
                end if;
            end if;
        end if;
    end process;

    ------------------------------------------------------------------
    -- Synchronisations HDMI
    ------------------------------------------------------------------
    o_hdmi_tx_hs <= '0'
        when (h_cnt >= H_RES + H_FP and h_cnt < H_RES + H_FP + H_PW)
        else '1';

    o_hdmi_tx_vs <= '0'
        when (v_cnt >= V_RES + V_FP and v_cnt < V_RES + V_FP + V_PW)
        else '1';

    ------------------------------------------------------------------
    -- Data Enable (zone visible)
    ------------------------------------------------------------------
    de_int <= '1' when (h_cnt < H_RES and v_cnt < V_RES) else '0';
    o_hdmi_tx_de <= de_int;

    ------------------------------------------------------------------
    -- Génération des pixels
    -- fond blanc + carré noir 10x10
    ------------------------------------------------------------------
    o_hdmi_tx_d <=
        -- carré noir
        (others => '0')
            when (de_int = '1' and
                  h_cnt >= i_X and h_cnt < i_X + 5 and
                  v_cnt >= i_Y and v_cnt < i_Y +5 ) else

        -- fond blanc
        (x"FF" & x"FF" & x"FF")
            when de_int = '1' else

        -- hors zone active
        (others => '0');

end architecture rtl;
```
## Mémoriser 
- Expliquez ce qu'est une mémoire dual-port :
  une mémoire qui possède deux entrées/sorties indépendantes.
- Proposer un schéma pour mémoiriser les pixels.
- <img width="2036" height="1496" alt="image" src="https://github.com/user-attachments/assets/222e6982-c690-4ee3-bb74-2d62ec075ce2" />


## 📂 Arborescence du projet
