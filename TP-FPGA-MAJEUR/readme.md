Readme de TPGA-Majeur


# Tutoriel Nios V
L'une des choses les plus importantes a été de bien respecter toutes les étapes du tutoriel.
Nous avons eu du mal au début avec Riscfree car il était introuvable à partir du shell. Cependant, en partant du shell nous sommes arrivé à lancer Riscfree depuis le terminal.
```
[niosv-shell] C:\Users\Antle\Documents\FPGA_Majeur\tp_nios_v> C:\altera_lite\25.1std\riscfree\RiscFree\RiscFree.exe
```
Puis nous avons pu mettre le premier code dans le NIOS V qui consisté seulement à écrire un "Hello, world!" dans le terminal.

<img width="947" height="608" alt="image" src="https://github.com/user-attachments/assets/b8689042-48e6-4b7b-8ed7-d1c590e6b92c" />

Maintenant que nous arrivons à programmer le NIOS V, nous pouvons refaire le chenillard :

```VHDL
#include <stdio.h>
#include <unistd.h>
#include "system.h"
#include "altera_avalon_pio_regs.h"

int main(void)
{
    //printf("Début du chenillard sur les 10 LEDs...\n");

    while(1)
    {
        for (int i = 0; i < 10; i++)
        {
            int val = (1 << i);

            IOWR_ALTERA_AVALON_PIO_DATA(PIO_0_BASE, val);

            usleep(200000);
        }
    }

    return 0;
}
```
<video controls src="533306539-40483c28-0fdc-4462-9079-2f6aeb9b5ec9.mp4" title="Title"></video>

Par manque de temps, nous n'avons pas pu aller plus loin dans le TP.