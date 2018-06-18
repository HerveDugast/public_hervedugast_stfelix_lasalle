#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : ThreadSockServer.py      version 1.3
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
import socket
import sys
import threading
from CLogger import CLogger

class ThreadSockServer(threading.Thread):
   """ Gère un socket serveur dans un thread
   """
   def __init__(self, nomThread='thSockSrv_listen', host="127.0.0.1", port=0, \
                loggerName="debugThreadSockServer", loggerLevel="DEBUG", consoleLevel="INFO",  \
                fileName="debugThreadSockServer.log", fileLevel="DEBUG"):
      """ constructeur
          Consulter commentaires classe CLogger pour en savoir plus sur les autres paramètres
      """
      fonction = "ThreadSockServer.__init__(host={}, port={}, ...)".format(host, port)
      # ----- Mise en place du logger qui va gérer les handlers console et fichier rotatif
      self.logger = CLogger(loggerName, loggerLevel, consoleLevel, fileName, fileLevel)      
      self.__nomThread = nomThread
      self.__host = host
      self.__port = port
      threading.Thread.__init__(self, name=nomThread)
      self.sockSrv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      try:
         self.sockSrv.bind((host, port))
      except:
         message = "Thread {}. La liaison du socket à l'adresse choisie a échoué \n{}\n-- {}" \
            .format(nomThread, sys.exc_info(), fonction)
         self.logger.error(message)
         sys.exit()
      self.sockSrv.listen(5)
      # Attente et prise en charge des connexions demandées par les clients :
      self.cnxClient = {}	# dictionnaire des connexions clients
      
   def run(self):
      fonction = "ThreadSockServer.run()"
      nomThreadSrv = self.__nomThread
      message = "Serveur prêt, en attente de requêtes ..."
      print(message)
      message2 = "Thread {}. {} Ecoute port {}, attente clients (accept) -- {}" \
         .format(nomThreadSrv, message, self.__port, fonction)
      self.logger.debug(message2)
      while 1:
         # Attente connexion clients
         cnxClient, adresse = self.sockSrv.accept()
         # Créer un nouvel objet thread pour gérer la connexion :
         thCnxClient = ThreadClient(cnxClient, self.cnxClient, self.logger)
         # Mémoriser la connexion dans le dictionnaire :
         nomThreadCli = thCnxClient.getName()	  # identifiant du thread
         self.cnxClient[nomThreadCli] = cnxClient
         message = "Connexion Client-{}, IP {}, port {}" \
            .format(nomThreadCli.split('_')[2], adresse[0], adresse[1])
         print(message)
         message2 = "Thread {}. {}. Création du thread {} pour gérer les messages de ce client " \
            "-- {}".format(nomThreadSrv, message, nomThreadCli, fonction)
         self.logger.debug(message2)
           # Dialogue avec le client :
         thCnxClient.start()
         message = "#Client-{}# Vous êtes connecté, envoyez vos messages.".format(ThreadClient.numClient)
         message2 = "Thread {}. Affichage console server et envoi à Client-{} (send): '{}' -- {}" \
            .format(nomThreadSrv, nomThreadCli.split('_')[2], message, fonction)
         self.logger.debug(message2)
         cnxClient.send(message.encode('utf8'))      
   
class ThreadClient(threading.Thread):
   """  dérivation d'un objet thread pour gérer la connexion avec un client
   """
   numClient = 0
   def __init__(self, cnxSock, cnxClient, logger):
      num = self.__genererNumClient()
      nomThread = "thSockSrv_Client_{}".format(num)
      self.__nomClient = "Client-{} ".format(num)
      threading.Thread.__init__(self, name=nomThread) 
      self.cnxSock = cnxSock
      self.cnxClient = cnxClient
      self.logger = logger

   def __genererNumClient(self):
      """ Génère un numéro de client unique : 1, 2, ...
          Retour : int
      """
      ThreadClient.numClient += 1
      return ThreadClient.numClient
   
   def run(self):
      # Dialogue avec le client :
      fonction = "module ThreadSockServer.py, ThreadClient.run()"
      nomThread = self.getName()	    # Chaque thread possède un nom
      while 1:
         try:
            # attente réception message client
            message = "Thread {}. Attente réception message {} (recv) -- {} " \
               .format(nomThread, self.__nomClient, fonction)
            self.logger.debug(message)
            msgClient = self.cnxSock.recv(1024)
            msgClient = msgClient.decode('utf8')
            
            if not msgClient or msgClient.upper() == "FIN":
               break
            # message encodé en bytearray
            message = "{}> {}".format(self.__nomClient, msgClient)
            print(message)
            message2 = "Thread {}. Message reçu puis affiché dans la console : '{}' -- {}" \
               .format(nomThread, message, fonction)
            self.logger.debug(message2)
            # Faire suivre le message à tous les autres clients :
            for cle in self.cnxClient:
               if cle != nomThread:	  # ne pas le renvoyer à l'émetteur
                  message3 = "Thread {}. Transmission (send) message '{}' à Client-{} -- {}" \
                     .format(nomThread, message, cle.split('_')[2], fonction)
                  self.logger.debug(message3)
                  self.cnxClient[cle].send(message.encode('utf_8'))
         except:
            message = "Thread {}. Client déconnecté ?\n{} -- {}" \
               .format(nomThread, sys.exc_info(), fonction)
            self.logger.error(message)
            break
            #sys.exit()
      
      try:
         # Fermeture de la connexion :
         del self.cnxClient[nomThread]	# supprimer son entrée dans le dictionnaire
         message = "{} s'est déconnecté".format(self.__nomClient)
         print(message)
         message2 = "Thread {}. {}. Fin du thread {}. -- {}" \
            .format(nomThread, message, nomThread, fonction)
         self.logger.debug(message2)
         self.cnxSock.close()	  # couper la connexion côté serveur
         # Le thread se termine ici
      except:
         print('*')

# Initialisation du serveur - Mise en place du socket :
if __name__ == "__main__":
   # mise un place d'un logger : 1 console et un fichier rotatif
   CLogger.effacerFichierLog("debugThreadSockServer.log")
   
   #HOST = '192.168.0.20'
   HOST = '192.168.0.20'
   PORT = 46000   
   thSockSrv_listen = ThreadSockServer('thSockSrv_listen', HOST, PORT)
   thSockSrv_listen.start()
   #print("Fin programme ThreadSockServer.py")
   
