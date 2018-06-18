#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : s4_serverThread_client.py      version 1.2
Date : 18-04-2018
Auteur : Hervé Dugast
Source : http://www.bogotobogo.com/python/python_network_programming_server_client.php
                NETWORK PROGRAMMING III - SOCKETSERVER 

------ Affichage console s4_serverThread_client.py ------------------------------------------------
Server loop running in thread: Thread-1
Received: Thread-2: Hello World 1
Received: Thread-3: Hello World 2
Received: Thread-4: Hello World 3
fin Thread-1
fin Thread-4
fin Thread-2
fin Thread-3
---------------------------------------------------------------------------------------------------
"""
import socket
import threading
import socketserver
import time

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

   def handle(self):
      """ To implement a service, we must derive a class from BaseRequestHandler and redefine 
          its handle() method
      """
      # receive bytearray and convert it to string
      data = (self.request.recv(1024)).decode('utf8')
      cur_thread = threading.current_thread()
      # Add the thread name in the message
      dataNew = "{}: {}".format(cur_thread.name, data)
      self.request.sendall(dataNew.encode('utf_8'))
      time.sleep(3)
      print("fin {}".format(cur_thread.name))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
   """ When inheriting from ThreadingMixIn for threaded connection behavior, we should explicitly 
       declare how we want our threads to behave on an abrupt shutdown. The ThreadingMixIn class 
       defines an attribute daemon_threads, which indicates whether or not the server should wait 
       for thread termination. We should set the flag explicitly if we would like threads to 
       behave autonomously. The default value is False, meaning that Python will not exit 
       until all threads created by ThreadingMixIn have exited. In the code, we set it True, 
       which means Python will exit the server thread when the main thread terminates not waiting 
       for other threads' exit.
   """
   pass

def client(ip, port, message):
   
   try:
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.connect((ip, port))
      sock.sendall(message.encode('utf_8'))
      response = sock.recv(1024)
      print("Received: {}".format(response.decode('utf_8')))
   finally:
      sock.close()

if __name__ == "__main__":
   # port 0 means to select an arbitrary unused port
   HOST, PORT = "localhost", 0

   server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
   ip, port = server.server_address

   # start a thread with the server. 
   # the thread will then start one more thread for each request.
   server_thread = threading.Thread(target=server.serve_forever)

   # exit the server thread when the main thread terminates
   server_thread.daemon = True
   server_thread.start()
   print("Server loop running in thread:", server_thread.name)

   client(ip, port, 'Hello World 1')
   client(ip, port, 'Hello World 2')
   client(ip, port, 'Hello World 3')

   server.shutdown()
   print("fin Thread-1")