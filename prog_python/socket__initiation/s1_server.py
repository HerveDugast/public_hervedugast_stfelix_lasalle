#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : s1_server.py      version 1.0
Date : 16-04-2018
Auteur : Hervé Dugast
Source : http://www.bogotobogo.com/python/python_network_programming_server_client.php
                NETWORK PROGRAMMING - SERVER & CLIENT A : BASICS

s1_server.py sends the current time string to the client. 
Note that the server socket doesn't receive any data. It just produces client sockets. 
Each clientsocket is created in response to some other client socket doing a connect() to the host
and port we're bound to.

s1_client.py sends a connection request to the server. This last establishes this one. Then, 
the client can communicate with the server using methods send() et recv(). In our case, once the 
connection is established, the client displays the current time sent by the server.

------ Affichage console s1_server.py -------------------------------------------------------------
C:\>python D:\prog\python\socket__initiation\s1_server.py
server listens port 9999
Got a connection from ('192.168.0.20', 57293)
Got a connection from ('192.168.0.20', 57294)
---------------------------------------------------------------------------------------------------

------ Affichage console s1_client.py -------------------------------------------------------------
C:\>python D:\prog\python\socket__initiation\s1_client.py
The time got from the server is 2018-04-16 10:23:06.623527

C:\>python D:\prog\python\socket__initiation\s1_client.py
The time got from the server is 2018-04-16 10:23:10.944946
---------------------------------------------------------------------------------------------------

"""
import socket                                         
from datetime import datetime

# create a socket object using the given address family, socket type
# AF_INET : famille d'adresses de type Internet, SOCK_STREAM : type du socket pour protocole TCP
srvSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()                           
port = 9999                                           

# bind to the port
srvSock.bind((host, port))                                  

# queue up to 5 requests
srvSock.listen(5)   

print("server listens port {}".format(port))

while True:
   # establish a connection
   clientSock,addr = srvSock.accept()      

   print("Got a connection from {}".format(addr))
   dat = str(datetime.now())
   # send message convert to bytes object with method encode
   clientSock.send(dat.encode('utf_8'))
   clientSock.close()

