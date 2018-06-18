#!/usr/bin/python3.4
# coding: utf-8
"""
Programme classe : CLogger.py     version : 1.1
Auteur : H. Dugast
Date : 30-04-2018
Source : https://deusyss.developpez.com/tutoriels/Python/Logger/
Auteur source : GALODE Alexandre

Fonctionnement :
  Cette classe peut être personnalisée en fonction des besoins de traçage.
  Dans le code ci-dessous
  - trace l'activité au niveau demandé dans la console
  - trace l'activité au niveau demandé (peut-être différent de celui choisi pour la console) 
    dans un fichier rotatif
    
------------------ Affichage console ---------------------------------------------------------------
2018-04-08 22:06:13,231 -- CRITICAL -- msg critical 1 -- CLogger.envoyerMessageTestTousNiveaux()
2018-04-08 22:06:13,232 -- ERROR -- msg error 1 -- CLogger.envoyerMessageTestTousNiveaux()

----- Affichage contenu fichier journal.log -----
2018-04-08 22:06:13,231 -- CRITICAL -- msg critical 1 -- CLogger.envoyerMessageTestTousNiveaux()
2018-04-08 22:06:13,232 -- ERROR -- msg error 1 -- CLogger.envoyerMessageTestTousNiveaux()
2018-04-08 22:06:13,232 -- WARNING -- msg warning 1 -- CLogger.envoyerMessageTestTousNiveaux()
2018-04-08 22:06:13,233 -- INFO -- msg info 1 -- CLogger.envoyerMessageTestTousNiveaux()
2018-04-08 22:06:13,233 -- DEBUG -- msg debug 1 -- CLogger.envoyerMessageTestTousNiveaux()
----------------------------------------------------------------------------------------------------

Compléments d'informations :
   - logger : objet mémoire tampon filtrant un niveau de criticité. Le logger envoie à ses handlers
              uniquement les messages de niveau supérieur ou égal à son niveau de criticité.
              ordre hiérarchique : CRITICAL > ERROR > WARNING > INFO > DEBUG
   - niveau de criticité : importance des messages 
      Voici les niveaux de criticité classés du plus important au moins important :
         - CRITICAL (C) : plantage application...
         - ERROR (E) : erreur sévère sans plantage...
         - WARNING (W) : événement important pouvant entrainer un dysfonctionnement...
         - INFO (I) : information, événement normal venant de se passer...
         - DEBUG (G) : débogage, valeur de variables...
   - handler : gestionnaire qui redirige le message vers un endroit désigné par le type de handler
     Types de handlers existant :
        - console : StreamHandler
        - fichier : FileHandler, WatchedFileHandler, RotatingFileHandler, TimeRotatingFileHandler
        - mail : SmtpHandler
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
import sys
import logging
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
import time
import os

class CLogger:
   """ Classe permettant d'effectuer un traçage des événements
      Trace les événements au niveau demandé dans la console et un fichier rotatif
   """
   # Niveau disponible pour le logger qui envoie les événements à la console et au fichier
   # ordre hiérarchique : CRITICAL > ERROR > WARNING > INFO > DEBUG
   level = {"critical":"CRITICAL", "error":"ERROR", "warning":"WARNING", "info":"INFO", \
            "debug":"DEBUG"}
   
   def __init__(self, loggerName="foo", loggerLevel="DEBUG", consoleLevel="DEBUG", \
                fileName="foo.log", fileLevel="DEBUG", maxBytes=1000000, backupCount=1 ):
      """ constructeur
      """
      self.__loggerName = loggerName
      # ------ format des messages --------------------------------------------------------------- 
      # format des messages dans ce logger, regarder l'entête pour en savoir plus
      formatter = logging.Formatter("%(asctime)s -- %(levelname)s -- %(message)s")
   
      # ------ 1er handler de type console ------------------------------------------------------- 
      self.__streamHandler = logging.StreamHandler()
      self.__streamHandler.setFormatter(formatter)
      self.set_consoleLevel(consoleLevel)
      
      # ------ 2ème handler de type fichier rotatif à taille définie ------------------------------ 
      self.__maxBytes = maxBytes          # taille max fichier
      self.__backupCount = backupCount    # nb de backup lorsque le fichier est rempli
      self.__fileName = fileName
      self.__fileHandler = RotatingFileHandler(fileName, maxBytes, backupCount)
      # applique format message
      self.__fileHandler.setFormatter(formatter)
      #  fixe le niveau de sensibilité au handler
      self.set_fileLevel(fileLevel)

      # ------ logger --------------------------------------------------------------------------- 
      # nom du logger, puis niveau de sensibilité et liaison avec handler
      self.__logger = logging.getLogger(loggerName)
      self.set_loggerLevel(loggerLevel)
      self.__logger.addHandler(self.__streamHandler)   
      self.__logger.addHandler(self.__fileHandler)
   
   def set_loggerLevel(self, loggerLevel):
      """ Change la valeur de __loggerLevel. Si la valeur passée en paramètre n'est pas valide, la 
          valeur "DEBUG" est écrite dans __loggerLevel.
      """
      if loggerLevel.lower() not in __class__.level.keys():
         self.__loggerLevel = "DEBUG"
      else:
         self.__loggerLevel = loggerLevel.upper()
      
   def set_maxBytes(self, maxBytes):
      self.__maxBytes = maxBytes
      
   def set_backupCount(self, backupCount):
      self.__backupCount = backupCount

   def set_loggerLevel(self, loggerLevel):
      """ Fixe le niveau de sensibilité du logger. Change la valeur de __loggerLevel. 
          Si la valeur passée en paramètre n'est pas valide, la valeur "DEBUG" est écrite 
          dans __loggerLevel.
      """
      if loggerLevel.lower() not in __class__.level.keys():
         self.__loggerLevel = "DEBUG"
      else:
         self.__loggerLevel = loggerLevel.upper()
      self.__changerLoggerLevel() 
      
   def __changerLoggerLevel(self):
      if self.__loggerLevel == __class__.level['critical']:
         self.__logger.setLevel(logging.CRITICAL)
      elif self.__loggerLevel == __class__.level['error']:
         self.__logger.setLevel(logging.ERROR)
      elif self.__loggerLevel == __class__.level['warning']:
         self.__logger.setLevel(logging.WARNING)
      elif self.__loggerLevel == __class__.level['info']:
         self.__logger.setLevel(logging.INFO)
      elif self.__loggerLevel == __class__.level['debug']:
         self.__logger.setLevel(logging.DEBUG)

   def set_fileLevel(self, fileLevel):
      """ Fixe le niveau de sensibilité du handler RotatingFileHandler. Change la valeur 
          de __fileLevel. Si la valeur passée en paramètre n'est pas valide, la valeur "DEBUG" 
          est écrite dans __fileLevel.
      """
      if fileLevel.lower() not in __class__.level.keys():
         self.__fileLevel = "DEBUG"
      else:
         self.__fileLevel = fileLevel.upper()
      self.__changerFileLevel() 
         
   def __changerFileLevel(self):
      if self.__fileLevel == __class__.level['critical']:
         self.__fileHandler.setLevel(logging.CRITICAL)
      elif self.__fileLevel == __class__.level['error']:
         self.__fileHandler.setLevel(logging.ERROR)
      elif self.__fileLevel == __class__.level['warning']:
         self.__fileHandler.setLevel(logging.WARNING)
      elif self.__fileLevel == __class__.level['info']:
         self.__fileHandler.setLevel(logging.INFO)
      elif self.__fileLevel == __class__.level['debug']:
         self.__fileHandler.setLevel(logging.DEBUG)
      
   def set_consoleLevel(self, consoleLevel):
      """ Fixe le niveau de sensibilité du handler streamHandler (console). Change la valeur 
          de __consoleLevel. Si la valeur passée en paramètre n'est pas valide, la valeur "DEBUG" 
          est écrite dans __consoleLevel.
      """
      if consoleLevel.lower() not in __class__.level.keys():
         self.__consoleLevel = "DEBUG"
      else:
         self.__consoleLevel = consoleLevel.upper()
      self.__changerConsoleLevel() 
         
   def __changerConsoleLevel(self):
      if self.__consoleLevel == __class__.level['critical']:
         self.__streamHandler.setLevel(logging.CRITICAL)
      elif self.__consoleLevel == __class__.level['error']:
         self.__streamHandler.setLevel(logging.ERROR)
      elif self.__consoleLevel == __class__.level['warning']:
         self.__streamHandler.setLevel(logging.WARNING)
      elif self.__consoleLevel == __class__.level['info']:
         self.__streamHandler.setLevel(logging.INFO)
      elif self.__consoleLevel == __class__.level['debug']:
         self.__streamHandler.setLevel(logging.DEBUG)   
      
   def critical(self, message):
      """ Envoie un message de niveau CRITICAL sur les handlers du logger si ce niveau est 
          supérieur ou égal au niveau configuré dans le logger.
      """
      self.__logger.critical(message)

   def error(self, message):
      """ Envoie un message de niveau ERROR sur les handlers du logger si ce niveau est 
          supérieur ou égal au niveau configuré dans le logger.
      """
      self.__logger.error(message)
      
   def warning(self, message):
      """ Envoie un message de niveau WARNING sur les handlers du logger si ce niveau est 
          supérieur ou égal au niveau configuré dans le logger.
      """
      self.__logger.warning(message)

   def info(self, message):
      """ Envoie un message de niveau INFO sur les handlers du logger si ce niveau est 
          supérieur ou égal au niveau configuré dans le logger.
      """
      self.__logger.info(message)

   def debug(self, message):
      """ Envoie un message de niveau DEBUG sur les handlers du logger si ce niveau est 
          supérieur ou égal au niveau configuré dans le logger.
      """
      self.__logger.debug(message)

   def get_fileName(self):
      return self.__fileName
   
   def afficherContenuFichier(self, fileName="foo.log"):
      """ Affiche le contenu du fichier indiqué
      """
      print("----- Affichage contenu fichier {} -----".format(fileName))
      with open(fileName, "r") as log_file:
         print(log_file.read())
   
   def afficherDonneesFichier(self, fileName="foo.log"):
      """ Récupérer puis afficher les données stockées dans le fichier indiqué
      """
      print("----- Fichier {} : affichage informations parsées dans une variable -----" \
            .format(fileName))
      with open(fileName, "r") as log_file:
         for line in log_file.readlines():
            data = line.split("-- ")
            print(data)
   
   def afficherDataFichierInfoLog(self, fileName="foo.log"):
      """ Récupérer puis afficher les données stockées dans le fichier indiqué
      """
      print("----- Fichier {} : affichage informations parsées par type -----" \
               .format(fileName))
      with open(fileName, "r") as log_file:
         for line in log_file.readlines():
            data = line.split("-- ")
            print("<time>{} <logger>{} <level>{} <message>{}" \
                  .format(data[0], data[1], data[2], data[3]), end='')   
   
   def envoyerMessageTestNiveau(self, niveauMsg, num=1):
      """ Envoie un message avec le niveau indiqué au logger
          Niveau possible : CRITICAL, ERROR, WARNING, INFO, DEBUG
      """
      if niveauMsg.upper() == __class__.level['critical']:
         self.__logger.critical("msg critical {}".format(num))
      elif niveauMsg.upper() == __class__.level['error']:
         self.__logger.error('msg error {}'.format(num))
      elif niveauMsg.upper() == __class__.level['warning']:
         self.__logger.warning('msg warning {}'.format(num))
      elif niveauMsg.upper() == __class__.level['info']:
         self.__logger.info('msg info {}'.format(num))
      elif niveauMsg.upper() == __class__.level['debug']:
         self.__logger.debug('msg debug {}'.format(num))
      else:
         print("Echec envoi message, niveau '{}' non reconnu !".format(niveauMsg))

   def envoyerMessageTestTousNiveaux(self, num=1):
      """ Envoi un message avec chaque niveau possible au logger
          Niveaux envoyés : CRITICAL, ERROR, WARNING, INFO, DEBUG
      """
      self.__logger.critical('msg critical {}'.format(num))
      self.__logger.error('msg error {}'.format(num))
      self.__logger.warning('msg warning {}'.format(num))
      self.__logger.info('msg info {}'.format(num))
      self.__logger.debug('msg debug {}'.format(num))
   
   def envoyerMessageBoucle(self, niveauMsg="TOUS", nbMsg=10, timeSleep=0):
      """ Envoie un certain nombre de fois un message de niveau choisi au logger
          Niveaux envoyés : CRITICAL, ERROR, WARNING, INFO, DEBUG
          "TOUS" -> envoie tous les niveaux à chaque boucle
      """
      for num in range(1, nbMsg+1):
         if niveauMsg.upper() == __class__.level['critical'] or niveauMsg.upper() == "TOUS":
            self.__logger.critical("msg boucle critical {}".format(num))
         if niveauMsg.upper() == __class__.level['error'] or niveauMsg.upper() == "TOUS":
            self.__logger.error('msg boucle error {}'.format(num))
         if niveauMsg.upper() == __class__.level['warning'] or niveauMsg.upper() == "TOUS":
            self.__logger.warning('msg boucle warning {}'.format(num))
         if niveauMsg.upper()== __class__.level['info'] or niveauMsg.upper() == "TOUS":
            self.__logger.info('msg boucle info {}'.format(num))
         if niveauMsg.upper() == __class__.level['debug'] or niveauMsg.upper() == "TOUS":
            self.__logger.debug('msg boucle debug {}'.format(num))
         if timeSleep != 0:
            time.sleep(timeSleep)
            
   @staticmethod
   def effacerFichierLog(fileName):
      """ Efface le fichier log indiqué s'il existe
      """
      try:
         if os.path.isfile(fileName):
            os.remove(fileName)
      except:
         print("ERREUR ! Effacement fichier {} impossible !\n{}".format(fileName, sys.exc_info()))
      
if __name__ == "__main__":
   nomFichier = "journal.log"
   CLogger.effacerFichierLog(nomFichier)
   logger = CLogger(loggerName="journal", loggerLevel="DEBUG", consoleLevel="ERROR", \
                    fileName=nomFichier, fileLevel="DEBUG")
   logger.envoyerMessageTestTousNiveaux(num=1)
   print("")
   logger.afficherContenuFichier(fileName=nomFichier)
