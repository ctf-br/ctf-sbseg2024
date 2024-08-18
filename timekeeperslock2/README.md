# Timekeeper's Lock v2

* Autor: [@thotypous](https://github.com/thotypous)
* Categoria: hardware + reversing
* Dificuldade esperada: difícil

## Enunciado

O pessoal da OHM sempre critica os CTFs, dizendo que eles não têm nada a ver com o mundo real, mas isso parece ser hipocrisia.

Descobrimos que a OHM adaptou o código de um [desafio de CTF antigo](https://github.com/epicleet/timekeeperslock) e passou a utilizá-lo para controlar as fechaduras eletrônicas de seus prédios. Segundo nosso informante, eles apenas trocaram a chave criptográfica e migraram para um FPGA mais novo — o **LFE5U-25F-6BG256C**.

Os pinos do FPGA estão conectadas ao circuito da seguinte forma:

 * `P6` — `CLK`, entrada de clock de 29.4912 MHz
 * `M13` — `RST_N`, entrada que reseta o circuito no nível lógico baixo
 * `A15` — `open_lock`, saída que abre a porta no nível lógico alto
 * `F16` — `gps_uart_rx`, entrada que recebe NMEA (`$GPRMC`) de um GPS em UART 115200 8N1
 * `A14` — `keypad_uart_rx`, entrada que recebe ASCII de cada tecla pressionada em um teclado hexadecimal em UART 115200 8N1

Faça engenharia reversa do bitfile fornecido como anexo e descubra a sequência hexadecimal que deve ser digitada no teclado para abrir a porta **agora** (dia, mês, ano, hora e minuto atuais). Acesse o link https://door.challenges.cfd/SEQUENCIA para receber a flag.

### Anexos


## Flag

Vide código do server
