# Zabbix-Chat-Bot

Zabbix Chat Bot, é um script em python que é utilizado como um intermediário entre o Telegram (bot) e o Zabbix que iremos coletar as informações


## Variáveis

|Variável  | Exemplo |  Descrição |
|--|--|--|
| LINK | http://192.168.162.202/zabbix/chart2.php?graphid={graphid}&from=now-24h&to=now&height=201&width=1679 |IP ou dominio de Acesso ao FrontEnd Do zabbix |
|varZabbixServer | http://192.168.162.202/zabbix/ | IP de Acesso ao FrontEnd Do zabbix|
| url_template | http://192.168.162.202/zabbix/chart2.php?graphid={graphid}&from=now-24h&to=now&height=201&width=1679&profileIdx=web.charts.filter&_=vx2jnxh4 | IP ou dominio de Acesso ao FrontEnd Do zabbix |
| token | BotToken | Token do Bot do Telegram  |
| varPassword | zabbix | Senha do user que tem acesso a API do Zabbix |
| varUsername | Admin | Nome do user que tem acesso a API do Zabbix |

## SystemD

Para utilizar o script como um serviço no systemd:

- Mova o arquivo zabbix-chat-bot.py para  /usr/lib/zabbix/alertscripts/
``` sh
mv  zabbix-chat-bot.py /usr/lib/zabbix/alertscripts/
```
- Instalar dependências:

Debian:
```sh 
# apt install python3-pip python-urllib3
# pip install -r requeriments.txt 
```
-  Edite o script e alimente as variáveis

- Crie um serviço no systemd para deixar o script em execução:
```sh
vim /etc/systemd/system/zabbix-chat-bot.service 
```

Conteudo:
```sh
[Unit]
Description=Python Script Zabbix Chat Bot
[Service]
Type=simple
ExecStart=/usr/bin/python3 /usr/lib/zabbix/alertscripts/zabbix-chat-bot.py
Restart=on-abort
[Install]
WantedBy=multi-user.target
```

- De a permissão de execução no service
```sh
# chmod a+x /etc/systemd/system/zabbix-chat-bot.service
```

- Ative o script para executar com o sistema e inicie ele
```sh
# systemctl daemon-reload
# systemctl enable --now zabbix-chat-bot.service
```
- Para validar se executou corretamente, valide o status do serviço
```sh
# systemctl status zabbix-chat-bot
```


## DockerFile

Para instalar o Docker
```sh
curl -fsSL https://get.docker.com/ | bash
```

Para utilizar o Zabbix Chat bot em um container usando o DockerFile, primeiro temosq ue buildar a imagem:
PS: Antes de executar os comandos tenha certeza que os arquivos desse repositório estão no diretório atual

```sh
docker build -t zabbix-chat-bot .
```

Agora basta iniciar o nosso container
```sh
docker container run -d zabbix-chat-bot
```

## Funcionamento

As funções:
```python
def help(update, context):
def menuLINK(update, context):
def menuOLT(update, context):
```

Possui qual o 
```python 
text= 
```
que será enviado para o usuário sempre que ele digitar:
```python
dispatcher.add_handler(CommandHandler("help", help))
dispatcher.add_handler(CommandHandler("graficos", help))
dispatcher.add_handler(CommandHandler("links", menuLINK))
dispatcher.add_handler(CommandHandler("olts", menuOLT))
```

Então caso quiser alterar o conteúdo, ou a palavra que vai chamar a função, basta alterar.

### Adicionado Host/Grafico

Para adicionar o gráfico de um hosts manualmente, temos que fazer o seguinte:

 - Garantir que a função que chama o gráfico, contenha o texto que você quer utilizar para exibir o gráfico:
```python
def menuLINK(update, context):
chat_id = update.message.chat_id
context.bot.sendMessage(chat_id=chat_id, text="LINKS IP's Robson GO:\n"
"/linkCidade1 - Ver informações do Link de CIDADE 1\n"
"/linkCidade2 - Ver informações do Link CIDADE 2\n"
)
```

 No caso acima o /linkCidadade1 e /linkCidade2 são os menus que iram chamar alguma função.
 ```python
dispatcher.add_handler(CommandHandler("linkCidade1", lambda update, context: enviar_grafico(update, context, get_graphid('CCR 1016','Interface vlan195(Telefonia Made4it e Persis): Network traffic'))))
dispatcher.add_handler(CommandHandler("linkCidade2", lambda update, context: enviar_grafico(update, context, get_graphid('CCR 1016', 'Interface vlan4000(GERENCIA-Meth-OLT-MADE4OLT): Network traffic'))))
 ```

Agora basta adicionar qual o **HOST** e o **GRÁFICO** que deseja:
No meu caso:

**Host:** CCR 1016
**Gráfico:** Interface vlan4000(GERENCIA-Meth-OLT-MADE4OLT): Network traffic


## Script

### Requisitos

A nova função de script funciona da seguinte forma:

Enviamos o nome do Host e o Nome do Script, via API do zabbix valida se existe o host e script e então executa o script para o host especifico.

Para exemplo criei um script que realiza o reboot do zabbix server (via agent) e reboota um mikrotik (via script ssh).


Primeiro temos que configurar o user do zabbix_server para poder dar comandos em nosso servidor.

- Instale o pacote sudo

Debian:
``` sh
# apt install sudo
```
- Edite o arquivo: /etc/sudoers e permita o zabbix executar comandos sem senha

```sh
# vim /etc/sudoers 
```
Adicione, logo abaixo de **root	ALL=(ALL:ALL) ALL**
```sh
zabbix ALL=(ALL) NOPASSWD:ALL
```
- Vamos dar um shell para o user Zabbix e criar a home dele
```sh
# sudo chsh -s /bin/bash zabbix
# mkdir /var/lib/zabbix/
# chown -R zabbix. /var/lib/zabbix/
```

Para teste você pode instalar o pacote nmap em seu servidor, e testar a execução do script que já existe no Zabbix, que é o: **Detect operating system**

Pois ele utiliza o sudo e o shell para executar o comando e dar o retorno.


### Configuração

Agora precisamos criar nossos scripts no FrontEnd do Zabbix, na versão 6.4 fica em:
Alerts > Script


