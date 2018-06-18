#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : bissextile_v22.py       version 2.2
Date : 14-12-2017
Auteur : Hervé Dugast

Fonctionnement programme :
  Vérifie la validité de l'année saisie et affiche si l'année est bissextile ou non

------- affichage console (en cas d'erreur "raise") ------------------------
Saisissez une année : -100
Erreur :  
Année saisie non valide ou négative !
------------------------------------------------------------------------
"""

annee = input("Saisissez une année : ") # saisie de l'année à tester par l'utilisateur
try: # On essaye de convertir l'année saisie en entier
   annee = int(annee)
   # si l'année saisie est valide, les instructions suivantes sont exécutées
   # sinon ce sera le bloc except qui sera exécuté
   # si l'année est négative, on va lever une exception et interrompre le programme proprement
   if annee < 0:
      raise ValueError   
   if annee % 400 == 0 or (annee % 4 == 0 and annee % 100 != 0):
      print(annee, " est bissextile")
   else:
      print(annee, " n'est pas bissextile")   
except ValueError as err:
   print("Erreur : ", str(err))
   print("Année saisie non valide ou négative !")