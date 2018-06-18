#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : s2_client_echo.py      version 1.2
Date : 18-04-2018
Auteur : Hervé Dugast
Source : http://www.bogotobogo.com/python/python_network_programming_server_client.php
                NETWORK PROGRAMMING - SERVER & CLIENT A : BASICS

s2_server_echo.py sends the messages received (echo) from the client to the same client.

s2_client_echo.py sends 2 messages to the server. This last returns the same messages to the client
(echo).

------ Affichage console s2_server_echo.py --------------------------------------------------------
C:\>python D:\prog\python\socket__initiation\s2_server_echo.py
server listens port 12345
Connected by ('192.168.0.20', 49745)
Echo : b'Hello world!'
Echo : b'\x00\x7f\xa2\x01'
---------------------------------------------------------------------------------------------------

------ Affichage console s2_client_echo.py --------------------------------------------------------
C:\>python D:\prog\python\socket__initiation\s2_client_echo.py
Sent     : b'Hello world!'
Received : b'Hello world!'

Sent     : b'007fa201'
Received : b'\x00\x7f\xa2\x01'
           00 7f a2 011'
---------------------------------------------------------------------------------------------------
"""
import socket
import time
import binascii # to display a bytearray type in hex

host = socket.gethostname() 
host='192.168.0.20'
port = 12345                   # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

msgTxt = 'Hello world!'
print('Sent     : {}'.format(msgTxt.encode('utf_8')))
s.sendall(msgTxt.encode('utf_8'))
data = s.recv(1024)
print('Received : {}'.format(data))  # type bytes object
#print('Received : {}'.format(data.decode('utf_8')))  # convert to type str

msgBytearray = bytearray([])
msgBytearray.append(0x00)
msgBytearray.append(0x7F)
msgBytearray.append(0xA2)
msgBytearray.append(0x01)
print('\nSent     : {}'.format(binascii.hexlify(msgBytearray))) # bytearray displayed in hex
s.sendall(msgBytearray)
data = s.recv(1024)
print('Received : {}'.format(data))  # bytearray displayed by default
# to display the contents of bytearray in hex
print('           ', end='')
for byteVal in data:
   print("{0:02x} ".format(byteVal), end='')
   
s.close()
