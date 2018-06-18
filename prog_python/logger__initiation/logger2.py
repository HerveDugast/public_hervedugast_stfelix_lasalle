#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : logger2.py     version : 1.0
Auteur : H. Dugast
Date : 04-04-2018
Source : https://deusyss.developpez.com/tutoriels/Python/Logger/
Auteur source : GALODE Alexandre

Fonctionnement :
  Effectue un traçage des événements qui se produisent lors de l'exécution du programme. Ceux-ci
  sont mémorisés dans 2 fichiers et affichés dans la console en fonction de leur importance :
     - fichier debug.log : mémorise TOUTES les informations du niveau CRITICAL au niveau DEBUG
          nouveau fichier rotatif toutes les 2 secondes                      
     - fichier info.log : mémorise les informations de niveaux CRITICAL, ERROR, WARNING et INFO
          1 backup de fichier lorque le principal est rempli (taille 200 octets)
          fichier rotatif -> si fichier et backup rempli : dernière information écrase première 

------------- Contenu fichier debug.log après exécution --------------------------------------------
2018-04-04 22:32:40,770 -- debug_log -- DEBUG -- message debug n°8 -- logger2.envoyerMessageBoucle()
2018-04-04 22:32:41,373 -- debug_log -- DEBUG -- message debug n°9 -- logger2.envoyerMessageBoucle()
----------------------------------------------------------------------------------------------------
------------- Contenu fichier debug.log.2018-04-04_22-32-36 après exécution ------------------------
2018-04-04 22:32:36,463 -- debug_log -- DEBUG -- message DEBUG 1  -- logger2.envoyerMessageDivers()
2018-04-04 22:32:36,463 -- debug_log -- INFO -- message INFO 1 -- logger2.envoyerMessageDivers()
2018-04-04 22:32:36,463 -- debug_log -- WARNING -- message WARNING 1 -- logger2.envoyerMessageDivers()
2018-04-04 22:32:36,463 -- debug_log -- ERROR -- message ERROR 1 -- logger2.envoyerMessageDivers()
2018-04-04 22:32:36,463 -- debug_log -- CRITICAL -- message CRITICAL 1 -- logger2.envoyerMessageDivers()
2018-04-04 22:32:36,480 -- debug_log -- DEBUG -- message debug n°1 -- logger2.envoyerMessageBoucle()
2018-04-04 22:32:37,096 -- debug_log -- DEBUG -- message debug n°2 -- logger2.envoyerMessageBoucle()
2018-04-04 22:32:37,708 -- debug_log -- DEBUG -- message debug n°3 -- logger2.envoyerMessageBoucle()
----------------------------------------------------------------------------------------------------
------------- Contenu fichier debug.log.2018-04-04_22-32-38 après exécution ------------------------
2018-04-04 22:32:38,316 -- debug_log -- DEBUG -- message debug n°4 -- logger2.envoyerMessageBoucle()
2018-04-04 22:32:38,929 -- debug_log -- DEBUG -- message debug n°5 -- logger2.envoyerMessageBoucle()
2018-04-04 22:32:39,543 -- debug_log -- DEBUG -- message debug n°6 -- logger2.envoyerMessageBoucle()
----------------------------------------------------------------------------------------------------
------------- Contenu fichier info.log après exécution ---------------------------------------------
2018-04-04 22:32:40,770 -- info_log -- ERROR -- message error n°8
2018-04-04 22:32:41,373 -- info_log -- ERROR -- message error n°9
----------------------------------------------------------------------------------------------------
------------- Contenu fichier info.log.1 après exécution -------------------------------------------
2018-04-04 22:32:39,543 -- info_log -- ERROR -- message error n°6
2018-04-04 22:32:40,157 -- info_log -- ERROR -- message error n°7
----------------------------------------------------------------------------------------------------

------------- Affichage console après exécution ----------------------------------------------------
2018-04-04 22:32:36,463 -- info_log -- INFO -- message INFO 1
2018-04-04 22:32:36,463 -- info_log -- WARNING -- message WARNING 1
2018-04-04 22:32:36,463 -- info_log -- ERROR -- message ERROR 1
2018-04-04 22:32:36,479 -- info_log -- CRITICAL -- message CRITICAL 1
2018-04-04 22:32:36,481 -- info_log -- ERROR -- message error n°1
2018-04-04 22:32:37,096 -- info_log -- ERROR -- message error n°2
2018-04-04 22:32:37,708 -- info_log -- ERROR -- message error n°3
2018-04-04 22:32:38,316 -- info_log -- ERROR -- message error n°4
2018-04-04 22:32:38,929 -- info_log -- ERROR -- message error n°5
2018-04-04 22:32:39,543 -- info_log -- ERROR -- message error n°6
2018-04-04 22:32:40,157 -- info_log -- ERROR -- message error n°7
2018-04-04 22:32:40,770 -- info_log -- ERROR -- message error n°8
2018-04-04 22:32:41,373 -- info_log -- ERROR -- message error n°9

['2018-04-04 22:32:40,770 ', 'info_log ', 'ERROR ', 'message error n°8\n']
['2018-04-04 22:32:41,373 ', 'info_log ', 'ERROR ', 'message error n°9\n']

<time>2018-04-04 22:32:40,770  <logger>info_log  <level>ERROR  <message>message error n°8
<time>2018-04-04 22:32:41,373  <logger>info_log  <level>ERROR  <message>message error n°9
----------------------------------------------------------------------------------------------------

Compléments d'informations :
   - logger : objet mémoire tampon filtrant un niveau de criticité. Le logger envoie à ses handlers
              les messages de niveau supérieur ou égal à son niveau de criticité.
   - niveau de criticité : importance des messages, niveaux 
      Voici les niveaux de criticité classés du plus important au moins important :
         - CRITICAL (C) : plantage application...
         - ERROR (E) : erreur sévère sans plantage...
         - WARNING (W) : événement important pouvant entrainer un dysfonctionnement...
         - INFO (I) : information, événement normal venant de se passer...
         - DEBUG (G) : débogage, valeur de variables...
   - handler : gestionnaire qui redirigige le message vers un endroit désigné par le type de handler
     Types de handlers existant :
        - console : StreamHandler
        - fichiers : FileHandler, WatchedFileHandler, RotatingFileHandler, TimeRotatingFileHandler
        - mails : SmtpHandler
        - réseau : SocketHandler
        - web : HTTPHandler
        ...
   - formatter : permet de mettre en forme le message
     Attributs de format existant :
       %(asctime)s : Date au format  AAAA-MM-JJ HH:MM:SS,xxx 
       %(filename)s : Nom du fichier ayant écrit dans le log
       %(funcName)s : Nom de la fonction contenant l'appel à l'écriture dans le log
       %(levelname)s : Niveau du message
       %(module)s : Nom du module ayant appelé l'écriture dans le log
       %(message)s : Le message à logger
       %(name)s : Nom donné au logger avec méthode getLogger
       %(thread)d : L'ID du thread courant
       %(threadName)s : Le nom du thread courant
       ...
"""
# module gérant les loggers et les handlers
import logging
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
import time

def definirLoggerDebug():
   """
   """
   global loggerDebug

   # ------ format des messages --------------------------------------------------------------- 
   formatter = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s " \
                                      "-- %(module)s.%(funcName)s()")
   # ------ handler de type fichier rotatif périodique --------------------------------------- 
   # création d'un nouveau fichier log toutes les 2 secondes
   fileDebug = TimedRotatingFileHandler("debug.log", when="s", interval=2)
   # applique format message et niveau de sensibilité au handler
   fileDebug.setFormatter(formatter)
   fileDebug.setLevel(logging.DEBUG)
   # ------ logger --------------------------------------------------------------------------- 
   # nom du logger, puis niveau de sensibilité et liaison avec handler
   loggerDebug = logging.getLogger("debug_log")
   loggerDebug.setLevel(logging.DEBUG)
   loggerDebug.addHandler(fileDebug)

def definirLoggerInfo():
   """
   """
   global loggerInfo

   # ------ format des messages --------------------------------------------------------------- 
   # format des messages dans ce logger
   formatter = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")

   # ------ 1er handler de type fichier rotatif à taille définie ------------------------------ 
   # 1 seul backup, quand le fichier principal est rempli. Quand tout est rempli, les premières 
   # infos sont écrasées par les dernières arrivées
   fileInfo = RotatingFileHandler("info.log", maxBytes=200, backupCount=1)
   # applique format message et niveau de sensibilité au handler
   fileInfo.setFormatter(formatter)
   fileInfo.setLevel(logging.INFO)
   # ------ 2è handler de type console ------------------------------------------------------- 
   streamHandler = logging.StreamHandler()
   streamHandler.setFormatter(formatter)
   streamHandler.setLevel(logging.INFO)
   # ------ logger --------------------------------------------------------------------------- 
   # nom du logger, puis niveau de sensibilité et liaison avec handler
   loggerInfo = logging.getLogger("info_log")
   loggerInfo.setLevel(logging.INFO)
   loggerInfo.addHandler(fileInfo)
   loggerInfo.addHandler(streamHandler)   
   
def afficherDataFichierInfoLogBrut():
   """ Récupérer puis afficher les données stockées dans le fichier info.log
   """
   print("")
   with open("info.log", "r") as log_file:
      for line in log_file.readlines():
         data = line.split("-- ")
         print(data)

def afficherDataFichierInfoLog():
   """ Récupérer puis afficher les données stockées dans le fichier info.log
   """
   print("")
   with open("info.log", "r") as log_file:
      for line in log_file.readlines():
         data = line.split("-- ")
         print("<time>{} <logger>{} <level>{} <message>{}" \
               .format(data[0], data[1], data[2], data[3]), end='')   

def envoyerMessageDivers():
   """ Envoi de messages de différents niveaux aux loggers
   """
   loggerDebug.debug('message DEBUG 1 ')
   loggerDebug.info('message INFO 1')
   loggerDebug.warning('message WARNING 1')
   loggerDebug.error('message ERROR 1')
   loggerDebug.critical('message CRITICAL 1')

   loggerInfo.debug('message DEBUG 1 ')
   loggerInfo.info('message INFO 1')
   loggerInfo.warning('message WARNING 1')
   loggerInfo.error('message ERROR 1')
   loggerInfo.critical('message CRITICAL 1')

def envoyerMessageBoucle():
   """ Envoi de messages aux loggers
   """
   for i in range(1, 10):
      # i varie de 1 à 9
      loggerDebug.debug('message debug n°{}'.format(i))
      loggerInfo.error('message error n°{}'.format(i))
      time.sleep(0.6)

if __name__ == "__main__":
   definirLoggerDebug()
   definirLoggerInfo()
   envoyerMessageDivers()
   envoyerMessageBoucle()
   afficherDataFichierInfoLogBrut()
   afficherDataFichierInfoLog()

