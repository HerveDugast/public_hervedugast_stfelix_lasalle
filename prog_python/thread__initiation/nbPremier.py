#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : nbPremier.py      version 1.0
Date : 02-04-2018
Auteur : Hervé Dugast

Affiche la liste des nombres premiers inférieurs à une certaine valeur, dans l'ordre, au fur
et à mesure de son élaboration

------- affichage console ------------------------------------------------------
*** Affichage progressif des nombres premiers inférieurs à 20
[2]
[2, 3]
[2, 3, 5]
[2, 3, 5, 7]
[2, 3, 5, 7, 11]
[2, 3, 5, 7, 11, 13]
[2, 3, 5, 7, 11, 13, 17]
[2, 3, 5, 7, 11, 13, 17, 19]
--------------------------------------------------------------------------------
"""
from time import sleep

# recherche si le nombre est premier (recherche non optimisée !)
def isNbPremier(n): 
   isPremier = True
   for i in range(2, n):
      if n % i == 0:
         isPremier = False
   return isPremier

def afficherNbPrem(nbMax=20):
   # nbMax = int(input("Affichez la liste des nombres premiers inférieur à nbMax. Nb max ? "))
   listNbPrem = []
   print("*** Affichage progressif des nombres premiers inférieurs à {}".format(nbMax))
   for n in range(2, nbMax):
      if isNbPremier(n):
         listNbPrem.append(n)
         print(listNbPrem) 
         sleep(1)
   
if __name__ == "__main__":   
   afficherNbPrem()   