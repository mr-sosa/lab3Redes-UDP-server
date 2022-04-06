#!/usr/bin/env python3

# Importing libraries
import socket
import sys
import datetime
import time
import os

BUFFER = 1024*64

# Lets catch the 1st argument as server ip
if (len(sys.argv) > 1):
    ServerIp = sys.argv[1]
else:
    print("\n\n Run like \n python3 client.py < serverip address > \n\n")
    exit(1)


# Now we can create socket object
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Lets choose one port and connect to that port
PORT = 9899
s.sendto("Hola".encode(), (ServerIp, PORT))

def getSizeArchivo(numArchivo):
    if(numArchivo == 1):
        return 100
    elif(numArchivo == 2):
        return 250
    else:
        return 13

def logs(archivo, idThread, Resultado, timeE):
    date = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    file = open(f"./ArchivosRecibidos/Logs/{date}-log.txt", "a")

    if archivo=="1":
        file.write("\n Nombre del archivo: file100MB.txt - Tamanio: 100MB")
    elif archivo == "2":
        file.write("\n Nombre del archivo: file250MB.txt - Tamanio: 250MB")
    elif archivo == "3":
        file.write("\n Nombre del archivo: sample1.txt - Tamanio: 13B")

    file.write('\n Conexion con el cliente: ' + str(idThread))
    file.write('\n La entrega del archivo fue: ' + Resultado)
    file.write('\n El tiempo de ejecucion fue: ' + str(timeE) + " ms")
    file.close()

# Look for the response
data, addr = s.recvfrom(BUFFER)
client, conexiones, archivo = data.decode().split("/")
print("\n\n Conexiones: " + conexiones)

file = open(f"./ArchivosRecibidos/Cliente{client}-Prueba-{conexiones}.txt", "wb")

t1 = int(round(time.time() * 1000))
while True:
    print("Recibiendo")
    data, addr = s.recvfrom(BUFFER)
    if data.decode() == 'fin':
        # nothing is received
        #file transmitting is done
        break
        # write to the file the bytes we just received
    file.write(data)
print("Fin recibido")
t2 = int(round(time.time() * 1000))

# Close the file opened at server side once copy is completed
file.close()
print("\n\n File has been copied successfully \n")
#file_size = os.path.getsize(f"./ArchivosRecibidos/Cliente{client}-Prueba-{conexiones}.txt")
file_size = os.path.getsize(f"./ArchivosRecibidos/Cliente1-Prueba-5.txt")
print(file_size)
if file_size == getSizeArchivo(archivo):
    print("\n\n Se recibió correctamente el archivo.")
    s.sendto("Exitoso".encode(), (ServerIp, PORT))
    logs(archivo, client, "Exitoso", t2-t1)
else:
    print("\n\n ERROR: No se recibió correctamente el archivo.")
    s.sendto("Fallido".encode(), (ServerIp, PORT))
    logs(archivo, client, "Fallido", t2-t1)

