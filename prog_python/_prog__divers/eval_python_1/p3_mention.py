#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : p3_mention.py       version 1.1
Date : 17-01-2018
Auteur : Hervé Dugast
 
Fonctionnement programme :
  Affiche la mention obtenu à un examen
  
------- affichage console --------------------------
Saisir une note ? 2
Non admis
Saisir une note ? 10
Passable
Saisir une note ? 12.5
Assez bien
Saisir une note ? 14
Bien
Saisir une note ? 18
Très bien
Saisir une note ? 21
Saisissez une note comprise entre 0 et 20 svp !
Saisir une note ? -1
Fin programme
----------------------------------------------------
"""
note = 1
while note >= 0:
   note = float(input("Saisir une note ? "))
   if note >= 0:
      if note < 10:
         print("Non admis")
      elif note < 12:
         print("Passable")
      elif note < 14:
         print("Assez bien")
      elif note < 16:
         print("Bien")
      elif note <= 20:
         print("Très bien")
      else:
         print("Saisissez une note comprise entre 0 et 20 svp !")
print("Fin programme")