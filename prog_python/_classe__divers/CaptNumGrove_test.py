#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""
Classe : CaptNumGrove_test.py     version : 1.2
Auteur : H. Dugast
Date : 05-12-2015
Matériel utilisé : carte raspberry avec carte grovePi, module grove button
Connexion : module button -> D3 de grovePi

Fonction :
    Lit l'état d'un capteur numérique à une entrée (interrupteur, bouton-poussoir...)
    puis l'affiche dans l'interpréteur python
"""

import time
import grovepi
from CaptNumGrove import *

# crée objet bp3
BP_PIN = 3
BP_NIV_ACTIF = 1
bp4 = CaptNumGrove(BP_PIN, BP_NIV_ACTIF)

# ------- programme principal --------------------------------------------------

bpEtatMem = True;

if(bp4.isCapteurActif()):
    print("BP actionné")
else:
    print("BP au repos")

while True:
    bpEtatMem = bp4.get_niveauActuelCapteur();
    if(bp4.isCapteurActif()):
        if(bp4.get_niveauActuelCapteur() != bpEtatMem):
            print("BP actionné")
    else:
        if(bp4.get_niveauActuelCapteur() != bpEtatMem):
            print("BP au repos")
    
