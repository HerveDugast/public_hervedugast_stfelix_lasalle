#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : logger1.py     version : 1.0
Auteur : H. Dugast
Date : 04-04-2018
Source : https://deusyss.developpez.com/tutoriels/Python/Logger/
Auteur source : GALODE Alexandre

Fonctionnement :
  Effectue un traçage des événements qui se produisent lors de l'exécution du programme. Ceux-ci
  sont mémorisés dans 2 fichiers :
     - fichier critic.log : mémorise les informations de niveau CRITICAL
     - fichier info.log : mémorise les informations de niveaux CRITICAL, ERROR, WARNING et INFO

------------- Contenu fichier critic.log après exécution ----------------------------------------
2018-04-04 18:23:51,387 -- journal -- CRITICAL -- message ERROR 2
-------------------------------------------------------------------------------------------------
------------- Contenu fichier info.log après exécution ----------------------------------------
2018-04-04 18:23:51,387 -- journal -- INFO -- message ERROR 1
2018-04-04 18:23:51,387 -- journal -- CRITICAL -- message ERROR 2
2018-04-04 18:23:51,387 -- journal -- WARNING -- message WARNING 1
-------------------------------------------------------------------------------------------------

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

# définit le format des messages
formatter = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")

# création de 2 handlers de types fichiers pour mémoriser les niveaux CRITICAL et INFO
handler_critic = logging.FileHandler("critic.log", mode="a", encoding="utf-8")
handler_info = logging.FileHandler("info.log", mode="a", encoding="utf-8")

# applique le format des messages précédemment défini aux handlers
handler_critic.setFormatter(formatter)
handler_info.setFormatter(formatter)

# fixe le niveau de sensibilité pour chaque handler
handler_info.setLevel(logging.INFO)
handler_critic.setLevel(logging.CRITICAL)

# donne un nom au logger qui transmettra les messages aux handlers
logger = logging.getLogger("journal")
# fixe son niveau de sensibilité
logger.setLevel(logging.INFO)
# lie les 2 handlers précédemment créés au logger
logger.addHandler(handler_critic)
logger.addHandler(handler_info)

# Envoi de messages de niveau différent au logger
logger.debug('message DEBUG 1 ')
logger.info('message ERROR 1')
logger.critical('message ERROR 1')
logger.warning('message WARNING 1')

logger.debug('message DEBUG 2 ')
logger.info('message ERROR 2')
logger.critical('message ERROR 2')
logger.warning('message WARNING 2')