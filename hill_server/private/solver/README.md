# Análise inicial

O algoritmo customizado usado é o Hill Cipher. A chave é uma matriz $$n \times n$$. Na encriptação, ele divide a entrada em blocos de $$n$$ bytes, e trata cada bloco como vetor e encripta multiplicando pela matriz. Para decriptar, ele multiplica pela inversa.

A comunicação, pelo enunciado, é de um servidor web, então a parte encriptada é do protoclo HTTP.

# Vulnerabilidade 

O Hill Cipher é vulnerável a known-plaintext-attacks (vide https://colab.research.google.com/drive/16muraSRMefM3MLfWn8-jU0XkYgGl4gZ7?usp=sharing). Como o protocolo é conhecido, e com base na informação do domínio, é possível descobrir o conteúdo inicial das mensagens. Em especial, é possível deduzir que a primeira mensagem enviada é:

`GET / HTTP/VERSAO\r\nHOST: headquarter.secure.hill\r\nUser-Agent: `

E a resposta disso começa com:

`HTTP/VERSAO2 200 OK\r\n`

VERSAO e VERSAO2 podem assumir os valores '1.0', '1.1' e '2'. É só brutar essas combinações. Com esses plaintexts conhecidos, é possível quebrar o Hill Cipher e descobrir a chave, e então decriptar a resposta da última comunicação, que revela a flag.

