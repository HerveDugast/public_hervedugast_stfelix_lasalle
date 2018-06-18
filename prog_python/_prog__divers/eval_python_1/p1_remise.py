#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : p1_remise.py       version 1.0
Date : 16-01-2018
Auteur : Hervé Dugast
 
Fonctionnement programme :
  Calcul du prix à payer avec remise
  
------- affichage console ----------------
Prix article ? 100
Montant remise en % ? 30
Prix à payer : 70.00
------------------------------------------
"""

prixArticle = float(input("Prix article ? "))
remise = float(input("Montant remise en % ? "))
prixAPayer = prixArticle - prixArticle * (remise / 100)
print("Prix à payer : {:.2f}\n".format(prixAPayer))
