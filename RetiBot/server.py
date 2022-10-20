from socket import *
serverPort = 120
serverSocket = socket(AF_INET, SOCK_STREAM) #AF inet intende IPv4 SOCK STREAM che TCP
serverSocket.bind(('', serverPort)) #il primno parametro indica da chi puo' ricevere. Lasciato vuoto si intende che tutti possono connettersi
serverSocket.listen(1)
print("Il server e' pronto")
while True:
    connectionSocket, addr = serverSocket.accept()  #indica chi e' collegato (addr) tramite IP e la connessione stessa
    print("Accettato un nuovo cliente", addr)
    sentence = connectionSocket.recv(1024).decode() #riceve il messaggio dal client, decode serve per trasformare il messsaggio indipendente dalla macchina
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence.encode()) #manda il messaggio al client
    connectionSocket.close()