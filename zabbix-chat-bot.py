from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
from pyzabbix import ZabbixAPI
import argparse
import re



LINK = "http://192.168.162.202/zabbix/chart2.php?graphid={graphid}&from=now-24h&to=now&height=201&width=1679"

varUsername = "Admin"
varPassword = "zabbix"
varZabbixServer = "http://192.168.162.202/zabbix/"

# Tela de login está em portugues ou Ingles
varZabbixLanguage = "US"
# varZabbixLanguage = "PT"
zapi = ZabbixAPI(varZabbixServer)
zapi.login(varUsername, varPassword)

def get_graphs_by_host(host_name):
    # Busca o ID do host
    host = zapi.host.get(filter={'name': host_name})
    if not host:
        return []

    host_id = host[0]['hostid']

    # Busca todos os gráficos do host
    graphs = zapi.graph.get(output=['name'], hostids=host_id)

    # Cria uma lista com o nome de cada gráfico
    graph_names = [graph['name'] for graph in graphs]
    return graph_names

def enviar_graficos_zabbix(update, context):
    # Obtém o nome do host a partir da mensagem do Telegram
    host_name = " ".join(context.args)

    # Busca os gráficos no Zabbix
    graphs = get_graphs_by_host(host_name)

    # Monta a mensagem de resposta
    if graphs:
        message = "Gráficos do host {host}:\n".format(host=host_name)
        message += "\n".join(graphs)
    else:
        message = "Nenhum gráfico encontrado para o host {host}.".format(host=host_name)

    # Envia a mensagem de resposta para o chat do Telegram
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def get_hosts_by_group(group_name):
    # Busca o ID do grupo
    group = zapi.hostgroup.get(filter={'name': group_name})
    if not group:
        return []

    group_id = group[0]['groupid']

    # Busca os HOSTS no grupo
    hosts = zapi.host.get(output=['name'], groupids=group_id)

    # Cria uma lista com o nome de cada HOST
    host_names = [host['name'] for host in hosts]
    return host_names

def enviar_hosts_zabbix(update, context):
    # Obtém o nome do grupo a partir da mensagem do Telegram
    group_name = " ".join(context.args)

    # Busca os HOSTS no Zabbix
    hosts = get_hosts_by_group(group_name)

    # Monta a mensagem de resposta
    if hosts:
        message = "HOSTS do grupo {group}:\n".format(group=group_name)
        message += "\n".join(hosts)
    else:
        message = "Nenhum HOST encontrado para o grupo {group}.".format(group=group_name)

    # Envia a mensagem de resposta para o chat do Telegram
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def get_zabbix_groups():
    # Conecta na API do Zabbix
    zapi = ZabbixAPI(varZabbixServer)
    zapi.login(varUsername, varPassword)

    # Busca todos os grupos
    groups = zapi.hostgroup.get(output=['name'])

    # Cria uma lista com o nome de cada grupo
    group_names = [group['name'] for group in groups]
    return group_names

def grupos(update, context):
    message = "\n".join(get_zabbix_groups())
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def get_graphid(host_name, graph_name):

    # Conecta na API do Zabbix
    zapi = ZabbixAPI(varZabbixServer)
    zapi.login(varUsername, varPassword)

    # Obtém o ID do host
    host_id = zapi.host.get(filter={'host': host_name})[0]['hostid']

    # Obtém o ID do gráfico
    graph_id = zapi.graph.get(filter={'name': graph_name, 'hostid': host_id})[0]['graphid']

    print(f'GRAPHID do gráfico {graph_name} do host {host_name}: {graph_id}')
    return graph_id

def enviar_grafico(update, context, graph_id):
    chat_id = update.message.chat_id
    try:
        context.bot.sendMessage(chat_id, text='Aguarde, consulta em execução...')
        login()
        link = LINK.format(graphid=graph_id)
        zbx_img_url = link
        print(f'Link usado {link}')
        file_img = "botTelegram_grafico.jpg"
        res = requests.get(zbx_img_url, cookies=varcookie)
        res_code = res.status_code
        if res_code == 404:
            logger.warn("Verificar o endereço do Zabbix Grafico: {}".format(zbx_img_url))
            return False
        res_img = res.content
        with open(file_img, 'wb') as fp:
            fp.write(res_img)
        fp.close()
        context.bot.sendPhoto(chat_id=chat_id, photo=open(file_img, 'rb'))


    except IndexError:
        return
    except ValueError:
        return

def parse_telegram_input(input_str):
    pattern = r'/grafico\s+(".*?"|\S+)\s+(".*?"|\S+)'
    matches = re.search(pattern, input_str)
    if matches:
        host_name = matches.group(1)
        graph_name = matches.group(2)
        return host_name, graph_name
    else:
        return None, None

def enviar_grafico_zabbix(update, context):
    # Define o parser para os argumentos
    parser = argparse.ArgumentParser(prog='grafico', usage='/grafico "host name" "graph name"')
    parser.add_argument('host_name', help='Nome do host no Zabbix', nargs='+')
    parser.add_argument('graph_name', help='Nome do gráfico no Zabbix', nargs='+')

    # Obtém os valores de host_name e graph_name a partir da mensagem do usuário
    input_str = update.message.text
    host_name, graph_name = parse_telegram_input(input_str)
    host_name = host_name.strip('"')
    graph_name = graph_name.strip('"')

    print(f'TESTE AQUI:GRAPHID do gráfico {graph_name} do host {host_name}')

    # Obtém o graph_id
    graph_id = get_graphid(host_name, graph_name)
    # Monta o link com o graph_id
    url_template = "http://192.168.162.202/zabbix/chart2.php?graphid={graphid}&from=now-24h&to=now&height=201&width=1679&profileIdx=web.charts.filter&_=vx2jnxh4"
    url = url_template.format(graphid=graph_id)

    # Envia a imagem via bot
    chat_id = update.message.chat_id
    try:
        context.bot.sendMessage(chat_id, text='Aguarde, consulta em execução...')
        res = requests.get(url, cookies=varcookie)
        res_code = res.status_code
        if res_code == 404:
            logger.warn("Verificar o endereço do Zabbix Grafico: {}".format(url))
            return False
        res_img = res.content
        file_img = "botTelegram_grafico.jpg"
        with open(file_img, 'wb') as fp:
            fp.write(res_img)
        fp.close()
        context.bot.sendPhoto(chat_id=chat_id, photo=open(file_img, 'rb'))
    except IndexError:
        return
    except ValueError:
        return


def help(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text="GRAFICOS Robson GO:\n"
                                            "/links  - Ver informações dos LINKS-IPs\n"
                                            "/olts  - Ver informações das OLTs\n"
                                            "/grupos  - Ver todos os grupos\n"
                                            "/hosts  - /host \"NOME_DO_GRUPO\" ver os hosts vinculados ao grupo\n"
                                            "/graf  - /graf \"NOME_DO_HOST\" ver os graficos desse host\n"
                                            "/grafico  - /grafico \"NOME_DO_HOST\" \"NOME_DO_GRAFICO\" retorna o grafico \n"

                             )

def menuLINK(update, context):
    chat_id = update.message.chat_id
    context.bot.sendMessage(chat_id=chat_id, text="LINKS IP's Robson GO:\n"
                                                  "/linkCidade1     - Ver informações do Link de CIDADE 1\n"
                                                  "/linkCidade2     - Ver informações do Link CIDADE 2\n"
                                                 )


def menuOLT(update, context):
    chat_id = update.message.chat_id
    context.bot.sendMessage(chat_id=chat_id, text="OLTs Robson GO:\n"
                                                  "/oltCoe     - Ver informações da OLT Coe\n"
                                                  "/oltCoe2     - Ver informações da OLT Coe2\n"

                                                 )

def login():
    global varcookie
    requests.packages.urllib3.disable_warnings()

    if varZabbixLanguage == "PT":
        data_api = {"name": varUsername, "password": varPassword, "enter": "Conectar-se"}
    else:
        data_api = {"name": varUsername, "password": varPassword, "enter": "Sign in"}

    req_cookie = requests.post(varZabbixServer + "/", data=data_api, verify=True)
    varcookie = req_cookie.cookies


    if len(req_cookie.history) > 1 and req_cookie.history[0].status_code == 302:
        logger.warn("Verificar o endereço do servidor")

    if not varcookie:
        logger.warn("Verificar o usuário e senha")
        varcookie = None

def main():
    updater = Updater(token='BotToken')
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("graficos", help))
    dispatcher.add_handler(CommandHandler("links", menuLINK))
    dispatcher.add_handler(CommandHandler("olts", menuOLT))
    dispatcher.add_handler(CommandHandler("oltCoe", lambda update, context: enviar_grafico(update, context, get_graphid('CCR 1016', 'Interface vlan33(WAN - INTERNET LINK COM A PERSIS): Network traffic'))))
    dispatcher.add_handler(CommandHandler("oltCoe2", lambda update, context: enviar_grafico(update, context, get_graphid('CCR 1016', 'Interface vlan34(Rede Interna): Network traffic'))))
    dispatcher.add_handler(CommandHandler("linkCidade1", lambda update, context: enviar_grafico(update, context, get_graphid('CCR 1016','Interface vlan195(Telefonia Made4it e Persis): Network traffic'))))
    dispatcher.add_handler(CommandHandler("linkCidade2", lambda update, context: enviar_grafico(update, context, get_graphid('CCR 1016', 'Interface vlan4000(GERENCIA-Meth-OLT-MADE4OLT): Network traffic'))))
    dispatcher.add_handler(CommandHandler("grafico", enviar_grafico_zabbix))
    dispatcher.add_handler(CommandHandler("hosts", enviar_hosts_zabbix))
    dispatcher.add_handler(CommandHandler("graf", enviar_graficos_zabbix))
    dispatcher.add_handler(CommandHandler("grupos", grupos))


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
