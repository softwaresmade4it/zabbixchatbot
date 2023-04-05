# Zabbix-Chat-Bot

Zabbix Chat Bot, é um script em python que é utilizado como um intermediário entre o Telegram (bot) e o Zabbix que iremos coletar as informações


## Variáveis

|Variável  | Exemplo |  Descrição |
|--|--|--|
| LINK | http://192.168.162.202/zabbix/chart2.php?graphid={graphid}&from=now-24h&to=now&height=201&width=1679 |IP ou dominio de Acesso ao FrontEnd Do zabbix |
|varPassword | zabbix | Senha do user que tem acesso a API do Zabbix |
|varZabbixServer | http://192.168.162.202/zabbix/ | IP de Acesso ao FrontEnd Do zabbix|
| url_template | http://192.168.162.202/zabbix/chart2.php?graphid={graphid}&from=now-24h&to=now&height=201&width=1679&profileIdx=web.charts.filter&_=vx2jnxh4 | IP ou dominio de Acesso ao FrontEnd Do zabbix |


## DockerFile
To use a Zabbix Bot in container use a Dockerfile. Let's start by build an image :

Para utilizar o Zabbix Chat bot em um container usando o DockerFile, primeiro temosq ue buildar a imagem:
PS: Antes de executar os comandos tenha certeza que os arquivos desse repositório estão no diretório atual

```sh
docker build -t zabbix-chat-bot .
```

Agora basta iniciar o nosso container
```sh
docker container run -d zabbix-bot
```
