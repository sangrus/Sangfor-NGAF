import paramiko
import sys

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

host = input('Введите айпи NGAFа:\n> ')
user = input('Введите имя пользователя:\n> ')
password = input('Введите пароль:\n> ')
port = input('Введите ssh порт:\n> ')

ssh_client.connect(hostname=host,port=port,username=user,password=password)

print(''.join(ssh_client.exec_command("show interface")[1].readlines()))

iface = input('Выберите интерфейс:\n> ')
action = input('Добавить (add) или удалить (del) айпи?\n> ')
if (action != 'add') and (action != 'del'):
    print('Неверная операция')
    sys.exit(1)
ip = input('Введите айпи (формат x.x.x.x/y или x.x.x.x/y.y.y.y):\n> ')

while 1:
	wan = input('Это WAN интерфейс? (y/n):\n> ').lower()
	if (wan == 'y'):
		wan = 'enable'
		ssh_client.exec_command("config\n interface {0}\n wan {1}".format(iface, wan))[1].readlines()
		break
	elif (wan == 'n'):
		wan = 'disable'
		ssh_client.exec_command("config\n interface {0}\n wan {1}".format(iface, wan))[1].readlines()
		break
	else:
		print('Попробуйте ещё раз')

if (action == 'add'):
    ssh_client.exec_command("config\n interface {0}\nip address {1}\n wan {2}".format(iface, ip, wan))[1].readlines()
elif (action == 'del'):
    ssh_client.exec_command("config\n interface {0}\n no ip address {1}".format(iface, ip))[1].readlines()

input('Настройка завершена. Нажимите Enter для выхода')

stdin.close()
stdout.close()
ssh_client.close()
