Readme de TPGA-Majeur
Pour ouvrir Riscfree : [niosv-shell] C:\Users\Antle\Documents\FPGA_Majeur\tp_nios_v> C:\altera_lite\25.1std\riscfree\RiscFree\RiscFree.exe
<img width="947" height="608" alt="image" src="https://github.com/user-attachments/assets/b8689042-48e6-4b7b-8ed7-d1c590e6b92c" />
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

            // On écrit la valeur sur le PIO
            IOWR_ALTERA_AVALON_PIO_DATA(PIO_0_BASE, val);

            //printf("dans la boucle");

            // Attente de 200ms pour voir le mouvement
            usleep(200000);
        }
    }

    return 0;
}
```

https://github.com/user-attachments/assets/40483c28-0fdc-4462-9079-2f6aeb9b5ec9


