#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : ex05_volumeSphere.py     version : 1.0
Auteur : H. Dugast
Source : http://hebergement.u-psud.fr/iut-orsay/Pedagogie/MPHY/Python/exercices-python3.pdf
Date : 06-05-2017

Fonction :
Écrire une fonction volumeSphere qui calcule le volume d’une sphère de rayon r fourni en argument
et qui utilise la fonction cube.
Tester la fonction volumeSphere par un appel dans le programme principal.

Exemple d'exécution pour un rayon de 3 cm :
Rayon (cm) : 3
Volume de la sphere de rayon 3.0 cm : 113.097 cm3
"""
from math import pi

# fonctions
def cube(x):
   """Calcule le cube de l'argument."""
   return x**3

def volumeSphere(r):
   """Calcule le volume d'une sphere de rayon <r>."""
   return 4 * pi * cube(r) / 3

# programme principal -----------------------------------------------
rayon = float(input("Rayon (cm) : "))
print("Volume de la sphere de rayon {:.1f} cm : {:.3f} cm3".format(rayon, volumeSphere(rayon)))