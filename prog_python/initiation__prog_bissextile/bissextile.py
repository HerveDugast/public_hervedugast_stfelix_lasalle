#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : bissextile.py       version 1.0
Date : 07-12-2017
Auteur : Hervé Dugast
Source : https://openclassrooms.com/courses/apprenez-a-programmer-en-python

Fonctionnement programme :
  teste si l'année saisie est bissextile

------- affichage console ----------------
mardi 14-11-2017 08:58:14
mardi 14-11-2017 08:58:14
14-11-2017 08:58:14
14-11-2017
08:58:14
Année : 17
------------------------------------------

"""

annee = input("Saisissez une année : ") # saisie de l'année à tester par l'utilisateur
annee = int(annee) # Risque d'erreur si l'utilisateur n'a pas saisi un nombre

if annee % 400 == 0 or (annee % 4 == 0 and annee % 100 != 0):
   print(annee, " est bissextile")
else:
   print(annee, " n'est pas bissextile")