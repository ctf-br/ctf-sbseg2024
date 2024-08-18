# Análise inicial

A imagem dada não nos diz muita coisa, o que talvez nos faça pensar em esteganografia.
Ao olhar o arquivo enc.py nos deparamos com um código que faz uma cópia da imagem, e na função enc quando a altura e largura do pixel são divisiveis por 11 e o valor do byte G do pixel RGB é par, um bit da flag é inserido no valor do byte B do pixel, caso o bit da flag seja 0, ele força B a ser par, e caso o bit da flag seja 1, ele força B a ser ímpar, por fim ele delimita que após todos os bits da flag serem completamente inseridos, ele coloca um pixel final de valor (137, 137, 137).

# Resolução

Basta fazermos um programa que abre a imagem um forma de matriz com a biblioteca de python que nos foi passada, e quando o pixel tiver altura e largura divisiveis por 11 e 'G' par nós extraimos 0 caso B seja par e '1' caso B seja ímpar, até atingir o pixel (137, 137, 137).

Com isso obtemos `010000110101010001000110001011010100001001010010011110110101011100110000011101110101111100110101011101000011001101100111011000010110111000110000011001110111001000110100011100000110100000110111010111110011000101110011010111110011010001010111001100110101001100110000011011010110010101111101`

Convertendo de binário para ascii obtemos a flag:

`CTF-BR{W0w_5t3gan0gr4ph7_1s_4W3S0me}`
