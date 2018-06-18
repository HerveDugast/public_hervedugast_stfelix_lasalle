#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : s6_client_class.py      version 1.2
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
#host = '10.16.3.232'
host = '192.168.0.20'
port = 46000

import socket
import sys
import threading
import time

class ThreadReception(threading.Thread):
   """ objet thread gérant la réception des messages
   """
   def __init__(self, conn):
      threading.Thread.__init__(self)
      self.connexion = conn	     # réf. du socket de connexion

   def run(self):
      while 1:
         messageRecu = self.connexion.recv(1024)
         # messageRecu est un bytearray, conversion en str
         messageRecu = messageRecu.decode('utf8')
         print("* {} *".format(messageRecu))
         if not messageRecu or messageRecu.upper() == "FIN":
            break
      # Le thread <réception> se termine ici.
      # On demande la fermeture du thread <émission> :
      # th_E._stop() -> !!! ne fonctionne plus depuis version 3.4. 
      # L'arrêt brutal n'était pas une bonne idée de toute façon...
      print("Client arrêté. Connexion interrompue.")
      try:
         self.connexion.close()
      except:
         print("erreur")
      print("Fin thread réception")
      

class ThreadEmission(threading.Thread):
   """ objet thread gérant l'émission des messages
   """
   def __init__(self, conn):
      threading.Thread.__init__(self)
      self.connexion = conn	     # réf. du socket de connexion

   def run(self):
      while 1:
         message_emis = input()
         self.connexion.send(message_emis.encode("Utf8"))
         if message_emis.upper() == "FIN":
            break
            # Le thread <émission> se termine ici.
      print("Fin thread émission")

if __name__ == "__main__":
   # Programme principal - Établissement de la connexion :
   connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      connexion.connect((host, port))
      print("Connexion établie avec le serveur.")
      time.sleep(1)
      # Dialogue avec le serveur : on lance deux threads pour gérer
      # indépendamment l'émission et la réception des messages :
      th_E = ThreadEmission(connexion)
      th_R = ThreadReception(connexion)
      th_E.start()
      th_R.start()   
   except:
      print("La connexion a échoué. Fin du programme")
      sys.exit()
