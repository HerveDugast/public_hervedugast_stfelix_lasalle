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


Exemple d'exécution pour ce programme :
--- Console affiche ---
15-05-2017 16:10:43 :: WARNING :: Mise sous tension du système supervisor
15-05-2017 16:10:43 - INFO - Attente information capteurs...

--- Contenu fichier supervision.log ---
15-05-2017 16:10:43 - WARNING - Mise sous tension du système supervisor


"""

from RaspiomixPlus.raspiomix import Raspiomix
import RPi.GPIO as GPIO
import threading

LED = Raspiomix.IO0
CONTACT_1 = Raspiomix.IO4
NB_ETAT_ON_MIN = 10 # il faut NB_ETAT_ON_MIN lectures successives à ON pour détecter contact fermé
global contactEtat, contactEtatPrec

GPIO.setwarnings(False) # évite l'affichage d'un message Warning

GPIO.setmode(GPIO.BOARD) # mode de fonctionnement GPIO
GPIO.setup(LED, GPIO.OUT) # configure port en sortie

GPIO.setup(CONTACT_1, GPIO.IN)

def thread_led(tempo): 
    threading.Timer(tempo, thread_led, [tempo]).start() 
    ## Reste du traitement
    GPIO.output(LED, not GPIO.input(LED))
    
def thread_contact(tempo): 
    threading.Timer(tempo, thread_contact, [tempo]).start() 
    ## Reste du traitement
    global contactEtat
       # initialisation variable statique compteurs température et pression
    thread_contact.count = getattr(thread_contact, 'count', 0)
    contactNow = GPIO.input(CONTACT_1)
    # comptage du nombre successif d'état ON (contact fermé)
    if contactNow == True:
        thread_contact.count += 1
    else:
        thread_contact.count = 0
    if thread_contact.count > NB_ETAT_ON_MIN:
        thread_contact.count = NB_ETAT_ON_MIN
    #print(thread_contact.count) 
    # si nombre d'états successifs lus à ON est atteint -> contact fermé détecté
    if thread_contact.count == NB_ETAT_ON_MIN:
        contactEtat = True
    else:
        contactEtat = False
    

def thread_affichage(tempo): 
    threading.Timer(tempo, thread_affichage, [tempo]).start() 
    ## Reste du traitement
    global contactEtat, contactEtatPrec 
    if contactEtat != contactEtatPrec:
        if contactEtat:
            print("on")
        else:
            print("off")
        contactEtatPrec = contactEtat
        
contactEtat = GPIO.input(CONTACT_1)
contactEtatPrec = not contactEtat
thread_led(1)
thread_contact(0.01)
thread_affichage(0.02)
