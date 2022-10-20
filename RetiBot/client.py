from socket import *
serverName = 'localhost'
serverPort = 120
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket .connect((serverName, serverPort))
sentence = input('Input lowercase sentence: ')
clientSocket.send(sentence.encode()) #invia il messaggio di input al server
modifiedSentence = clientSocket.recv(1024) #1024 grandezza dei byte
print('From Server: ', modifiedSentence.decode()) #mostra il messaggio modificato dal server
clientSocket.
clientSocket.close()