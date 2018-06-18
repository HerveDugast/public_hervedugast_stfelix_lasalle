#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : Thread_nbPremier.py      version 1.0
Date : 02-04-2018
Auteur : Hervé Dugast

Fonctionnement
   Lance 2 threads affichant la liste des nombres premiers inférieurs à une certaine valeur, dans 
   l'ordre, au fur et à mesure de son élaboration et à une vitesse différente.

------- affichage console ------------------------------------------------------
*** list-1 ->  Affichage progressif des nombres premiers inférieurs à 20
list-1 -> [2] 
*** list-2 ->  Affichage progressif des nombres premiers inférieurs à 15
list-2 -> [2] 
list-1 -> [2, 3] 
list-1 -> [2, 3, 5] 
list-2 -> [2, 3] 
list-1 -> [2, 3, 5, 7] 
list-1 -> [2, 3, 5, 7, 11] 
list-2 -> [2, 3, 5] 
list-1 -> [2, 3, 5, 7, 11, 13] 
list-1 -> [2, 3, 5, 7, 11, 13, 17] 
list-2 -> [2, 3, 5, 7] 
list-1 -> [2, 3, 5, 7, 11, 13, 17, 19] 
*** list-1 -> Fin Thread
list-2 -> [2, 3, 5, 7, 11] 
list-2 -> [2, 3, 5, 7, 11, 13] 
*** list-2 -> Fin Thread
--- Fin programme ---
--------------------------------------------------------------------------------
"""

from threading import Thread
from time import sleep

class Thread_nbPremier(Thread): 
   
   def __init__(self, nom='', nbMax=20, dureeRech=1): 
      """ constructeur
      """
      Thread.__init__(self) 
      self.__nom = nom 
      self.__nbMax = nbMax
      self.__dureeRech = dureeRech

   def run(self): 
      self.afficherNbPrem()
      
   def isNbPremier(self, n): 
      isPremier = True
      for i in range(2, n):
         if n % i == 0:
            isPremier = False
      return isPremier
   
   def afficherNbPrem(self):
      # self.__nbMax = int(input("Affichez liste nombres premiers inférieur à nbMax. Nb max ? "))
      listNbPrem = []
      print("*** {} ->  Affichage progressif des nombres premiers inférieurs à {}". \
            format(self.__nom, self.__nbMax))
      for n in range(2, self.__nbMax):
         if self.isNbPremier(n):
            listNbPrem.append(n)
            print("{} -> {} ".format(self.__nom, listNbPrem))
            sleep(self.__dureeRech)
      print("*** {} -> Fin Thread".format(self.__nom))
         
if __name__ == "__main__":
   list1 = Thread_nbPremier("list-1", nbMax=20, dureeRech=1)
   list1.start()
   list2 = Thread_nbPremier("list-2", nbMax=15, dureeRech=2.3)
   list2.start()
   list1.join()
   list2.join()
   print("--- Fin programme ---")