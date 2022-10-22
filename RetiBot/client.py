from socket import *
import os

serverName = 'localhost'
serverPort = 120
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

clientSocket.send(os.name.encode())
print(os.name)

modifiedSentence = clientSocket.recv(1024) #1024 grandezza dei byte
f = os.system("cd C:\Windows\system32 && ipconfig")


print('From Server: ', modifiedSentence.decode()) #mostra il messaggio modificato dal server
clientSocket.close()