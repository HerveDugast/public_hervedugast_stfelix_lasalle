#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : s3_server_echo2.py      version 1.2
Date : 18-04-2018
Auteur : Hervé Dugast
Source : http://www.bogotobogo.com/python/python_network_programming_server_client.php
                NETWORK PROGRAMMING - SOCKETSERVER 

s3_server_echo2.py
The server we're creating echoes the message received from clients except it sends the message 
back upper-cased. Press CTRL + C to stop.

s3_client_echo2.py sends a messages to the server. This last returns the same message upper-cased
to the client (echo).

------ Affichage console s3_server_echo2.py -------------------------------------------------------
C:\>python D:\prog\python\socket__initiation\s3_server_echo2.py
127.0.0.1 wrote: b"C'est un l\xc3\xa9zard"
                 C'est un lézard
                 b'432765737420756e206cc3a97a617264'
---------------------------------------------------------------------------------------------------

------ Affichage console s3_client_echo2.py -------------------------------------------------------
C:\>python D:\prog\python\socket__initiation\s3_client_echo2.py
Sent:     C'est un lézard
Received: b"C'EST UN L\xc3\xa9ZARD"
          C'EST UN LéZARD
          b'432745535420554e204cc3a95a415244'
---------------------------------------------------------------------------------------------------
"""
import socketserver
import binascii  # to display a bytearray type in hex

# Create a request handler class by subclassing the BaseRequestHandler class
class MyTCPSocketHandler(socketserver.BaseRequestHandler):
   """
   The RequestHandler class for our server.
   It is instantiated once per connection to the server, and must override the handle() method to 
   implement communication to the client.
   """
   # The child class should override the inherited handle() method
   def handle(self):
      """ process incoming requests
      """
      # self.request is the TCP socket connected to the client
      # method strip removes spaces in front of and behind the string 
      self.data = self.request.recv(1024).strip()
      # display of the received message in different forms
      print("{} wrote: {}".format(self.client_address[0], self.data))
      print("                 {}".format(self.data.decode('utf_8')))
      print("                 {}".format(binascii.hexlify(self.data)))
      # just send back the same data, but upper-cased
      self.request.sendall(self.data.upper())

if __name__ == "__main__":
   HOST, PORT = "localhost", 9999
   # instantiate the server, and bind to localhost on port 9999
   server = socketserver.TCPServer((HOST, PORT), MyTCPSocketHandler)
   # handle_request() -> process one request     serve_forever() -> process many requests
   # activate the server, this will keep running until Ctrl-C
   server.serve_forever()
