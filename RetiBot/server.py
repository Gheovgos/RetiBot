from socket import *

serverPort = 120
serverSocket = socket(AF_INET, SOCK_STREAM) #AF inet intende IPv4 SOCK STREAM che TCP
serverSocket.bind(('', serverPort)) #il primno parametro indica da chi puo' ricevere. Lasciato vuoto si intende che tutti possono connettersi
serverSocket.listen(1)
continua = True
print("Il server e' pronto")
while True:

    connectionSocket, addr = serverSocket.accept()  #indica chi e' collegato (addr) tramite IP e la connessione stessa
    print("Accettato un nuovo cliente", addr)

    OS = connectionSocket.recv(1024).decode() #riceve il messaggio dal client, decode serve per trasformare il messsaggio indipendente dalla macchina
    if OS == "nt":
        OS = "Windows"
    print("Sistema operativo in uso:", OS)

    while continua:
        print("Inserisci comando di prompt:")
        cmd = input()
        connectionSocket.send(cmd.encode())  # manda il messaggio al client
        out = connectionSocket.recv(1024).decode()
        print(out)
        print("Inserire un nuovo comando? [s\\n]: ")
        yn = input()
        while yn != "s" and yn != "n" and yn != "S" and yn != "N":
            print("Input non valido, reinserire: ")
            yn = input()
        if yn == "s" or yn == "S":
            continua = True
        else:
            print("Termino la connessione..")
            connectionSocket.close()
            continua = False
            print("Connessione terminata.")


