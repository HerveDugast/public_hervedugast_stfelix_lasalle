#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : s1_client.py      version 1.2
Date : 18-04-2018
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

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()                           
port = 9999

# connection to hostname on the port.
s.connect((host, port))                               

# Receive no more than 1024 bytes, tm is bytes object.
# example : b'2018-04-18 16:07:39.843578'
tm = s.recv(1024)   

s.close()
# function decode convert bytes to str
print("The time got from the server is {}".format(tm.decode('utf_8')))