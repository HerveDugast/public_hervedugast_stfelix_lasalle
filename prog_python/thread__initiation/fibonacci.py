#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : fibonacci.py      version 1.0
Date : 02-04-2018
Auteur : Hervé Dugast

Fonctionnement
   Affiche la suite de fibonacci au fur et à mesure de sa construction
   
Source énoncé suite de Fibonacci: Wikipédia
La suite de Fibonacci est une suite d'entiers dans laquelle chaque terme est la somme des deux 
termes qui le précèdent. Elle commence généralement par les termes 0 et 1 (parfois 1 et 1) et 
ses premiers termes sont : 0, 1, 1, 2, 3, 5, 8, 13, 21, etc.

Elle doit son nom à Leonardo Fibonacci qui, dans un problème récréatif posé dans l'ouvrage Liber 
abaci publié en 1202, décrit la croissance d'une population de lapins : « Un homme met un couple de
lapins dans un lieu isolé de tous les côtés par un mur. Combien de couples obtient-on en un an si 
chaque couple engendre tous les mois un nouveau couple à compter du début du troisième mois de son 
existence ? »

------- affichage console ------------------------------------------------------
1 mois : [1] 
2 mois : [1, 1] 
3 mois : [1, 1, 2] 
4 mois : [1, 1, 2, 3] 
5 mois : [1, 1, 2, 3, 5] 
6 mois : [1, 1, 2, 3, 5, 8] 
7 mois : [1, 1, 2, 3, 5, 8, 13] 
8 mois : [1, 1, 2, 3, 5, 8, 13, 21] 
9 mois : [1, 1, 2, 3, 5, 8, 13, 21, 34] 
10 mois : [1, 1, 2, 3, 5, 8, 13, 21, 34, 55] 
11 mois : [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89] 
12 mois : [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144] 
Population au bout de 12 mois : 144 couples de lapins
--------------------------------------------------------------------------------
"""
from time import sleep

def afficherSuite(numMois, popul):
   print("{} mois : {} ".format(numMois, popul))
   sleep(1)

def fibonnaci():
   #nbMois = int(input("Nombre de mois ? "))
   nbMois = 12
   
   # calcul population de lapins
   popul = [1]    # au bout de 1 mois -> 1 couple
   afficherSuite(1, popul)
   popul.append(1)  # au bout de 2 mois -> 1 couple
   afficherSuite(2, popul)
   
   for i in range(2, nbMois):
      # au bout i mois -> popul[i-2]+popul[i-1]
      popul.append(popul[i-2] + popul[i-1])
      afficherSuite(i+1, popul)
   print("Population au bout de {} mois : {} couples de lapins".format(nbMois, popul[nbMois-1]))

if __name__ == "__main__":
   fibonnaci()