import paramiko
import sys

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

host = input('Введите айпи NGAFа:\n> ')
user = input('Введите имя пользователя:\n> ')
password = input('Введите пароль:\n> ')
port = input('Введите ssh порт:\n> ')

ssh_client.connect(hostname=host,port=port,username=user,password=password)

print(''.join(ssh_client.exec_command("show ip route")[1].readlines()))

action = input('Добавить (add) (по умолчанию)  или удалить (del) маршрут?\n> ')
if (action != 'add') and (action != 'del'):
    print('Неверная операция')
    sys.exit(1)
    
route_to = input('Введите сеть назначения (формат x.x.x.x/y или x.x.x.x/y.y.y.y):\n> ')
route_via = input ('Введите ip-адрес шлюза:\n> ')
iface = input('Введите интерфейс (не знаете или не уверены - указывайте auto):\n> ')
metric = input('Введите метрику (0-255):\n> ')

if (action == 'add'):
    ssh_client.exec_command("config\n ip route {0} {1} interface {2} metric {3}".format(route_to, route_via, iface, metric))[1].readlines()
elif (action == 'del'):
    ssh_client.exec_command("config\n no ip route {0} {1} interface {2} metric {3}".format(route_to, route_via, iface, metric))[1].readlines()

input('Настройка завершена. Нажимите Enter для выхода')

stdin.close()
stdout.close()
ssh_client.close()
