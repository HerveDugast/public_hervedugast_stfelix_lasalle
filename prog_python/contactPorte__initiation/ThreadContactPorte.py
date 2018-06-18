#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : ThreadContactPorte.py      version 1.1
Date : 12-06-2018
Auteur : Hervé Dugast

Détecte l'état d'une porte à l'aide d'un détecteur magnétique (contact + aimant)
La porte peut prendre l'un de ses trois états : Open, Close ou Unknown

------ Affichage console --------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------
Connectique :
   carte : raspberry pi 3
   Sortie PWM    ->  GPIO18 soit pin12 (bcm12)
   Entrée button ->  GPIO17 soit pin11 (bcm11)
   Ground        ->  choisir parmi : pin6, pin14, pin20, pin30, pin34
   voir schéma connectique contact porte : fichier detection_etat_porte_3_etats_raspberry.pdf
"""

import sys
import threading
import RPi.GPIO as GPIO
from CLogger import CLogger
import time, datetime
from gpiozero import Button, PWMLED

class ThreadContactPorte(threading.Thread):
   """ Détecte si un contact de porte est actif ou non, donc si une porte est ouverte ou fermée. 
       chaque objet de cette classe est exécutée dans un thread
   """
   __numThreadContactPorte = 0
   
   def __init__(self, pinInContact=17, pinOutContact=18, nomThread='', logger=''):
       """ constructeur
           Consulter commentaires classe CLogger pour en savoir plus sur les autres paramètres
           variable membre :
           self.__etatCaptPorte : caractère, 3 états possibles  
                                     '?':inconnu (possibilité panne)   'O':ouvert    'F':fermé
           self.__pinInContact : int, numéro broche entrée contact porte notation BCM
                                  exemple : GPIO14 -> self.__pinInContact = 14  
           self.__pinOutContact : int, numéro broche sortie PWM vers contact
                                  exemple : GPIO18 -> self.__pinOutContact = 18  
       """
       fonction = "ThreadContactPorte.__init__(...)"
       # ----- Mise en place du logger qui va gérer les handlers console et fichier rotatif
       self.logger = logger
       self.__nomThread = nomThread
       self.__etatCaptPorte = '?'
       threading.Thread.__init__(self, name=nomThread)
       self.__pinInContact = pinInContact 
       self.__pinOutContact = pinOutContact
       self.__nbFront = 0
       self.__nbFrontPrec = 99
       self.__niveauInContactPrec = False
       self.__etatPorte = "Unknown"
       self.__etatPortePrec = "titi"
      
   def definirEtatPorte(self, nbFront, niveauInContact):
      """ Retourne l'état du contact. L'état de la porte est définie à l'aide de 2 variables :
          - niveauInContact : booléen, niveau logique présent sur l'entrée numérique
            pinInContact
          - nbFront : int, nombre de changement d'états sur l'entrée numérique pinInContact
            pendant une durée définie (dureeMes = 100 ms). nbFront est remis à 0 à la fin de
            chaque dureeMes.
            
          La porte peut prendre 3 états différents :
          - etatPorte = 'Close' : porte fermée -> contact fermé
                  condition : niveauInContact = True et nbFront = 0, au moins 2 fois de suite
          - etatPorte = 'Open' : porte ouverte -> contact ouvert (Vin -> PWM avec PWM = 25Hz)
                  condition : nbFront compris entre 3 et 7, au moins 2 fois de suite
          - etatPorte = 'Unknown' : état porte inconnue (fil contact coupé...)
                  condition : niveauInContact = False et nbFront = 0, au moins 2 fois de suite
          Tous les autres cas n'entrainent pas de changement d'état de la variable etatPorte
          Retour:
              etatPorte : chaine caractères,   'Close', 'Open' ou 'Unknown'
      """
      fonction = "ThreadContactPorte.definirEtatPorte(...)"
      if niveauInContact and nbFront == 0 and self.__niveauInContactPrec \
         and self.__nbFront == 0:
          self.__etatPorte = 'Close'
      elif 3 <= nbFront <= 7 and 3 <= self.__nbFrontPrec <= 7:
          self.__etatPorte = 'Open'
      elif niveauInContact == False and nbFront == 0 and self.__niveauInContactPrec == False \
         and self.__nbFront == 0:
          self.__etatPorte = 'Unknown'
          
      if self.__etatPorte != self.__etatPortePrec:
          message ="Thread {}. Door : {} -- {}".format(self.__nomThread, self.__etatPorte, fonction)
          self.logger.info(message)
          print(self.__etatPorte)
      self.__etatPortePrec = self.__etatPorte

   def executerPorteFerme(self):
        #print("0")
       self.__nbFront += 1
       
   def executerPorteOuvert(self):
        #print("1")
       self.__nbFront += 1

   def run(self):
      fonction = "ThreadContactPorte.run()"
      message = "Thread {}. Lancement -- {}".format(self.__nomThread, fonction)
      self.logger.info(message)
      self.contactPorte = Button(pin=self.__pinInContact, pull_up=True, bounce_time=None)
      
      self.contactPorte.when_pressed = self.executerPorteFerme
      self.contactPorte.when_released = self.executerPorteOuvert
      
      #self.contactOutPwm = PWMLED(pin=self.__pinOutContact, frequency=5000)
      #self.contactOutPwm.pulse()
      
      GPIO.setmode(GPIO.BCM)
      GPIO.setup(18, GPIO.OUT)

      p = GPIO.PWM(18, 25)
      p.start(50)
      #self.contactOutPwm.blink(on_time=0.025, off_time=0.025)
      timePrec = datetime.datetime.now()
      while 1:
          timeNow = datetime.datetime.now()
          delta = timeNow - timePrec
          #dureeEnSecond = round(duree.total_seconds())
          if int(delta.total_seconds()*1000) >= 100: # en ms
              timePrec = timeNow
              #print(self.__nbFront, self.contactPorte.is_pressed)
              self.__niveauInContact = self.contactPorte.is_pressed
              self.definirEtatPorte(self.__nbFront, self.__niveauInContact)
              self.__niveauInContactPrec = self.__niveauInContact
              self.__nbFrontPrec = self.__nbFront
              self.__nbFront = 0
  

# Initialisation du serveur - Mise en place du socket :
if __name__ == "__main__":
    PIN_IN_CONTACT = 17   # entrée numérique permettant de lire l'état du contact de porte
    PIN_OUT_CONTACT = 18   # sortie PWM raspberry (soit GPIO18 : bcm12, soit GPIO13 : bcm33)

    # mise un place d'un logger : 1 console et un fichier rotatif
    CLogger.effacerFichierLog("debugContactPorte.log")
    # ----- Mise en place du logger qui va gérer les handlers console et fichier rotatif
    logger = CLogger(loggerName="loggerContactPorte", loggerLevel="DEBUG", \
                       consoleLevel="INFO", fileName="debugContactPorte.log", fileLevel="DEBUG")    
    thContactPorte = ThreadContactPorte(pinInContact=PIN_IN_CONTACT, pinOutContact=PIN_OUT_CONTACT,\
                                        nomThread='thContactPorte', logger=logger)
    thContactPorte.start()
   