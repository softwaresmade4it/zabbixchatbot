import paramiko
import sys

# Recebendo as informações do usuário
username = sys.argv[1]
password = sys.argv[2]
ip = sys.argv[3]
modelo = sys.argv[4]

# Função para executar o comando de reboot no Mikrotik
def reboot_mikrotik(ssh):
    ssh.exec_command("/system reboot")

# Conexão SSH no equipamento Mikrotik
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=ip, username=username, password=password)

# Verificando o modelo do Host e executando a função correspondente
if modelo == "Mikrotik":
    reboot_mikrotik(ssh)
else:
    print("Modelo de Host inválido.")

# Fechando a conexão SSH
ssh.close()


