# AES CBC Bit flipping

Na decriptação, sendo $$P_i$$ o bloco do plaintext $i$ (1-indexado) e $$C_i$$ o do ciphertext,
tem-se que $$P_i = \text{AES-DEC}(C_i) \oplus C_{i-1}$$, sendo que $$C_0$$ é o IV.

Com isso, o atacante consegue modificar o bloco $$C_{i-1}$$ para então manipular o resultado
que o servidor vai obter na decriptação do bloco $$P_i$$, embora isso vá zoar o bloco $$P_{i-1}$$
de maneira irremediável.

Mais especificamente, seja $$O_i$$ o conteúdo original do bloco $$i$$, e $$T_i$$ o que o atacante quer
por no lugar. Então, ao enviar $$C'_{i-1} = C_{i-1} \oplus O_i \oplus T_i$$ no lugar de $$C_{i-1}$$, 
o servidor vai obter o bloco 
$$P_i = (\text{AES-DEC}(C_i) \oplus C_{i-1}) \oplus O_i \oplus T_i = O_i \oplus O_i \oplus T_i = T_i$$.

# Usando isso para explorar o binário

O atacante consegue então controlar alguns blocos do binário, mas não todos (ao mesmo tempo). No caso, ele
consegue formar uma cadeia de blocos ruins com blocos bons. Mas, como é um binário, ele pode fazer isso em 
blocos de instruções, e no final de um bloco bom pular para o próximo bloco bom, ignorando assim os blocos ruins.
O problema é que não dá para ignorar o primeiro bloco ruim dessa forma, mas isso pode ser contornado colocando o 
primeiro bloco bom no começo de uma função tal que o bloco ruim fique num outro trecho que (talvez) nunca seja chamado.

Olhando no ghidra, é possível ver que é possível fazer isso na função `check_password`, pois antes dela tem apenas as
funções de `print_uptime` e `print_if_system_is_on`, que, como vamos por um shellcode para chamar a shell, nunca serão 
chamadas.

