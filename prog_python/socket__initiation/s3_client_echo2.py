#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : s3_client_echo2.py      version 1.2
Date : 18-04-2018
Auteur : Hervé Dugast
Source : http://www.bogotobogo.com/python/python_network_programming_server_client.php
                NETWORK PROGRAMMING III - SOCKETSERVER 

s3_server_echo2.py
The server we're creating echoes the message received from clients except it sends the message 
back upper-cased. Press CTRL + C to stop.

s3_client_echo2.py sends a messages to the server. This last returns the same message upper-cased
to the client (echo).

------ Affichage console s3_server_echo2.py -------------------------------------------------------
C:\>D:\prog\python\socket__initiation\s3_server_echo2.py
127.0.0.1 wrote:
b'Hello world!'
127.0.0.1 wrote:
b'Hello world!'
---------------------------------------------------------------------------------------------------

------ Affichage console s3_client_echo2.py -------------------------------------------------------
C:\>D:\prog\python\socket__initiation\s3_client_echo2.py
Sent:     b'Hello world!'
Received: b'HELLO WORLD!'

C:\>D:\prog\python\socket__initiation\s3_client_echo2.py
Sent:     b'Hello world!'
Received: b'HELLO WORLD!'
---------------------------------------------------------------------------------------------------
"""
import socket
import binascii  # to display a bytearray type in hex

HOST, PORT = "localhost", 9999
message = "C'est un lézard"

# create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
   # connect to server 
   sock.connect((HOST, PORT))
   # send data
   sock.sendall(message.encode('utf_8'))
   # receive data back from the server
   received = sock.recv(1024)
finally:
   # shut down
   sock.close()

print("Sent:     {}".format(message))
# display of the received message in different forms
print("Received: {}".format(received))
print("          {}".format(received.decode('utf_8')))
print("          {}".format(binascii.hexlify(received)))
