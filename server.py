#!/usr/bin/env python3

# Importing socket library 
import socket
import hashlib
import datetime
import time
from _thread import *
from xmlrpc.client import DateTime

def hash_file(filename):
   """"This function returns the SHA-1 hash
   of the file passed into it"""

   # make a hash object
   h = hashlib.sha1()
   # open file for reading in binary mode
   with open(filename,'rb') as f:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = f.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()

# Now we can create socket object
s = socket.socket()

#Number of threads
ThreadCount = 1

listThreads = []

# Lets choose one port and start listening on that port
PORT = 9899
print("\n Server is listing on port :", PORT, "\n")

# Now we need to bind to the above port at server side
s.bind(('', PORT))

# Seleccion
print("Seleccione el archivo que quiere enviar:")
print("1. Archivo 100MB")
print("2. Archivo 250MB")
print("3. Archivo prueba")
archivo = input()

def readFile():
    #Variable file
    file = ""

    if archivo=="1":
        file = open("./ArchivosServidor/file100MB.txt", "rb") 
        hash_value = hash_file("./ArchivosServidor/file100MB.txt")
    elif archivo == "2":
        file = open("./ArchivosServidor/file250MB.txt", "rb") 
        hash_value = hash_file("./ArchivosServidor/file250MB.txt")
    elif archivo == "3":
        file = open("./ArchivosServidor/sample1.txt", "rb")
        hash_value = hash_file("./ArchivosServidor/sample1.txt")

    return file

def readHash():
    #Variable hash
    hash_value = ""

    if archivo=="1":
        hash_value = hash_file("./ArchivosServidor/file100MB.txt")
    elif archivo == "2":
        hash_value = hash_file("./ArchivosServidor/file250MB.txt")
    elif archivo == "3":
        hash_value = hash_file("./ArchivosServidor/sample1.txt")

    return hash_value

clients = input("Número de clientes a los cuales desea enviar el archivo: ")

# Now we will put server into listenig  mode 
s.listen(int(clients))

def threaded_client(conn, id):
    #Variable file
    file = readFile()

    #Variable hash
    hash_value = readHash()

    SendData = file.read(1024)

    estado = conn.recv(1024).decode()

    print("\n Estado del cliente "+ str(id) +": " + estado + "\n\n")

    if estado == 'Listo':
        conn.send(str(clients).encode())

        res = conn.recv(1024).decode()

        if res == 'OK':
            conn.send(str(id).encode())
            res = conn.recv(1024).decode()
        
            if res == 'OK':
                conn.send(str(hash_value).encode())
                res = conn.recv(1024).decode()

                if res == 'OK':
                    t1 = int(round(time.time() * 1000))
                    while SendData:
                        #Now send the content of sample.txt to server
                        conn.send(SendData) 
                        SendData = file.read(1024)
                        res = conn.recv(10).decode()
                    t2 = int(round(time.time() * 1000))
                    conn.send('Fin'.encode())
                    res = conn.recv(1024).decode()

                    if res == 'OK':
                        conn.send(archivo.encode())
                        res = conn.recv(10).decode()
                        #res = 'Exitoso'
                        print(res)
                        logs(id, res, t2-t1) 

           

    # Close file
    file.close()

    # Close connection with client
    conn.close()
    print("\n Server closed the connection to client " + str(id) + " \n")

def logs(idThread, Resultado, timeE):
    date = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    file = open(f"./ArchivosServidor/Logs/{date}-log.txt", "a")

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

# Now we do not know when client will concatct server so server should be listening contineously  
while True:
    # Now we can establish connection with clien
    conn, addr = s.accept()
    
    listThreads.append(conn)

    print('Connected to: ' + addr[0] + ':' + str(addr[1]))
    if str(len(listThreads)) == clients:
        for l in range(len(listThreads)):
            start_new_thread(threaded_client, (listThreads[l], l+1))       
    
    print('Thread Number: ' + str(ThreadCount))
    ThreadCount  += 1
    # Come out from the infinite while loop as the file has been copied from client.
    #break
