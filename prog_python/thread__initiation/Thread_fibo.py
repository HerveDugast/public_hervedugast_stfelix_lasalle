#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : Thread_fibo.py      version 1.0
Date : 02-04-2018
Auteur : Hervé Dugast

Fonctionnement
   Affiche la suite de fibonacci au fur et à mesure de sa construction. On utilise 2 threads qui
   vont compter la population de lapins à 2 vitesses différentes (on imagine que le comptage de 
   la population 2 est plus compliqué et dure donc plus longtemps).
   
Source énoncé : Wikipédia
La suite de Fibonacci est une suite d'entiers dans laquelle chaque terme est la somme des deux 
termes qui le précèdent. Elle commence généralement par les termes 0 et 1 (parfois 1 et 1) et 
ses premiers termes sont : 0, 1, 1, 2, 3, 5, 8, 13, 21, etc.

Elle doit son nom à Leonardo Fibonacci qui, dans un problème récréatif posé dans l'ouvrage Liber 
abaci publié en 1202, décrit la croissance d'une population de lapins : « Un homme met un couple de
lapins dans un lieu isolé de tous les côtés par un mur. Combien de couples obtient-on en un an si 
chaque couple engendre tous les mois un nouveau couple à compter du début du troisième mois de son 
existence ? »

------- affichage console ------------------------------------------------------
*** popul-1 ->  Affichage évolution population de couples de lapins sur 6 mois
popul-1 -> 1 mois : [1] 
*** popul-2 ->  Affichage évolution population de couples de lapins sur 5 mois
popul-2 -> 1 mois : [1] 
popul-1 -> 2 mois : [1, 1] 
popul-1 -> 3 mois : [1, 1, 2] 
popul-2 -> 2 mois : [1, 1] 
popul-1 -> 4 mois : [1, 1, 2, 3] 
popul-1 -> 5 mois : [1, 1, 2, 3, 5] 
popul-2 -> 3 mois : [1, 1, 2] 
popul-1 -> 6 mois : [1, 1, 2, 3, 5, 8] 
popul-1 -> Population au bout de 6 mois : 8 couples de lapins
*** popul-1 -> Fin Thread
popul-2 -> 4 mois : [1, 1, 2, 3] 
popul-2 -> 5 mois : [1, 1, 2, 3, 5] 
popul-2 -> Population au bout de 5 mois : 5 couples de lapins
*** popul-2 -> Fin Thread
--- Fin programme ---
--------------------------------------------------------------------------------
"""

from threading import Thread
from time import sleep

class Thread_fibo(Thread): 
   
   def __init__(self, nom='', dureeCompt=1, dureeCalculEnMois=12): 
      """ constructeur
      """
      Thread.__init__(self) 
      self.__nom = nom 
      self.__dureeMois = dureeCompt
      self.__dureeCalculEnMois = dureeCalculEnMois

   def run(self): 
      self.fibonnaci()
      
   def afficherSuite(self, numMois, popul):
      print("{} -> {} mois : {} ".format(self.__nom, numMois, popul))
      sleep(self.__dureeMois)
   
   def fibonnaci(self):
      # calcul population de lapins
      print("*** {} ->  Affichage évolution population de couples de lapins sur {} mois" \
            .format(self.__nom, self.__dureeCalculEnMois))
      popul = [1]    # au bout de 1 mois -> 1 couple
      self.afficherSuite(1, popul)
      popul.append(1)  # au bout de 2 mois -> 1 couple
      self.afficherSuite(2, popul)
      
      for i in range(2, self.__dureeCalculEnMois):
         # au bout i mois -> popul[i-2]+popul[i-1]
         popul.append(popul[i-2] + popul[i-1])
         self.afficherSuite(i+1, popul)
      print("{} -> Population au bout de {} mois : {} couples de lapins". \
            format(self.__nom, self.__dureeCalculEnMois, popul[self.__dureeCalculEnMois-1]))
      print("*** {} -> Fin Thread".format(self.__nom))
         
if __name__ == "__main__":
   popul1 = Thread_fibo("popul-1", dureeCompt=1, dureeCalculEnMois=6)
   popul1.start()
   popul2 = Thread_fibo("popul-2", dureeCompt=2.3, dureeCalculEnMois=5)
   popul2.start()
   popul1.join()
   popul2.join()
   print("--- Fin programme ---")