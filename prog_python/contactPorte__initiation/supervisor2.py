#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : Supervisor2.py      version 1.1
Date : 12-06-2018
Auteur : Hervé Dugast

Supervise un système embarqué qui gère les opérations suivantes :
- détecte l'état d'une porte d'une salle : Open, Close ou Unknown
- mesure la température intérieure de la salle en °C toutes les x minutes
- mesure la pression atmosphérique en millibar toutes les x minutes
- journalise chaque événement (détection état porte, mesures) dans une bdd
- journalise les éventuelles erreurs dans un fichier supervisor_erreur.log

------ Affichage console --------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------
Connectique :
   carte : raspberry pi 3
   Sortie PWM    ->  GPIO18 soit pin12 (bcm12)
   Entrée button ->  GPIO17 soit pin11 (bcm11)
   Ground        ->  choisir parmi : pin6, pin14, pin20, pin30, pin34
   voir schéma connectique contact porte : fichier detection_etat_porte_3_etats_raspberry.pdf
"""

from ThreadContactPorte import ThreadContactPorte
from CLogger import CLogger

class Supervisor2():
    """ Gère les cpateurs d'un système embarqué : détecteur d'ouverture/fermeture de porte...
    """
   
    def __init__(self, logger):
        """ constructeur
            self.__listeThreadContactPorte : liste d'entiers
               contiendra les numéros de contacts de porte pour les identifier de façon unique
        """
        self.logger = logger
        self.__listeThreadContactPorte = []
      
    def creerThreadContactporte(self, numContact=0, pinInContact=999, pinOutContact=999):
        """ Créer un thread qui gèrera le contact de porte indiqué
            Paramètre :
               numContact : int, numéro du contact de porte à gérer (doit être unique)
        """
        fonction = "Supervisor2.creerThreadContactporte({})".format(numContact)
        try:
            if numContact <= 0 or numContact in self.__listeThreadContactPorte :
                raise ValueError()
            self.__listeThreadContactPorte.append(numContact)
            nomThread = "thContactPorte-{}".format(numContact)
            message = "Thread {}. Lancement -- {}".format(nomThread, fonction)
            self.logger.debug(message)
            thContactPorte = ThreadContactPorte(pinInContact, pinOutContact, nomThread=nomThread, \
                                                logger=self.logger)
            thContactPorte.start()

        except ValueError:
            message = "numContact={}. listeContactExistant={}. Numéro de contact non valide."\
                      " Celui-ci doit être non nul, positif et unique ! -- {}"\
                      .format(numContact, self.__listeThreadContactPorte, fonction)
            self.logger.error(message)
            
# Initialisation du serveur - Mise en place du socket :
if __name__ == "__main__":
    PIN_IN_CONTACT = 17   # entrée numérique permettant de lire l'état du contact de porte
    PIN_OUT_CONTACT = 18   # sortie PWM raspberry (soit GPIO18 : bcm12, soit GPIO13 : bcm33)
    
    # mise un place d'un logger : 1 console et un fichier rotatif
    CLogger.effacerFichierLog("debugSupervisor2.log")
    # ----- Mise en place du logger qui va gérer les handlers console et fichier rotatif
    logger = CLogger(loggerName="loggerSupervisor2", loggerLevel="DEBUG", \
                     consoleLevel="INFO", fileName="debugSupervisor2.log", fileLevel="DEBUG") 
    sup = Supervisor2(logger)
    # crée un thread pour gérer le détecteur d'état de le porte
    sup.creerThreadContactporte(numContact=1, pinInContact=PIN_IN_CONTACT, \
                                pinOutContact=PIN_OUT_CONTACT)
   