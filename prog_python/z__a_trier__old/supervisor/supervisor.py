#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : supervis.py     version : 1.0
Auteur : H. Dugast
Date : 15-05-2017
Matériel utilisé :  ordinateur sous windows (avec wing ide par exemple)
Fonction :
- Mise en place d'un logger pour : 
   - mémoriser les informations importantes dans un fichier supervision.log (niveau WARNING)
   - afficher les informations utiles dans une console (niveau INFO)
   - mémoriser les informations de débogage dans le fichier debug.log (niveau DEBUG)
   Remarque :
     hiérarchie de niveau : CRITICAL > ERROR > WARNING > INFO > DEBUG
     exemple pour écrire dans un log au niveau info -> logger.info('Hello')
     exemple pour écrire dans un log au niveau warning -> logger.wrning('Hello')


Exemple d'exécution pour ce programme :
--- Console affiche ---
15-05-2017 16:10:43 :: WARNING :: Mise sous tension du système supervisor
15-05-2017 16:10:43 - INFO - Attente information capteurs...

--- Contenu fichier supervision.log ---
15-05-2017 16:10:43 - WARNING - Mise sous tension du système supervisor


"""

import logging
from logging.handlers import RotatingFileHandler
from Bddmysql.Bddmysql import *
import sys
import mysql.connector
import time

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
FILE_LOG_NAME = 'supervision.log' 
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

# ----- fichier debug : paramètres configuration (utile pour mise au point) -----
# pour mémoriser des états de variables avec handler RotatingFileHandler
FILE_DEBUG_NAME = 'debug.log' 
FILE_DEBUG_LEVEL = logging.DEBUG  # niveau possible : CRITICAL > ERROR > WARNING > INFO > DEBUG
FILE_DEBUG_FORMAT = '%(levelname)s :: %(message)s'
FILE_DEBUG_SIZE = 10000    # taille en octets du fichier log
# nombre de fichiers backups créés lorsque le fichier log est "plein" avec extension log.1,log.2 ...
FILE_DEBUG_BACKUP_NB = 1   # nombre de backups du fichier log
FILE_DEBUG_ENCODING = 'utf8'
# création d'un formateur qui va ajouter le temps, le niveau de chaque message quand on écrira un 
# message dans le log
formatter = logging.Formatter(FILE_DEBUG_FORMAT)
# création d'un handler qui va rediriger une écriture du log vers un fichier en mode 'append',
# et définition du nombre de backups et de la taille du fichier
file_handler = RotatingFileHandler(FILE_DEBUG_NAME, 'a', FILE_DEBUG_SIZE, FILE_DEBUG_BACKUP_NB, 
                                   FILE_DEBUG_ENCODING)
# ajout de cet handler au logger pour écrire les informations dans le fichier log 
file_handler.setLevel(FILE_DEBUG_LEVEL)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# ----- affichage console : paramètres configuration -----
# pour afficher tout sauf le debug avec handler StreamHandler (équivalent sys.stdout, sys.stderr)
CONSOLE_LEVEL = logging.INFO  # niveau possible : CRITICAL > ERROR > WARNING > INFO > DEBUG
CONSOLE_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
CONSOLE_DATE_FORMAT = '%d-%m-%Y %H:%M:%S'
# création d'un second handler qui va rediriger chaque écriture de log sur la console
formatter = logging.Formatter(CONSOLE_FORMAT, CONSOLE_DATE_FORMAT)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(CONSOLE_LEVEL)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# -------------------------------------------------------------------------------------------------
#  PROGRAMME PRINCIPAL
# -------------------------------------------------------------------------------------------------

logger.warning('Mise sous tension du système supervisor') 
logger.info('Attente information capteurs...')

# Création d'un objet base de données qui mémorisera les paramètres de connexion et permettra
# d'accéder à des méthodes bien pratiques pour manipuler les base de données.
# ATTENTION ! host -> mettre adresse IP du serveur de base de données de la section
# ATTENTION ! password -> mettre même mot de passe que compte windows local installateur     
host = "217.128.90.45"
port = 3306
user = "dbsupervis_user"
password = "Nantes44"
database = "dbsupervis"
errorMsg = "OK"
logger.info('*** Connexion à la base de données en cours ***')
logger.info("Remarque : la durée pour établir la connexion avant de signaler un échec " \
         "peut dépendre du timeout configuré sur le serveur de bdd, soyez patient !")
try:
   bdd = Bddmysql(host, port, user, password, database)
except NameError as err:
   errorMsg = "'NameError', pb importation module Bddmysql.py : " + str(err)
   logger.error(errorMsg)
   logger.warning("*** Fin programme à cause de l'erreur !!! ***")

if errorMsg == "OK":
   cnx = bdd._bdd_connecter()
   if bdd.m_messageError == "OK":
      logger.info("*** Connexion à la bdd "  + bdd.m_database + " réussie ***")
      time.sleep(1)
      bdd._bdd_deconnecter(cnx)   
   else:
      logger.error("ECHEC connexion à la bdd "  + bdd.m_database)
      logger.warning("*** Fin programme à cause de l'erreur !!! ***")
