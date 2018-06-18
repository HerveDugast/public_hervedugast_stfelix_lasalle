#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : ThreadContactPorte.py      version 1.0
Date : 30-05-2018
Auteur : Hervé Dugast

------ Affichage console --------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------
Connectique :
   carte : raspberry pi 3
   Sortie PWM    ->  GPIO18 (ou GPIO19) soit pin12 (ou pin35)
   Entrée button ->  GPIO14 (ou une autre) soit pin8
   Ground        ->  pin6, pin14, pin20, pin30, pin34
"""

import sys
import threading
import RPi.GPIO as GPIO
from CLogger import CLogger
import time
from gpiozero import Button

class ThreadContactPorte(threading.Thread):
   """ Détecte si un contact de porte est actif ou non, donc si une porte est ouverte ou fermée. 
       chaque objet de cette classe est exécutée dans un thread
   """
   __numThreadContactPorte = 0
   
   def __init__(self, pinInContact=14, pinOutContact=18, nomThread='', logger=''):
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
       print(self.logger)
       self.__nomThread = nomThread
       self.__etatCaptPorte = '?'
       threading.Thread.__init__(self, name=nomThread)
       self.__pinInContact = pinInContact 
      
   def executerPorteFerme(self):
        print("0")
       
   def executerPorteOuvert(self):
        print("1")

   def run(self):
      fonction = "ThreadContactPorte.run()"
      message = "Thread {}. Lancement -- {}".format(self.__nomThread, fonction)
      self.logger.info(message)
      self.contactPorte = Button(pin=self.__pinInContact, pull_up=True, bounce_time=None)
      
      self.contactPorte.when_pressed = self.executerPorteFerme
      self.contactPorte.when_released = self.executerPorteOuvert
      
      while 1:
          print("+",end='')
          time.sleep(1)

   

# Initialisation du serveur - Mise en place du socket :
if __name__ == "__main__":
    # mise un place d'un logger : 1 console et un fichier rotatif
    CLogger.effacerFichierLog("debugContactPorte.log")
    # ----- Mise en place du logger qui va gérer les handlers console et fichier rotatif
    logger = CLogger(loggerName="loggerContactPorte", loggerLevel="DEBUG", \
                       consoleLevel="INFO", fileName="debugContactPorte.log", fileLevel="DEBUG")    
    thContactPorte = ThreadContactPorte(nomThread='thContactPorte', logger=logger)
    thContactPorte.start()
   