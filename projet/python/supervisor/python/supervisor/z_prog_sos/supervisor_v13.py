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
     exemple pour écrire dans un log au niveau warning -> logger.warning('Hello')
- Détection d'ouverture de porte et de défaut du détecteur
   fil 1 contact relié au +5V, fil 2 contact (Vscont) relié à R1, R2 et à une entrée CAN avec R1 = R2 = 10K
   L'autre côté de R1 est relié au +5V et l'autre côté de R2 est relié à GND (masse)
   Ainsi : contact ON -> Vscont = 5V -> code CAN = 131072
           contact OFF -> Vscont = 2,5V -> code CAN = 65536
           contact HS (exemple fil coupé ou déconnecté) -> Vscont proche de 0V -> code CAN < 10 << 65536

Exemple d'exécution pour ce programme :
--- Console affiche ---
15-05-2017 16:10:43 :: WARNING :: Mise sous tension du système supervisor
15-05-2017 16:10:43 - INFO - Attente information capteurs...

--- Contenu fichier supervision.log ---
15-05-2017 16:10:43 - WARNING - Mise sous tension du système supervisor


"""
import sys 
sys.path.append("/home/pi/supervisor/BMP280")
import logging
from logging.handlers import RotatingFileHandler
from Bddmysql.Bddmysql import *
import sys
import mysql.connector
import BMP280
import time
from datetime import datetime, timedelta
import threading
import locale
from RaspiomixHd.raspiomixHd import RaspiomixHd
import RPi.GPIO as GPIO

# la méthode strftime utilise le système de date local (qui dépend de l'environnement d'exécution)
# ici, nous sommes en France donc format JJ/MM/AA HH:MM:SS
locale.setlocale(locale.LC_TIME,'')

# ----- Base de données : paramètres configuration -----
host = "217.128.90.45"
port = 3306
user = "dbsupervis_user"
password = "Nantes44"
database = "dbsupervis"

# ----- Système embarqué et capteurs -----
# nom du capteur de temperature intérieur dans la bdd connecté au système embarqué
#    -> nom du champ "nom" de la table "capteur"
SYSTEME_EMBARQUE = "raspi3-J518"
# Création objet capteur température et pression (BMP280) -----
sensor = BMP280.BMP280()

captTempIn518 = {}
captTempIn518["nom"] = "Temperat_in_518"   # capteur de température
captTempIn518["corr"] = -1  # correctif, ce capteur retourne une valeur très souvent 1°C au-dessus de la valeur réelle
captTempIn518["periodeSec"] = 1  # durée entre 2 mesures en secondes, cette valeur sera écrasée par la valeur stockée dans la bdd

captPres518 = {}
captPres518["nom"] = "Pression_518"   # capteur de température
captPres518["periodeSec"] = 1  # durée entre 2 mesures en secondes, cette valeur sera écrasée par la valeur stockée dans la bdd

ETAT_INCONNU = 999   # contact dans un état inconnu
ETAT_ON = 0        # contact fermé, porte fermée
ETAT_OFF = 1      # contact ouvert, porte ouverte
CODE_MIN_ON = 120000 # contact ON -> 5 soit code = 2^17 = 131072 >> 120000 
CODE_MIN_OFF = 50000 # contact OFF -> 2,5V soit code = 2^17 / 2 = 65536>> 50000

CONTACT_A_518_PIN = 1      # contact connecté sur entrée analogique Anx, x : numéro de l'entrée
captContA518 = {}
captContA518["nom"] = "ContactA_518"   # détecteur de porte
captContA518[0] = {}
captContA518[0]["dateHeure"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
captContA518[0]["etatNow"] = ETAT_INCONNU
captContA518[0]["etatPrec"] = ETAT_INCONNU

# index permettant de mémoriser les différents états de la porte
# L'état du contact de la porte peut changer plusieurs fois d'états durant l'enregistrement d'1 état
# dans la bdd. On ne peut donc pas attendre la fin d'écriture avant de lire à nouveau l'état du
# contact. On utilise donc un dictionnaire à 2 dimensions et un système d'index : 1 index
# (idxA518mes) pour pointer le dernier changement d'état et 1 autre (idxA518bdd) pour pointer les
# informations enregistrées dans la bdd. idxA518bdd <= idxA518mes
IDX_VAL_MAX = 20   # nb de valeurs du dictionnaire à 2 dimensions, on reprend à 1 après VAL_MAX
idxA518mes = 0
idxA518bdd = 0

# ----- Autres variables et constantes -----
errorMsg = "OK"

# ----- Ports GPIO -----
LED = RaspiomixHd.IO0

GPIO.setwarnings(False) # évite l'affichage d'un message Warning
GPIO.setmode(GPIO.BOARD) # mode de fonctionnement GPIO
GPIO.setup(LED, GPIO.OUT) # configure port en sortie


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

# ----- Thread pour vérifier l'accès à la base de données -----
def thread_verifBdd(tempo):
   """ thread lancé automatiquement toutes les "tempo" heures
   Effectue les mesures de température et pression atmosphérique """
   threading.Timer(tempo * 3600, thread_verifBdd, [tempo]).start() 
   cnx = bdd._bdd_connecter()
   if bdd.m_messageError == "OK":
      logger.info("*** Connexion à la bdd "  + bdd.m_database + " réussie ***")
      time.sleep(1)
      bdd._bdd_deconnecter(cnx)   
   else:
      logger.error("ECHEC connexion à la bdd "  + bdd.m_database)

# ----- Enregistrer relevé dans bdd -----
def bdd_enregistrer_releve(releve):
   """ enregistre un relevé (température, pression...) dans la bdd
       paramètres entrées : dico ("date_heure" : datetime, "valeur" : int, "capteur_id" : int" """

   sqlQuery = "INSERT INTO releve_capteur (date_heure, valeur, capteur_id) "  \
      "VALUES (%s, '%s', '%s')"
   bdd.executerReqInsertUpdateDelete(sqlQuery, releve["date_heure"], releve["valeur"], releve["capteur_id"])
   
def thread_captTempIn518(tempo): 
   """ Mesure la température avec le capteur indiqué toutes les tempo secondes
       Attention à ce que la durée du traitement dans ce thread ne dépasse pas
       la valeur tempo sous peine de fontionnement bizarre """
   threading.Timer(tempo, thread_captTempIn518, [tempo]).start() 
   ## Reste du traitement

   global errorMsg, captTempIn518
   heureDebutThread = datetime.now()
   dateHeureMes = heureDebutThread.strftime('%Y-%m-%d %H:%M:%S')
   releve = {}    # création d'un dico

   try:
      verrouBmp280.acquire()  # verrouille l'accès à la ressource
      mesTemperature = int( (sensor.read_temperature() + captTempIn518["corr"]) * 10)
      print(dateHeureMes, '  Temp = ', str(mesTemperature / 10) + "°C")
      verrouBmp280.release()  # déverrouille l'accès à la ressource

      # --- préparation de la mémorisation du relevé dans la bdd ---
      # complète les 2 premières valeurs du relevé
      releve["date_heure"] = dateHeureMes
      releve["valeur"] = mesTemperature

      # Récupère la valeur de la clé étrangère du capteur
      sqlQuery = "SELECT id FROM capteur WHERE nom LIKE %s"
      resultSelect = bdd.getResultatReqSelect(sqlQuery, captTempIn518["nom"])
      if len(resultSelect) != 0:
         releve["capteur_id"] = resultSelect[0][0]
         bdd_enregistrer_releve(releve)
      else:
         errorMsg = "Pas de valeur de capteur.id correspondant à captTempIn518['nom']"

##      heureFinThread = datetime.now()
##      duree = heureFinThread - heureDebutThread
##      print("durée thread Temp = ", duree)

   except OSError as err :
      errorMsg = "OSError mesTemperature" + str(err)
   except UnboundLocalError as err :
      errorMsg = "UnboundLocalError mesTemperature" + str(err)
   except:
      errorMsg = "Error unknown mesTemperature"
   if errorMsg != "OK":
      logger.error(errorMsg)

def thread_captPres518(tempo):
   """ Mesure la pression atmosphérique avec le capteur indiqué toutes les tempo secondes
       Attention à ce que la durée du traitement dans ce thread ne dépasse pas
       la valeur tempo sous peine de fontionnement bizarre """
   threading.Timer(tempo, thread_captPres518, [tempo]).start() 
   ## Reste du traitement
   
   global errorMsg, captPres518
   heureDebutThread = datetime.now()
   dateHeureMes = heureDebutThread.strftime('%Y-%m-%d %H:%M:%S')
   releve = {}    # création d'un dico

   try:
      verrouBmp280.acquire()  # verrouille l'accès à la ressource
      mesPression = int(sensor.read_pressure() / 100)
      print(dateHeureMes, '  Pres = ', str(mesPression) + "mbar")
      verrouBmp280.release()  # déverrouille l'accès à la ressource

      # --- préparation de la mémorisation du relevé dans la bdd ---
      # complète les 2 premières valeurs du relevé
      releve["date_heure"] = dateHeureMes
      releve["valeur"] = mesPression

      # Récupère la valeur de la clé étrangère du capteur
      sqlQuery = "SELECT id FROM capteur WHERE nom LIKE %s"
      resultSelect = bdd.getResultatReqSelect(sqlQuery, captPres518["nom"])
      if len(resultSelect) != 0:
         releve["capteur_id"] = resultSelect[0][0]
         bdd_enregistrer_releve(releve)
      else:
         errorMsg = "Pas de valeur de capteur.id correspondant à captPres518['nom']"

##      heureFinThread = datetime.now()
##      duree = heureFinThread - heureDebutThread
##      print("durée thread Pres = ", duree)

   except OSError as err :
      errorMsg = "OSError mesPression" + str(err)
   except UnboundLocalError as err :
      errorMsg = "UnboundLocalError mesPression" + str(err)
   except:
      errorMsg = "Error unknown mesPression"
   if errorMsg != "OK":
      logger.error(errorMsg)

def thread_led(tempo): 
    threading.Timer(tempo, thread_led, [tempo]).start() 
    ## Reste du traitement
    GPIO.output(LED, not GPIO.input(LED))
    
# ----- Thread pour lire l'état des contacts -----
def thread_contactA_518(tempo): 
   threading.Timer(tempo, thread_contactA_518, [tempo]).start() 
   ## Reste du traitement
   global errorMsg, captContA518, idxA518mes

   verrouContactA518.acquire()  # verrouille l'accès à la ressource
   heureDebutThread = datetime.now()
   dateHeureMes = heureDebutThread.strftime('%Y-%m-%d %H:%M:%S')

    # lecture état contact
   codeContact = contactA518.readAdcCode(CONTACT_A_518_PIN)
   captContA518[idxA518mes + 1] = {}  # création d'un relevé supplémentaire
   captContA518[idxA518mes + 1]["dateHeure"] = dateHeureMes

   if codeContact > CODE_MIN_ON:
      captContA518[idxA518mes + 1]["etatNow"] = ETAT_ON
   elif codeContact > CODE_MIN_OFF:
      captContA518[idxA518mes + 1]["etatNow"] = ETAT_OFF
   else:
      captContA518[idxA518mes + 1]["etatNow"] = ETAT_INCONNU
      captContA518[idxA518mes + 1]["etatPrec"] = ETAT_INCONNU
      errorMsg = "Impossible de lire l'état du contact CONTACT_A_518_PIN, vérifiez la connectique !"
      logger.error(errorMsg)

   # Si changement d'état
   if captContA518[idxA518mes + 1]["etatNow"] != captContA518[idxA518mes]["etatPrec"]:
      captContA518[idxA518mes + 1]["etatPrec"] = captContA518[idxA518mes + 1]["etatNow"]

      idxA518mes = idxA518mes + 1  # validation de la mémorisation du relevé
      if idxA518mes == IDX_VAL_MAX + 1:
         idxA518mes = 0
         captContA518[0]["dateHeure"] = dateHeureMes
         captContA518[0]["etatPrec"] = captContA518[IDX_VAL_MAX + 1]["etatPrec"]
         captContA518[0]["etatNow"] = captContA518[IDX_VAL_MAX + 1]["etatNow"]

   verrouContactA518.release()  # déverrouille l'accès à la ressource

def contactA_518_memoriser_bdd():
   global errorMsg, captContA518, idxA518bdd

   releve = {}    # création d'un dico
   # --- préparation de la mémorisation du relevé dans la bdd ---
   # complète les 2 premières valeurs du relevé
   releve["date_heure"] = captContA518[idxA518bdd + 1]["dateHeure"]
   releve["valeur"] = captContA518[idxA518bdd + 1]["etatNow"]

   # écriture dans console
   if releve["valeur"] == ETAT_ON:
      print(releve["date_heure"],'  Porte 1-518 fermée ... contact 1-518 =', releve["valeur"], ' (ON)')
   else:
      print(releve["date_heure"],'  Porte 1-518 ouverte ... contact 1-518 =', releve["valeur"], ' (OFF)')

   # Récupère la valeur de la clé étrangère du capteur
   sqlQuery = "SELECT id FROM capteur WHERE nom LIKE %s"
   resultSelect = bdd.getResultatReqSelect(sqlQuery, captContA518["nom"])
   if len(resultSelect) != 0:
      releve["capteur_id"] = resultSelect[0][0]
      bdd_enregistrer_releve(releve)
   else:
      errorMsg = "Pas de valeur de capteur.id correspondant à captContA518['nom']"


#   dico_2d_afficher_contact(captContA518) # Affichage de la liste circulaire des relevés

   idxA518bdd = idxA518bdd + 1
   if idxA518bdd == IDX_VAL_MAX + 1:
      idxA518bdd = 0
      
def dico_2d_afficher_contact(dico):
   """ affiche le contenu d'un dictionnaire à 2 dimensions """
   for i in range(idxA518mes + 1):
      #try:
         print("* ", i, dico[i]["dateHeure"], "  Now :", dico[i]["etatNow"], "  Préc :",
               dico[i]["etatPrec"])
      #except:
      #   pass

def bdd_creer_objet_bdd():
   """ Création objet base de données pour mémoriser les paramètres de connexion et disposer de
       méthodes de manipulation de bdd : host, port, user, password, database
       Retour : objet connecteur base de données """
   global errorMsg, bdd
   print('Connexion à la base de données en cours')
   # Remarque : la durée pour établir la connexion avant de signaler un échec
   #            peut dépendre du timeout configuré sur le serveur de bdd, soyez patient !   logger.info('*** Connexion à la base de données réussie ***')
   try:
      bdd = Bddmysql(host, port, user, password, database)
      return bdd
   except NameError as err:
      errorMsg = "'NameError', pb importation module Bddmysql.py : " + str(err)
      logger.error(errorMsg)
      logger.warning("*** Fin programme à cause de l'erreur !!! ***")
      sys.exit(0)
   except:
      errorMsg = "Erreur accès base de données"      
      logger.error(errorMsg)
      logger.warning("*** Fin programme à cause de l'erreur !!! ***")
      sys.exit(0)

def bdd_recuperer_periode_mesure():
   """ récupère dans la base de données les champs utiles au fonctionnement du système """
   global errorMsg, captTempIn518, captPres518

   # Récupère les périodicités de mesure dans la base de données
   sqlQuery = "SELECT freq_releve_sec FROM capteur WHERE nom LIKE %s"
   resultSelect = bdd.getResultatReqSelect(sqlQuery, captTempIn518["nom"])
   if len(resultSelect) != 0:
      captTempIn518["periodeSec"] = resultSelect[0][0]
   else:
      errorMsg = "Pas de valeur de capteur.freq_releve_sec correspondant à captTempIn518['nom']"
   if errorMsg != "OK":
      logger.error(errorMsg)

   sqlQuery = "SELECT freq_releve_sec FROM capteur WHERE nom LIKE %s"
   resultSelect = bdd.getResultatReqSelect(sqlQuery, captPres518["nom"])
   if len(resultSelect) != 0:
      captPres518["periodeSec"] = resultSelect[0][0]
   else:
      errorMsg = "Pas de valeur de capteur.freq_releve_sec correspondant à captPres518['nom']"
   if errorMsg != "OK":
      logger.error(errorMsg)

def bdd_verifier_existence_detecteur_porte():
   """ Vérifie si le contact servant à détecter l'ouverture de la porte est bien présent dans la
       base de données """
   global errorMsg
   sqlQuery = "SELECT id FROM capteur WHERE nom LIKE %s"
   resultSelect = bdd.getResultatReqSelect(sqlQuery, captContA518["nom"])
   if len(resultSelect) == 0:
      errorMsg = "Aucun capteur trouvé dans la table capteur avec un nom correspondant à captContA518['nom']"
   if errorMsg != "OK":
      logger.error(errorMsg)

def bdd_requete_retour_1_valeur(champNomRetour, table, champNomCritere, chaineCaract):
   """ retourne la valeur du champ id de la table indiquée correspondant à la valeur (type texte) du champ
       nomChamp, s'il trouve la clé étrangère. Sinon, retourne -1 et génère une erreur qui sera journalisée
       Requête de la forme : SELECT champNomRetour FROM table WHERE champNomCritere LIKE chaineCaract"""
   global errorMsg
   
   errorMsg = "OK"
   sqlQuery = "SELECT " + champNomRetour + " FROM " + table + " WHERE " + champNomCritere + " LIKE %s"
   print("1", sqlQuery)
   resultSelect = bdd.getResultatReqSelect(sqlQuery, chaineCaract)
   if len(resultSelect) != 0:
      return resultSelect[0][0]
   else:
      errorMsg = "Aucun résultat pour la requête : SELECT " + champNomRetour + " FROM " + table + " WHERE " + \
         champNomCritere + " LIKE " + chaineCaract
      logger.error(errorMsg)
      return -1

def journal_ecrire_bdd(dateHeure, niveauAlerte, capteurNom, message):
   """ écrit un message avec différentes informations dans la table journalisation de la bdd """
   global errorMsg
   journal = {}
   journal["date_heure"] = dateHeure
   # recherche clé étrangère niveau_id
   journal["niveau_id"] = bdd_requete_retour_1_valeur("id", "niveau", "niveau_alerte", "Warning")
   if capteurNom != 'NULL':
      journal["capteur_id"] = capteurNom
   else:
      journal["capteur_id"] = ""
   journal["message"] = message
   _bdd_enregistrer_journalisation(journal)
   
def _bdd_enregistrer_journalisation(journal):
   """ enregistre une ligne de journal (Warning ou Error) dans la bdd
       paramètres entrées : dico ("date_heure" : datetime, "niveau_id" : int, "capteur_id" : int",
          "message" : chaine """

   if journal["capteur_id"] != 'NULL':
      sqlQuery = "INSERT INTO journalisation (date_heure, niveau_id, capteur_id, message) "  \
         "VALUES (%s, '%s', '%s', %s)"
      bdd.executerReqInsertUpdateDelete(sqlQuery, journal["date_heure"], journal["niveau_id"], \
                                        journal["capteur_id"], journal["message"])
   else:
      sqlQuery = "INSERT INTO journalisation (date_heure, niveau_id, message) "  \
         "VALUES (%s, '%s', %s)"
      bdd.executerReqInsertUpdateDelete(sqlQuery, journal["date_heure"], journal["niveau_id"], \
                                        journal["message"])
      
   
   
# -------------------------------------------------------------------------------------------------
#  PROGRAMME PRINCIPAL
# -------------------------------------------------------------------------------------------------

message = 'Mise sous tension du système supervisor'
logger.warning(message)
dateHeure = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   
# ----- Création objet base de données -----
bdd_creer_objet_bdd()

#journal_ecrire_bdd(dateHeure, "Warning", "NULL", message)
bdd_recuperer_periode_mesure()
bdd_verifier_existence_detecteur_porte()

# ----- Verrou pour bloquer les threads dans certains cas (accès à la même ressource -----
verrouBmp280 = threading.Lock()
verrouContactA518 = threading.Lock()

# ----- Création objet capteur température et pression (BMP280) -----
thread_captTempIn518(captTempIn518["periodeSec"])
thread_captPres518(captPres518["periodeSec"])

# ----- Préparation du détecteur d'ouverture (contact) -----
contactA518 = RaspiomixHd()

contactEtatPrec = ETAT_INCONNU
# Attention, ne pas descendre en-dessous 0.5 seconde, sous peine de fonctionnement bizarre
# Choisir 1 seconde signifie que l'état du contact est lu toutes les secondes
#   Dans ce cas si le contact change d'état 2 fois en moins de 1s, ce changement peut ne pas être détecté
thread_contactA_518(0.5) # lecture contact toutes les x secondes (0.01 -> 10 ms)

# ----- pour vérifier visuellement que le programme tourne correctement -----
thread_led(0.5)    # Clignotement LED

while True:
   while idxA518bdd != idxA518mes:
      contactA_518_memoriser_bdd()
      


