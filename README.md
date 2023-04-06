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

## DockerFile

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
