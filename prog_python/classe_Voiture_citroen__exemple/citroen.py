#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : citroen.py       version 1.0
Date : 09-02-2018
Auteur : Hervé Dugast
Source : http://deusyss.developpez.com/tutoriels/Python/Pyreverse/

------- affichage console ----------------
Hydractives
Chevrons
------------------------------------------
"""

class Citroen():
   def __init__(self):
      self.type_suspension = "Hydractives"
      self.logo = "Chevrons"
      self.marque = "Citroen"

if __name__ == "__main__":
   ma_citroen = Citroen()
   print(ma_citroen.type_suspension)
   print(ma_citroen.logo)