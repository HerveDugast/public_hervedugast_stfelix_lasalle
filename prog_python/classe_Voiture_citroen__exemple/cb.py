#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : cb.py       version 1.0
Date : 09-02-2018
Auteur : Hervé Dugast
Source : http://deusyss.developpez.com/tutoriels/Python/Pyreverse/

------- affichage console ----------------
Citizen-Band
------------------------------------------
"""

class CB():
   def __init__(self):
      self.marque = "Citizen-Band"

if __name__ == "__main__":
   ma_cb = CB()
   print(ma_cb.marque)