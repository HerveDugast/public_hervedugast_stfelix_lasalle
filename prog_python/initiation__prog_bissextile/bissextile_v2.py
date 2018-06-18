#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : bissextile_v2.py       version 2.1
Date : 14-12-2017
Auteur : Hervé Dugast

Fonctionnement programme :
  Vérifie la validité de l'année saisie et affiche si l'année est bissextile ou non

------- affichage console ----------       ------- affichage console ----------
Saisissez une année : bonjour              Saisissez une année :2017
Erreur : année saisie non valide !         2017  n'est pas bissextile
------------------------------------       ------------------------------------
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
except:
   print("Erreur : année saisie non valide !")

