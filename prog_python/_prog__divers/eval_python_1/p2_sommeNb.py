#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : p2_sommeNb.py       version 1.0
Date : 16-01-2018
Auteur : Hervé Dugast
 
Fonctionnement programme :
  Affiche la somme d'une liste de nombres donnés
  
------- affichage console ---------------------
Liste nombres : (2, 50, 17, 14, 98, 15, 3, 24)
Somme = 223
-----------------------------------------------
"""
listeNb = (2, 50, 17, 14, 98, 15, 3, 24)

somme = 0
for nb in listeNb:
    somme += nb
print("Liste nombres : {}".format(listeNb))
print("Somme = {}".format(somme))
