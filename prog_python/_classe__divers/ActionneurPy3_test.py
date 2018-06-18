#!/usr/bin/python3.4
# coding: utf-8
"""
Classe : ActionneurPy3_test.py     version : 1.0
Auteur : H. Dugast
Date : 09-01-2017
Matériel utilisé : carte raspberry avec éventuellement carte raspiOmix+

Fonction : fait clignoter une led, 1 clignotement par seconde
Instructions non bloquantes
"""

import time
from raspiomix import Raspiomix
from ActionneurPy3 import *

# crée objet led4
LED_PIN = Raspiomix.IO0
LED_NIV_ACTIF = 1
led = ActionneurPy3(LED_PIN, LED_NIV_ACTIF)

# définit le temps d'allumage et d'extinction de la LED en milllisecondes
led.chronoDefinirDureeEtatEnMs(500)
led.chronoMemoriserDepart()     # mémorise instant du début allumage
led.activer()  # allume la LED

while True:
    if led.chronoIsFinDuree():
        led.chronoMemoriserDepart()
        led.changerEtat()
