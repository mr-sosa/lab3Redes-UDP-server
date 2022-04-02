#!/usr/bin/env python3

# Importing libraries
import socket
import sys
import hashlib
import datetime
import time
from xmlrpc.client import DateTime

h = hashlib.sha1()
chunk = 0

# Lets catch the 1st argument as server ip
if (len(sys.argv) > 1):
    ServerIp = sys.argv[1]
else:
    print("\n\n Run like \n python3 client.py < serverip address > \n\n")
    exit(1)


# Now we can create socket object
s = socket.socket()

# Lets choose one port and connect to that port
PORT = 9899

# Lets connect to that port where server may be running
s.connect((ServerIp, PORT))

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

#Open one recv.txt file in write mode
#file = open("./ArchivosCliente/recv.txt", "wb")
#print("\n Copied file name will be recv.txt at server side\n")

# Send data
message = 'Listo'
print("\n " + message)
s.send(message.encode())

# Look for the response
conexiones = s.recv(4).decode()
print("\n\n Conexiones: " + conexiones)

s.send("OK".encode())

client = s.recv(4).decode()
print("\n\n Id Thread: "+client)
file = open(f"./ArchivosRecibidos/Cliente{client}-Prueba-{conexiones}.txt", "wb") 

s.send("OK".encode())

hash_server = s.recv(40).decode()
print("\n\n Hash server: " + hash_server)

s.send("OK".encode())
"""
# Receive any data from client side
RecvData = s.recv(1024)
print('a')

 while RecvData:
    print('b')
    h.update(RecvData)
    print('c')
    file.write(RecvData)
    print('d')
    RecvData = s.recv(1024) """

t1 = int(round(time.time() * 1000))
while True:
    # read 1024 bytes from the socket (receive)
    bytes_read = s.recv(1024)
    if bytes_read.decode() == 'Fin':
        # nothing is received
        #file transmitting is done
        break
        # write to the file the bytes we just received
    h.update(bytes_read)
    file.write(bytes_read)
    s.send("OK".encode())
        # update the progress bar
t2 = int(round(time.time() * 1000))

s.send("OK".encode())

archivo = s.recv(4).decode()

# Close the file opened at server side once copy is completed
file.close()
print("\n\n File has been copied successfully \n")

hash_f = h.hexdigest()
print("\n\n Hash file: " + hash_f)

if hash_f == hash_server:
    print("\n\n No se modifico el documento.")
    s.send("Exitoso".encode())
    logs(archivo, client, "Exitoso", t2-t1)
else:
    print("\n\n ERROR: se modifico el documento")
    s.send("Fallido".encode())
    logs(archivo, client, "Fallido", t2-t1)



# Close the connection from client side
s.close()
