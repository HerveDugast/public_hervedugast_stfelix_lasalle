#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : bissextile_v2.py       version 2.1
Date : 14-12-2017
Auteur : Hervé Dugast

Fonctionnement programme :
  Vérifie la validité de l'année saisie et affiche si l'année est bissextile ou non

------- affichage console (en cas d'erreur) ------------------------
Saisissez une année : bonjour
Erreur :  invalid literal for int() with base 10: 'qsrf'
Année saisie non valide !
------------------------------------------------------------------------
"""

annee = input("Saisissez une année : ") # saisie de l'année à tester par l'utilisateur
try: # On essaye de convertir l'année saisie en entier
   annee = int(annee)
   # si l'année saisie est valide, les instructions suivantes sont exécutées
   # sinon ce sera le bloc except qui sera exécuté
   if annee % 400 == 0 or (annee % 4 == 0 and annee % 100 != 0):
      print(annee, " est bissextile")
   else:
      print(annee, " n'est pas bissextile")   
except ValueError as err:
   print("Erreur : ", str(err))
   print("Année saisie non valide !")

