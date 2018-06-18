#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : s2_server_echo.py      version 1.0
Date : 16-04-2018
Auteur : Hervé Dugast
Source : http://www.bogotobogo.com/python/python_network_programming_server_client.php
                NETWORK PROGRAMMING - SERVER & CLIENT A : BASICS

s2_server_echo.py sends the messages received (echo) from the client to the same client.

s2_client_echo.py sends 2 messages to the server. This last returns the same messages to the client
(echo).

------ Affichage console s2_server_echo.py --------------------------------------------------------
C:\>python D:\prog\python\socket__initiation\s2_server_echo.py
server listens port 12345
Connected by ('192.168.0.20', 52112)
Echo : b'Hello world!'
Echo : b'007F5A11'
---------------------------------------------------------------------------------------------------

------ Affichage console s2_client_echo.py --------------------------------------------------------
C:\>python D:\prog\python\socket__initiation\s2_client_echo.py
Received b'Hello world!'
Received b'007F5A11'
---------------------------------------------------------------------------------------------------

"""
import socket

host = ''        # Symbolic name meaning all available interfaces
port = 12345     # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
print("server listens port {}".format(port))
conn, addr = s.accept()
print('Connected by', addr)
while True:
   data = conn.recv(1024)
   if not data: break
   print("Echo : {}".format(repr(data)))
   conn.sendall(data)
conn.close()
