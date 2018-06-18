#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : s6_server_class.py      version 1.2
Date : 18-04-2018
Auteur : Hervé Dugast
Source : https://python.developpez.com/cours/apprendre-python3/?page=page_20

s6_server_class.py
Création d'un serveur pouvant accepter plusieurs clients, réceptionner leurs messages et leur 
envoyer une confirmation à chaque réception. Ce programme ne peut pas s'arrêter "proprement".

s6_client_class.py
Client socket

------ Affichage console s6_server_class.py ------------------------------------------------------
C:\>python D:\prog\python\socket__initiation\s6_server_class.py
Serveur prêt, en attente de requêtes ...
Client Thread-1 connecté, adresse IP 192.168.0.20, port 61356
Thread-1> coucou
Client Thread-2 connecté, adresse IP 192.168.0.20, port 61357
Client Thread-3 connecté, adresse IP 192.168.0.20, port 61358
Thread-2> Bonjour
Thread-3> Hello
Thread-1> Où est l'âne ?
Thread-2> Pas là
Thread-3> C'est toi l'âne Thread-1
Client Thread-1 déconnecté.
Client Thread-2 déconnecté.
---------------------------------------------------------------------------------------------------

------ Affichage console s6_client_class.py (client 1) --------------------------------------------
C:\>python D:\prog\python\socket__initiation\s6_client_class.py
Connexion établie avec le serveur.
* Vous êtes connecté. envoyez vos messages. *
coucou
* Thread-2> Bonjour *
* Thread-3> Hello *
Où est l'âne ?
* Thread-2> Pas là *
* Thread-3> C'est toi l'âne Thread-1 *
fin
Fin thread émission
*  *
Client arrêté. Connexion interrompue.
Fin thread réception
---------------------------------------------------------------------------------------------------

------ Affichage console s6_client_class.py (client 2) --------------------------------------------
C:\>python D:\prog\python\socket__initiation\s6_client_class.py
Connexion établie avec le serveur.
* Vous êtes connecté. envoyez vos messages. *
Bonjour
* Thread-3> Hello *
* Thread-1> Où est l'âne ? *
Pas là
* Thread-3> C'est toi l'âne Thread-1 *
fin
*  *
Fin thread émission
Client arrêté. Connexion interrompue.
Fin thread réception
---------------------------------------------------------------------------------------------------

------ Affichage console s6_client_class.py (client 3) --------------------------------------------
C:\>python D:\prog\python\socket__initiation\s6_client_class.py
Connexion établie avec le serveur.
* Vous êtes connecté. envoyez vos messages. *
* Thread-2> Bonjour *
Hello
* Thread-1> Où est l'âne ? *
* Thread-2> Pas là *
C'est toi l'âne Thread-1
---------------------------------------------------------------------------------------------------
"""
#HOST = '10.16.3.232'
HOST = '192.168.0.20'
PORT = 46000

import socket, sys, threading

class ThreadClient(threading.Thread):
   """  dérivation d'un objet thread pour gérer la connexion avec un client
   """
   def __init__(self, conn):
      threading.Thread.__init__(self)
      self.connexion = conn

   def run(self):
      # Dialogue avec le client :
      nom = self.getName()	    # Chaque thread possède un nom
      while 1:
         msgClient = self.connexion.recv(1024)
         msgClient = msgClient.decode('utf8')
         
         if not msgClient or msgClient.upper() == "FIN":
            break
         # message encodé en bytearray
         message = "{}> {}".format(nom, msgClient)
         print(message)
         # Faire suivre le message à tous les autres clients :
         for cle in conn_client:
            if cle != nom:	  # ne pas le renvoyer à l'émetteur
               #conn_client[cle].send(message.encode("Utf8"))
               conn_client[cle].send(message.encode('utf8'))
   
      # Fermeture de la connexion :
      self.connexion.close()	  # couper la connexion côté serveur
      del conn_client[nom]	# supprimer son entrée dans le dictionnaire
      print("Client {} déconnecté.".format(nom))
      # Le thread se termine ici

# Initialisation du serveur - Mise en place du socket :
if __name__ == "__main__":
   mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      mySocket.bind((HOST, PORT))
   except socket.error:
      print("La liaison du socket à l'adresse choisie a échoué.")
      sys.exit()
   print("Serveur prêt, en attente de requêtes ...")
   mySocket.listen(5)
   
   # Attente et prise en charge des connexions demandées par les clients :
   conn_client = {}	# dictionnaire des connexions clients
   while 1:
      connexion, adresse = mySocket.accept()
      # Créer un nouvel objet thread pour gérer la connexion :
      th = ThreadClient(connexion)
      th.start()
      # Mémoriser la connexion dans le dictionnaire :
      it = th.getName()	  # identifiant du thread
      conn_client[it] = connexion
      print("Client {} connecté, adresse IP {}, port {}".format(it, adresse[0], adresse[1]))
      # Dialogue avec le client :
      msg = "Vous êtes connecté. envoyez vos messages."
      connexion.send(msg.encode('utf8'))