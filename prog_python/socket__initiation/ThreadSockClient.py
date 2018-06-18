#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : ThreadSockClient.py      version 1.3
Date : 30-04-2018
Auteur : Hervé Dugast

ThreadSockServer.py
Met en place un serveur de chat. Le serveur écoute sur un port défini et accepte les clients qui
se connectent. Le serveur réceptionne chaque message venant d'un client, l'affiche dans sa console 
puis l'envoie aux autres clients. Le serveur déconnecte un client lorsque ce dernier lui envoie le 
message 'fin'. Il peut également gérer la déconnexion "brutale" d'un client.

ThreadSockClient.py
Se connecte à un serveur de chat puis envoie des messages à celui-ci qui les retransmettra aux 
autres clients. Pour se déconnecter du chat, le client doir envoyer le message 'fin'. Le client 
gère la déconnexion "brutale" du serveur.

Fonctionnement détaillé
*** Etape 1 : 
  -Server-  Lancement serveur de chat. Création d'un socket dans le thread 'thSockSrv_listen'. Ce 
            dernier écoute un port défini afin d'accepter les clients qui veulent rejoindre le chat.
            Ex.:  PID    Protocol   local@         localPort   dist@      distPort   State 
                  9752     TCP      192.168.0.20   46000       0.0.0.0    0          LISTENING
             
*** Etape 2 : 
  -Client-  Connexion du 1er client (lancé sur la même machine que le serveur). Création d'un socket
            avec le server puis de 2 threads : Thread-1 Emission et Thread-2 Réception. Ces derniers
            gèrent l'émission et la réception du client sans bloquer le reste du programme. 
            Ex.:  PID    Protocol   local@         localPort   dist@         distPort   State 
                  13084  TCP        192.168.0.20   57054       192.168.0.20  46000      ESTABLISHED
  -Server-  Connecte le 1er client et mémorise cette connexion. Création d'un socket dans le thread 
            'thSockSrv_Client_1'. Ce dernier gérera uniquement les échanges avec le client-1.
            Ex.:  PID    Protocol   local@         localPort   dist@         distPort   State 
                  9752   TCP        192.168.0.20   46000       192.168.0.20  57054      ESTABLISHED

*** Etape 3 : 
  -Client-  Connexion du 2è client (lancé sur la même machine que le serveur). Création d'un socket
            avec le server puis de 2 threads : Thread-1 Emission et Thread-2 Réception. Ces derniers
            gèrent l'émission et la réception du client sans bloquer le reste du programme. 
            Ex.:  PID    Protocol   local@         localPort   dist@         distPort   State 
                  8292   TCP        192.168.0.20   57059       192.168.0.20  46000      ESTABLISHED
  -Server-  Connecte le 2è client et mémorise cette connexion. Création d'un socket dans le thread 
            'thSockSrv_Client_2'. Ce dernier gérera uniquement les échanges avec le client-2.
            Ex.:  PID    Protocol   local@         localPort   dist@         distPort   State 
                  9752   TCP        192.168.0.20   46000       192.168.0.20  57059      ESTABLISHED
...

------ Affichage console ThreadSockServer.py ------------------------------------------------------
D:\prog\python\socket__initiation>python ThreadSockServer.py
Serveur prêt, en attente de requêtes ...
Connexion Client-1, IP 192.168.0.20, port 57054
Client-1 > Bonjour
Connexion Client-2, IP 192.168.0.20, port 57059
Client-2 > Hello
Client-1 > you're welcome
Client-2  s'est déconnecté
Client-1 > tchao
---------------------------------------------------------------------------------------------------

------ Affichage console ThreadSockClient.py (client 1) --------------------------------------------
D:\prog\python\socket__initiation>python ThreadSockClient.py
Client C202-PF4 ['192.168.0.20']. Connexion établie avec le serveur.
* #Client-1# Vous êtes connecté, envoyez vos messages. *
Bonjour
* Client-2 > Hello *
you're welcome
tchao
---------------------------------------------------------------------------------------------------

------ Affichage console ThreadSockClient.py (client 2) --------------------------------------------
D:\prog\python\socket__initiation>python ThreadSockClient.py
Client C202-PF4 ['192.168.0.20']. Connexion établie avec le serveur.
* #Client-2# Vous êtes connecté, envoyez vos messages. *
Hello
* Client-1 > you're welcome *
fin
*  *
Fin thread émission
Client arrêté. Connexion interrompue. Fin thread réception.
---------------------------------------------------------------------------------------------------
"""
#host = '10.16.3.232'
host = '192.168.0.20'
port = 46000

import socket
import sys
import threading
import time
from CLogger import CLogger

class ThreadSockClient():
   numclient = 0
   def __init__(self, host="127.0.0.1", port=0, \
                loggerName="debugThreadSockClient", loggerLevel="DEBUG", consoleLevel="INFO",  \
                fileName="debugThreadSockClient.log", fileLevel="DEBUG"):
      """ Constructeur
          Consulter commentaires classe CLogger pour en savoir plus sur les autres paramètres
      """
      fonction = "ThreadSockServer.__init__(host={}, port={}, ...)".format(host, port)
      # ----- Mise en place du logger qui va gérer les handlers console et fichier rotatif
      self.logger = CLogger(loggerName, loggerLevel, consoleLevel, fileName, fileLevel)      
      
      # récupération nom de machine et adresse IP du client (machine exécutant ThreadSockClient.py)
      pcNameIp = socket.gethostbyname_ex(socket.gethostname())
      # exemple de pcNameIp :   C202-PF4 ['192.168.0.20']
      self.__pcNameIp = "{} {}".format(pcNameIp[0], pcNameIp[2])

      self.sockClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      try:
         self.sockClient.connect((host, port))
         # le nom de client utilisé par le serveur sera transmis par le serveur (1er message)
         # on utilise une liste (à 1 élément) pour pouvoir passer cette variable par référence
         self.__nomClient = [] 
         message = "Client {}. Connexion établie avec le serveur.".format(self.__pcNameIp)
         print(message)
         message2 = "Client {}. Affichage console : '{}' -- {}" \
            .format(self.__pcNameIp, message, fonction)
         self.logger.debug(message2)
         time.sleep(1)
         # Dialogue avec le serveur : on lance les threads qui gèrent l'émission et la réception
         # des messages
         thClientEmis = ThreadEmission(self.sockClient, self.__nomClient, self.__pcNameIp, \
                                       self.logger)
         thClientEmis.start()
         thClientRecept = ThreadReception(self.sockClient, self.__nomClient, self.__pcNameIp, \
                                          self.logger)
         thClientRecept.start()
         message = "Client {}. Lancement thread émission {} et thread réception {} -- {}" \
            .format(self.__pcNameIp, thClientEmis.getName(), thClientRecept.getName(), fonction)
         self.logger.debug(message)
      except:
         message = "Client {}. La connexion a échoué. Fin du programme.\n{} -- {}" \
            .format(self.__pcNameIp, sys.exc_info(), fonction)
         self.logger.error(message)
         sys.exit()
         
class ThreadEmission(threading.Thread):
   """ objet thread gérant l'émission des messages
   """
   def __init__(self, sockClient, nomClient, pcNameIp, logger):
      """ constructeur
          nomClient : list -> nomClient[0] : nom client utilisé par le serveur
      """
      threading.Thread.__init__(self)
      self.sockClient = sockClient	     # réf. du socket de connexion
      self.__nomClient = nomClient
      self.__pcNameIp = pcNameIp
      self.logger = logger

   def run(self):
      fonction = "module ThreadSockClient.py, ThreadReception.run()"
      nomThread = "{} Emission".format(self.getName())
      while 1:
         try:
            if self.__nomClient:
               nomClient = self.__nomClient[0]
            else:
               nomClient = self.__pcNameIp
            message = "{}, {}. Attente saisie client (input). -- {}" \
               .format(nomClient, nomThread, fonction)            
            self.logger.debug(message)
            message_emis = input()
            self.sockClient.send(message_emis.encode("utf_8"))
            message = "{}, {}. Envoi à server du message : '{}'. -- {}" \
               .format(nomClient, nomThread, message_emis, fonction)
            self.logger.debug(message)
            if message_emis.upper() == "FIN":
               break
         except:
            message = "{}, {}. Serveur déconnecté ? \n{} -- {}" \
               .format(nomClient, nomThread, sys.exc_info(), fonction)
            self.logger.error(message)
            sys.exit()            

            # Le thread <émission> se termine ici.
      message = "Fin thread émission"
      print(message)
      message2 = "{}, {}. Affichage console : '{}'. -- {}" \
         .format(nomClient, nomThread, message, fonction)
      self.logger.debug(message2)
      
class ThreadReception(threading.Thread):
   """ objet thread gérant la réception des messages
   """
   def __init__(self, sockClient, nomClient, pcNameIp, logger):
      """ constructeur
          nomClient : list -> nomClient[0] : nom client utilisé par le serveur
      """
      threading.Thread.__init__(self)
      self.sockClient = sockClient	     # réf. du socket de connexion
      self.__nomClient = nomClient
      self.__pcNameIp = pcNameIp
      self.logger = logger

   def run(self):
      fonction = "module ThreadSockClient.py, ThreadReception.run()"
      nomThread = "{} Réception".format(self.getName())
      while 1:
         try:
            if self.__nomClient:
               nomClient = self.__nomClient[0]
            else:
               nomClient = self.__pcNameIp
            message = "{}, {}. Attente message server (recv). -- {}" \
               .format(nomClient, nomThread, fonction)            
            self.logger.debug(message)
            messageRecu = self.sockClient.recv(1024)
            # messageRecu est un bytearray, conversion en str
            messageRecu = messageRecu.decode('utf8')
            print("* {} *".format(messageRecu))
            message = "{}, {}. Message reçu du server : '{}' -- {}" \
               .format(nomClient, nomThread, messageRecu, fonction)            
            self.logger.debug(message)
            self.__recupererNomClient(messageRecu)
            if not messageRecu or messageRecu.upper() == "FIN":
               break
         except:
            message = "{}, {}. Serveur déconnecté ? \n{} -- {}" \
               .format(nomClient, nomThread, sys.exc_info(), fonction)
            self.logger.error(message)
            sys.exit()            
            
      # Le thread <réception> se termine ici.
      # On demande la fermeture du thread <émission>
      message = "Client arrêté. Connexion interrompue. Fin thread réception."
      print(message)
      message2 = "{}, {}. Affichage console : '{}' -- {}" \
         .format(nomClient, nomThread, message, fonction)
      self.logger.debug(message2)
      try:
         self.sockClient.close()
      except:
         message = "{}, {}. \n{} -- {}" \
            .format(nomClient, nomThread, sys.exc_info(), fonction)
         self.logger.error(message)
         sys.exit()
      
   def __recupererNomClient(self, messageRecu):
      """ récupère le nom de client utilisé par le serveur 
          Les threads émission et réception auront accès à ce nom pour le log (self.__nomClient)
      """
      # recherche du nom de client à l'aide des délimiteurs. Exemple de message envoyé par serveur:
      #    * #Client-7# Vous êtes connecté, envoyez vos messages. * -> extraction de  Client-7
      message = messageRecu.split('#')
      if len(message) > 1:
         if message[1][:7] == 'Client-' :
            self.__nomClient.append(message[1])

if __name__ == "__main__":
   #HOST = '10.16.3.232'
   HOST = '192.168.0.20'
   PORT = 46000      
   thSockClient = ThreadSockClient(HOST, PORT)
   
