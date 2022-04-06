#!/usr/bin/env python3

# Importing socket library 
import socket
import datetime
import time


clientesAddr = []

# Now we can create socket object
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Lets choose one port and start listening on that port
PORT = 9899
BUFFER = 1024*64
print("\n Server is listing on port :", PORT, "\n")

# Now we need to bind to the above port at server side
ip = 'localhost'
s.bind((ip, PORT))

# Seleccion
print("Seleccione el archivo que quiere enviar:")
print("1. Archivo 100MB")
print("2. Archivo 250MB")
print("3. Archivo prueba")
archivo = input()
conexiones = input("Indique el número de conexiones: ")

def readFile():
    # Variable file
    file = ""

    if archivo == "1":
        file = open("./ArchivosServidor/file100MB.txt", "rb")
    elif archivo == "2":
        file = open("./ArchivosServidor/file250MB.txt", "rb")
    elif archivo == "3":
        file = open("./ArchivosServidor/sample1.txt", "rb")

    return file

tiempoTotal = 0
def sendData_client(direccion, id):

    #Envía id del cliente
    s.sendto((str(id)+"/"+str(conexiones)+"/"+str(archivo)).encode(), direccion)

    # Variable file
    file = readFile()
    sendData = file.read(BUFFER)
    t1 = int(round(time.time() * 1000))
    while sendData:
        # Now send the content of sample.txt to server
        print("Enviando")
        s.sendto(sendData, direccion)
        sendData = file.read(BUFFER)
    print("Fin envío")
    t2 = int(round(time.time() * 1000))
    tiempoTotal = t2-t1
    s.sendto("fin".encode(), direccion)

    # Close file
    file.close()

def logs(idCliente, Resultado, timeE):
    date = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    file = open(f"./ArchivosServidor/Logs/{date}-log.txt", "a")

    if archivo == "1":
        file.write("\n Nombre del archivo: file100MB.txt - Tamanio: 100MB")
    elif archivo == "2":
        file.write("\n Nombre del archivo: file250MB.txt - Tamanio: 250MB")
    elif archivo == "3":
        file.write("\n Nombre del archivo: sample1.txt - Tamanio: 13B")

    file.write('\n Conexion con el cliente: ' + str(idCliente))
    file.write('\n La entrega del archivo fue: ' + Resultado)
    file.write('\n El tiempo de ejecucion fue: ' + str(timeE) + " ms")
    file.close()

# Now we do not know when client will concatct server so server should be listening contineously
while True:
    # Now we can establish connection with clien
    data, addr = s.recvfrom(BUFFER)
    print(data.decode())
    if(data.decode() == "Hola"):
        clientesAddr.append(addr)
        sendData_client(addr, len(clientesAddr))
    else:
        res = data.decode()
        print(res)
        logs(clientesAddr.index(addr)+1, res, tiempoTotal)
    # Come out from the infinite while loop as the file has been copied from client.
    # break
