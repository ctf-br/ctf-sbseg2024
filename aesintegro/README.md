# AES Integro

* Autor: [@brun0-matheus](https://github.com/brun0-matheus)
* Categoria: crypto + pwn
* Dificuldade esperada: difícil

## Enunciado

Um espião infiltrado na sede da OHM obteve acesso físico a um servidor e consegue sobrescrever
o programa inicial executado nele. Entretanto, a OHM tem uma medida de segurança: 
só são executados binários que foram encriptados com uma chave secreta, que ninguém mais, além deles, conhece.

O espião conseguiu descobrir qual foi o algoritmo de criptografia usado, mas ele não entende bulhufas,
então ele te mandou o código, assim como o binário que é executado quando o servidor inicia e também a 
sua versão encriptada.

Para facilitar o exploit, o infiltrado deixou um Arduino conectado à internet para você mandar o 
binário adulterado, e o Arduino cuida de sobrescrever no servidor e te dar acesso a ele.

Acesse com `nc aesintegro.challenges.cfd 5000`

### Anexos


## Flag

Está na pasta server (tá em um arquivo com nome zoado para evitar que os participantes adivinhem o nome 
do arquivo).

