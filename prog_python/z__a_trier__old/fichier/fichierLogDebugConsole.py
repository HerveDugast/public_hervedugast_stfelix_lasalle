#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : fichierLogDebugConsole.py     version : 1.1
Auteur : H. Dugast
Date : 15-05-2017
Matériel utilisé :  ordinateur sous windows (avec wing ide par exemple)
Fonction :
Créer un mécanisme pour écrire des messages sur différentes sorties en fonction du
niveau demandé (niveau possible : CRITICAL > ERROR > WARNING > INFO > DEBUG)
Ici, sorties : fichier log (WARNING), fichier debug (DEBUG) et console (INFO)

Source : http://sametmax.com/ecrire-des-logs-en-python/
Lire la documentation à l'URL indiquée pour comprendre le mécanisme des handlers

Exemple d'exécution pour ce programme :
--- Console affiche ---
06-05-2017 - INFO - Hello
06-05-2017 - WARNING - Testing foo

--- Contenu fichier activity.log ---
06-05-2017 23:10:47 :: WARNING :: Testing foo

--- Contenu fichier debug.log ---
INFO :: Hello
WARNING :: Testing foo
DEBUG ::  i = 1 	 i*i = 1
DEBUG ::  i = 2 	 i*i = 4
DEBUG ::  i = 3 	 i*i = 9
DEBUG ::  i = 4 	 i*i = 16
"""

import logging
from logging.handlers import RotatingFileHandler

# ----- logger : configuration -----
# Toujours mettre un niveau sur le logger plus bas que les handlers qui seront utilisés
# En effet, l'écriture vers la sortie (fichier, console, SMTP...) sera réellement
# faite en fonction du niveau des handlers (file_handler, steam_handler, SMTPHandler...)
LOGGER_LEVEL = logging.DEBUG  # niveau possible : CRITICAL > ERROR > WARNING > INFO > DEBUG
# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()
# on met le niveau du logger à DEBUG, comme ça le logger pourra tout écrire
logger.setLevel(LOGGER_LEVEL)

# ----- fichier log : configuration -----
# pour mémoriser les événements anormaux avec handler RotatingFileHandler
FILE_LOG_NAME = 'activity.log' 
FILE_LOG__LEVEL = logging.WARNING  # niveau possible : CRITICAL > ERROR > WARNING > INFO > DEBUG
FILE_LOG_FORMAT = '%(asctime)s :: %(levelname)s :: %(message)s'
FILE_LOG_DATE_FORMAT = '%d-%m-%Y %H:%M:%S'
FILE_LOG_SIZE = 1000000    # taille en octets du fichier log
# nombre de fichiers backups créés lorsque le fichier log est "plein" avec extension log.1,log.2 ...
FILE_LOG_BACKUP_NB = 10     # nombre de backups du fichier log
FILE_LOG_ENCODING = 'utf8'
# création d'un formateur qui va ajouter le temps, le niveau de chaque message quand on écrira un 
# message dans le log
formatter = logging.Formatter(FILE_LOG_FORMAT, FILE_LOG_DATE_FORMAT)
# création d'un handler qui va rediriger une écriture du log vers un fichier en mode 'append',
# et définition du nombre de backups et de la taille du fichier
file_handler = RotatingFileHandler(FILE_LOG_NAME, 'a', FILE_LOG_SIZE, FILE_LOG_BACKUP_NB, 
                                   FILE_LOG_ENCODING)
# ajout de cet handler au logger pour écrire les informations dans le fichier log 
file_handler.setLevel(FILE_LOG__LEVEL)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# ----- fichier debug : configuration  -----
# pour mémoriser des états de variables avec handler RotatingFileHandler
FILE_DEBUG_NAME = 'debug.log' 
FILE_DEBUG_LEVEL = logging.DEBUG  # niveau possible : CRITICAL > ERROR > WARNING > INFO > DEBUG
FILE_DEBUG_FORMAT = '%(levelname)s :: %(message)s'
FILE_DEBUG_SIZE = 10000    # taille en octets du fichier log
# nombre de fichiers backups créés lorsque le fichier log est "plein" avec extension log.1,log.2 ...
FILE_DEBUG_BACKUP_NB = 1   # nombre de backups du fichier log
# création d'un formateur qui va ajouter le temps, le niveau de chaque message quand on écrira un 
# message dans le log
formatter = logging.Formatter(FILE_DEBUG_FORMAT)
# création d'un handler qui va rediriger une écriture du log vers un fichier en mode 'append',
# et définition du nombre de backups et de la taille du fichier
file_handler = RotatingFileHandler(FILE_DEBUG_NAME, 'a', FILE_DEBUG_SIZE, FILE_DEBUG_BACKUP_NB)
# ajout de cet handler au logger pour écrire les informations dans le fichier log 
file_handler.setLevel(FILE_DEBUG_LEVEL)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# ----- console : configuration affichage -----
# pour afficher tout sauf le debug avec handler StreamHandler (équivalent sys.stdout, sys.stderr)
CONSOLE_LEVEL = logging.INFO  # niveau possible : CRITICAL > ERROR > WARNING > INFO > DEBUG
CONSOLE_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
CONSOLE_DATE_FORMAT = '%d-%m-%Y'
# création d'un second handler qui va rediriger chaque écriture de log sur la console
formatter = logging.Formatter(CONSOLE_FORMAT, CONSOLE_DATE_FORMAT)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(CONSOLE_LEVEL)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# Il est temps de spammer votre code avec des logs partout :
logger.info('Hello')
logger.warning('Testing %s', 'foo')
for i in range(1, 5):
   logger.debug(" i = {0} \t i*i = {1}".format(i, i*i))


