from socket import *
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM) #AF_INET = IPV4; SOCK_STREAM = TCP
serverSocket.bind( ('localhost',serverPort) )
serverSocket.listen(1)
print('The server is ready to receive')
connectionSocket, addr = serverSocket.accept()
print('Accepted a new client',addr)
uname = connectionSocket.recv(4096).decode()
print(uname)
machine = connectionSocket.recv(1024).decode()
print(machine)
user = connectionSocket.recv(1024).decode()
print(user)
memory = connectionSocket.recv(1024).decode()
print(memory)
fs = connectionSocket.recv(1024).decode()
print(fs)
connectionSocket.send('ok'.encode())
command = ''    
while command != 'exit':
    print('Commands: ls, cd, get [file_name]')
    command = input('Input a command:	')
    if(command == 'ls'):
        connectionSocket.send('ls'.encode())
        ls = connectionSocket.recv(1024).decode()
        cwd = connectionSocket.recv(1024).decode()
        print(ls)
        print('Current working directory:	',cwd)
    if(command == 'exit'):
        connectionSocket.send('exit'.encode())
    if(command.startswith('cd')  and command[1:].strip()):
        string = '1'+command.split(" ")[1]
        connectionSocket.send(string.encode())
        print('New path:	',connectionSocket.recv(1024).decode())
    if(command.startswith('get')  and command[1:].strip()):
        string = '0'+command.split(" ")[1]
        connectionSocket.send(string.encode())
        data = connectionSocket.recv(90000000).decode()
        file = open(string[1:], "w")
        print("Receiving the file data.")
        file.write(data)
        file.close()
connectionSocket.close()
