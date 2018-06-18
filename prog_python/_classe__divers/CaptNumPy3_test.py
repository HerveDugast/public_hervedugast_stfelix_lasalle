#!/usr/bin/python3.4
# coding: utf-8
"""
Classe : CaptNumPy3_test.py     version : 1.0
Auteur : H. Dugast
Date : 10-01-2017
Matériel utilisé : carte raspberry, carte raspiOmix+
Connexion : module grove button -> IO0 raspiomix

Fonction :
    Lit l'état d'un capteur numérique à une entrée (interrupteur, bouton-poussoir...)
    puis l'affiche dans l'interpréteur python
"""

from raspiomix import Raspiomix
from CaptNumPy3 import *

# crée objet bp
BP_PIN = Raspiomix.DIP0
BP_NIV_ACTIF = 1
bp = CaptNumPy3(BP_PIN, BP_NIV_ACTIF)

# ------- programme principal --------------------------------------------------

bpEtatMem = True;

if(bp.isCapteurActif()):
    print("BP actionné")
else:
    print("BP au repos")

while True:
    bpEtatMem = bp.get_niveauActuelCapteur();
    if(bp.isCapteurActif()):
        if(bp.get_niveauActuelCapteur() != bpEtatMem):
            print("BP actionné")
    else:
        if(bp.get_niveauActuelCapteur() != bpEtatMem):
            print("BP au repos")
