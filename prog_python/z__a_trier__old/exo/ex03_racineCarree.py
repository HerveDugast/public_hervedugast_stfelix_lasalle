#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : ex03_racineCarree.py     version : 1.0
Auteur : H. Dugast
Source : http://hebergement.u-psud.fr/iut-orsay/Pedagogie/MPHY/Python/exercices-python3.pdf
Date : 06-05-2017

Fonction :
Saisissez un flottant. S’il est positif ou nul, affichez sa racine, sinon affichez un message
d’erreur.

Exemple d'exécution :
x ? 10
La racine de 10.00 est 3.162
x ? -1
Erreur ! x doit etre positif ou nul !
"""
from math import sqrt

x = float(input("x ? "))
if x >= 0:
   y = sqrt(x)
   print("La racine de {:.2f} est {:.3f}".format(x, y))
else:
   print("Erreur ! x doit etre positif ou nul !")
