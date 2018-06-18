#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : Supervisor2.py      version 1.0
Date : 30-05-2018
Auteur : Hervé Dugast

------ Affichage console --------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------

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
      
    def creerThreadContactporte(self, numContact=0):
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
            thContactPorte = ThreadContactPorte(nomThread=nomThread, logger=self.logger)
            thContactPorte.start()

        except ValueError:
            message = "numContact={}. listeContactExistant={}. Numéro de contact non valide."\
                      " Celui-ci doit être non nul, positif et unique ! -- {}"\
                      .format(numContact, self.__listeThreadContactPorte, fonction)
            self.logger.error(message)
            
# Initialisation du serveur - Mise en place du socket :
if __name__ == "__main__":
    # mise un place d'un logger : 1 console et un fichier rotatif
    CLogger.effacerFichierLog("debugSupervisor2.log")
    # ----- Mise en place du logger qui va gérer les handlers console et fichier rotatif
    logger = CLogger(loggerName="loggerSupervisor2", loggerLevel="DEBUG", \
                     consoleLevel="INFO", fileName="debugSupervisor2.log", fileLevel="DEBUG") 
    sup = Supervisor2(logger)
    sup.creerThreadContactporte(1)
   