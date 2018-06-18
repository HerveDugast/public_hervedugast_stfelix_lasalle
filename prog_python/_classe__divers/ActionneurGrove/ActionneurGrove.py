#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""
Classe : ActionneurGrove.py     version : 1.1
Auteur : H. Dugast
Date : 04-12-2015
Matériel utilisé : carte raspberry avec carte grovePi
"""
# import time
import grovepi
from datetime import datetime

class ActionneurGrove:
    """
    Classe permettant d'activer, désactiver, faire changer d'état un actionneur
    (LED, relais...) connecté à un port de la carte grovePi
    Elle contient aussi une série de méthode permet de gérer la durée
    d'activation ou de repos de l'actionneur sans bloquer le programme.
    Pour cela, la bibliothèque time est utilisée.
    On mémorise l'instant de départ d'un état (actif ou inactif), puis à
    intervalle régulier, on soustrait l'instant présent à l'instant de
    départ pour calculer la durée écoulée.
    """

    s_ACTIF = 1 # actionneur actif (ACTIF = 1), indépendant du niveau actif
    
    def __init__(self, pinActionneur = 0xFF, niveauActif = 1):
        """
        Initialisateur, prépare un objet actionneur à une entrée, définit
        broche de connexion, met l'actionneur à l'état repos (inactif)
        
        m_pinActionneur : numéro broche à laquelle est connecté l'actionneur
        m_niveauActif : niveau logique (0 ou 1) qui rend actif l'actionneur
        m_isActionneurActif : 1 -> actionneur actif, 0 -> actionneur inactif
        m_niveauActuel : niveau logique présent à l'entrée de l'actionneur

        m_dureeEtatValeurEnMs : durée état actif (ou inactif) souhaitée en ms
        m_timeDepart : instant mémorisé correspondant au départ de la durée où
            l'actionneur doit garder le même état. Nombre à virgule exprimé en secondes
        m_timeNow : instant présent mémorisé. Nombre à virgule exprimé en
            secondes
        m_timeEcart : écart en millisecondes entre l'instant de la mesure et l'instant
            précédemment mesuré
        m_chronoDureeEcoulee : durée écoulée en ms depuis l'instant de départ
            mémorisée par la méthode chronoMemoriserDepart()
        m_chronoEcartFin : écart entre durée prévue et durée écoulée en ms
            nombre entier signé
        """
        self.m_pinActionneur = pinActionneur
        self.m_niveauActif = niveauActif
        # configure ligne en sortie
        grovepi.pinMode(self.m_pinActionneur ,"OUTPUT") 
        # désactive l'actionneur
        grovepi.digitalWrite(self.m_pinActionneur, not self.m_niveauActif)
        self.m_isActionneurActif = 0     # Actionneur désactivé
        self.m_niveauActuel = not self.m_niveauActif

        # initialisation des autres attributs
        self.m_dureeEtatValeurEnMs = 0
        self.m_timeDepart = 0
        self.m_timeNow = 0
        self.m_timeEcart = 0
        self.m_chronoDureeEcoulee = 0
        self.m_chronoEcartFin = 0

    
    def activer(self):
        """
        Active l'actionneur en envoyant à son entrée le niveau adéquat.
        Les attributs m_isActionneurActif et m_niveauActuel sont mis à jour
        """
        grovepi.digitalWrite(self.m_pinActionneur, self.m_niveauActif)
        self.m_isActionneurActif = self.s_ACTIF         # Actionneur activé
        self.m_niveauActuel = self.m_niveauActif
        
    def desactiver(self):
        """
        Désactive l'actionneur en envoyant à son entrée le niveau adéquat.
        Les attributs m_isActionneurActif et m_niveauActuel sont mis à jour
        """
        grovepi.digitalWrite(self.m_pinActionneur, not self.m_niveauActif)
        self.m_isActionneurActif = not self.s_ACTIF     # Actionneur désactivé
        self.m_niveauActuel = not self.m_niveauActif

    def changerEtat(self):
        """
        Change d'état l'actionneur, fonction basculement (toggle).
        Lit l'état logique présent à l'entrée de l'actionneur puis envoie
        l'état logique opposé pour faire changer d'état l'actionneur.
        Les attributs m_isActionneurActif et m_niveauActuel sont mis à jour
        """
        self.m_niveauActuel = not grovepi.digitalRead(self.m_pinActionneur)
        grovepi.digitalWrite(self.m_pinActionneur, self.m_niveauActuel)
        if self.m_niveauActuel == self.s_ACTIF:
            self.m_isActionneurActif = self.s_ACTIF     # Actionneur activé
        else:
            self.m_isActionneurActif = not self.s_ACTIF # Actionneur désactivé

    def chronoDefinirDureeEtatEnMs(self, dureeEtat):
        """
        Définit la durée en millisecondes durant laquelle l'actionneur doit
        rester dans le même état.
        m_dureeEtatValeurEnMs : durée état actif (ou inactif) souhaitée en ms
        """
        self.m_dureeEtatValeurEnMs = dureeEtat

    def chronoMemoriserDepart(self):
        """
        Mémorise l'instant de départ de la durée durant laquelle l'actionneur
        doit rester dans le même état. Permet d'avoir une précision autour
        de la milliseconde.
        m_timeDepart :
            instant mémorisé correspondant au départ de la durée où l'actionneur
            doit garder le même état. Nombre à virgule exprimé en secondes
        """
        self.m_timeDepart = datetime.now()
        self.m_chronoDureeEcoulee = 0
        self.m_chronoEcartFin = 0 - self.m_dureeEtatValeurEnMs

    def chronoCalculerDureeEcoulee(self):
        """
        Calcule durée écoulée en millisecondes depuis l'instant de départ.
        mémorisé par la méthode chronoMemoriserDepart(), attribut m_timeDepart.
        Retour : écart entre ces 2 instants en millisecondes
        
        m_timeDepart :
            instant mémorisé correspondant au départ de la durée où l'actionneur
            doit garder le même état. Nombre à virgule exprimé en secondes
        m_timeNow :
            instant présent mémorisé. Nombre à virgule exprimé en secondes

        m_timeEcart : écart en millisecondes entre l'instant de la mesure et l'instant
            précédemment mesuré
            
        Retour :
            m_chronoDureeEcoulee : durée écoulée en ms depuis l'instant de départ
                mémorisée par la méthode chronoMemoriserDepart()
                m_chronoDureeEcoulee = m_timeNow - m_timeDepart en ms
    """
        self.m_timeNow = datetime.now()
        self.m_timeEcart = self.m_timeNow - self.m_timeDepart
        self.m_chronoDureeEcoulee = round((self.m_timeEcart.total_seconds())*1000)
        return self.m_chronoDureeEcoulee

    def chronoCalculerEcartFinDuree(self):
        """
        Retourne l'écart en millisecondes qui existe entre la durée prévue
        (où l'actionneur doit rester dans le même état) et la durée écoulée
        à cet instant.

        m_dureeEtatValeurEnMs : durée état actif (ou inactif) souhaitée en ms
        m_chronoDureeEcoulee : durée écoulée en ms depuis l'instant de départ
            mémorisée par la méthode chronoMemoriserDepart()

        Retour :
            m_chronoEcartFin : écart entre durée prévue et durée écoulée en ms
                              nombre entier signé
                              si nb >= 0 -> durée prévue atteinte ou dépassée
                              si nb < 0  -> durée prévue non atteinte
        """
        self.chronoCalculerDureeEcoulee()
        self.m_chronoEcartFin = self.m_chronoDureeEcoulee - self.m_dureeEtatValeurEnMs
        return self.m_chronoEcartFin
    
    def chronoIsFinDuree(self):
        """
        Signale si la durée est écoulée, celle où où l'actionneur doit rester
        dans le même état. L'attribut m_chronoEcartFin est mis à jour.
        
        m_chronoEcartFin : écart entre durée prévue et durée écoulée en ms
                          nombre entier signé
        Retour :
            True -> durée écoulée atteinte ou dépassée
            False -> durée écoulée non atteinte
            
        """
        if self.chronoCalculerEcartFinDuree() >= 0:
            return True
        else:
            return False

    def debugAttribut(self):
        """
        Affiche dans un terminal les valeurs de tous les attributs de l'objet
        """
        print("")
        print("---- Début objet ----")
        print("m_pinActionneur : "),
        print(self.m_pinActionneur)
        print("m_niveauActif : "),
        print(self.m_niveauActif)
        print("m_isActionneurActif : "),
        print(self.m_isActionneurActif)
        print("m_niveauActuel : "),
        print(self.m_niveauActuel)
        print("")
        print("m_dureeEtatValeurEnMs : "),
        print(self.m_dureeEtatValeurEnMs)
        print("m_timeDepart : "),
        print(self.m_timeDepart)
        print("m_timeNow : "),
        print(self.m_timeNow)
        print("m_chronoDureeEcoulee : "),
        print(self.m_chronoDureeEcoulee)
        print("m_chronoEcartFin : "),
        print(self.m_chronoEcartFin)
        print("---- Fin objet ----")

