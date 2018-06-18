#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""
Classe : CaptNumGrove.py     version : 1.1
Auteur : H. Dugast
Date : 05-12-2015
Matériel utilisé : carte raspberry avec carte grovePi
"""
import time
import grovepi

class CaptNumGrove:
    """
    Classe permettant de lire l'état logique envoyé par un capteur numérique
    (bouton-poussoir, interrupteur...) connecté à un port de la carte grovePi
    """

    s_ACTIF = 1 # actionneur actif (ACTIF = 1), indépendant du niveau actif
    
    def __init__(self, pinCapteur = 0xFF, niveauActif = 1):
        """
        Initialisateur, prépare un objet actionneur à une entrée, définit
        broche de connexion, met le capteur à l'état repos (inactif)
        
        m_pinCapteur : numéro broche à laquelle est connecté le capteur
        m_niveauActif : niveau logique envoyé par le capteur lorsqu'il est actif
        m_isActionneurActif : 1 -> actionneur actif, 0 -> actionneur inactif
        m_niveauActuel : niveau logique retourné par le capteur
        ??? BUG ??? parfois, la lecture de l'entrée du capteur retourne 255 !!!
            au lieu de retourner un booléen
        m_niveauPrecedent : mémorise état précédent du capteur et corrige bug
        """
        self.m_pinCapteur = pinCapteur
        self.m_niveauActif = niveauActif
        # configure ligne en entrée
        grovepi.pinMode(self.m_pinCapteur ,"INPUT") 
        # initialise les attributs du capteur
        self.m_niveauPrecedent = not self.m_niveauActif

        # niveau logique envoyé par capteur (0 ou 1)
        # ??? BUG ??? parfois, la lecture de l'entrée du capteur retourne 255 !!!
        #     au lieu de retourner un booléen
        # utilisation m_niveauPrecedent pour corriger ce bug
        self.m_niveauActuel = grovepi.digitalRead(self.m_pinCapteur)
        if (self.m_niveauActuel != 0 and self.m_niveauActuel != 1):
            self.m_niveauActuel = self.m_niveauPrecedent
        if(self.m_niveauActuel == self.m_niveauActif):
            self.m_isActionneurActif = True     # capteur actif
        else:
            self.m_isActionneurActif = False    # capteur au repos


    def lire(self):
        """
        Lit l'état logique actuel du capteur et met à jour les attributs de
        l'objet
        """
        # niveau logique envoyé par capteur (0 ou 1)
        # ??? BUG ??? parfois, la lecture de l'entrée du capteur retourne 255 !!!
        # utilisation m_niveauPrecedent pour corriger ce bug
        self.m_niveauPrecedent = self.m_niveauActuel
        self.m_niveauActuel = grovepi.digitalRead(self.m_pinCapteur)
        if (self.m_niveauActuel != 0 and self.m_niveauActuel != 1):
            self.m_niveauActuel = self.m_niveauPrecedent
        if(self.m_niveauActuel == self.m_niveauActif):
            self.m_isActionneurActif = True     # capteur actif
        else:
            self.m_isActionneurActif = False    # capteur au repos
        return self.m_isActionneurActif;

    def isCapteurActif(self):
        """
        Lit l'état de l'entrée du capteur puis signale s'il est actif ou non
        """
        self.lire()
        if(self.m_isActionneurActif):
            return True
        else:
            return False

    def get_niveauActuelCapteur(self):
        """
        Retourne l'état logique de la dernière lecture de l'entrée du capteur
        """
        return self.m_niveauActuel
        
    def debugAttribut(self):
        """
        Affiche dans un terminal les valeurs de tous les attributs de l'objet
        """
        print("")
        print("---- Début objet ----")
        print("m_pinCapteur : "),
        print(self.m_pinCapteur)
        print("m_niveauActif : "),
        print(self.m_niveauActif)
        print("m_isActionneurActif : "),
        print(self.m_isActionneurActif)
        print("m_niveauActuel : "),
        print(self.m_niveauActuel)
        print("")
        print("---- Fin objet ----")

