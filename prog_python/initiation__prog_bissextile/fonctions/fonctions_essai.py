#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : fonctions_essai.py       version 1.4
Date : 07-12-2017
Auteur : Hervé Dugast
Source : https://openclassrooms.com/courses/apprenez-a-programmer-en-python

Fonctionnement programme :
  Module permettant d'essayer des fonctions arithmétiques contenues dans le module fonctions.py

------- affichage console ----------------
Table de multiplication de  3
1  *  3  =  3
2  *  3  =  6
...
7  *  3  =  21
Table d'addition de  3
0  +  3  =  3
1  +  3  =  4
...
7  +  3  =  10
Soustraction entre 2 nombres
2  -  12  =  -10
------------------------------------------
"""
# Ajout des chemins d'accès aux bibliothèques et modules dans le python PATH
# donc ajout du dossier parent contenant les dossiers projets, library et test_unitaire
dossier_parent = "python"  # A ADAPTER ! mettre le nom du dossier contenant votre projet
import sys
import os
chemin = os.path.dirname(os.path.abspath(__file__))
while not chemin.endswith(dossier_parent):
   chemin = os.path.dirname(chemin)
if chemin not in sys.path:
   sys.path.insert(0, chemin)
print(sys.path)

from library.divers_perso.fonctions import *  

# Essai de la fonction table
tableMultiplication(3, 7)
tableAddition(3, 7)
soustraction(2, 12)
division(10, 3)
division(10, 0)
division('Canard', 'Deux')
