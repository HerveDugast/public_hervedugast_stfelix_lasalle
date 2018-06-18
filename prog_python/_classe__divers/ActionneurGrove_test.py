#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""
Classe : ActionneurGrove_test.py     version : 1.1
Auteur : H. Dugast
Date : 04-12-2015
Matériel utilisé : carte raspberry avec carte grovePi

Fonction :  active, stoppe, change d'état un actionneur (LED, relais...)
            connecté à un port de la carte grovePi
"""

import time
import grovepi
from ActionneurGrove import *

# crée objet led4
LED_PIN = 4
LED_NIV_ACTIF = 1
led4 = ActionneurGrove(LED_PIN, LED_NIV_ACTIF)

# ------- programme principal --------------------------------------------------

# définit le temps d'allumage et d'extinction de la LED en milllisecondes
led4.chronoDefinirDureeEtatEnMs(250)
led4.chronoMemoriserDepart()     # mémorise instant du début allumage
led4.activer()  # allume la LED

while True:
    if led4.chronoIsFinDuree():
        led4.chronoMemoriserDepart()
        led4.changerEtat()
