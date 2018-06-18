#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : Thread_gestion_fibo_nbPrem.py      version 1.0
Date : 02-04-2018
Auteur : Hervé Dugast

Fonctionnement
   Affiche la suite de fibonacci au fur et à mesure de sa construction. On utilise 2 threads qui
   vont compter la population de lapins à 2 vitesses différentes (on imagine que le comptage de 
   la population 2 est plus compliqué et dure donc plus longtemps).
   Lance 2 threads affichant la liste des nombres premiers inférieurs à une certaine valeur, dans 
   l'ordre, au fur et à mesure de son élaboration et à une vitesse différente.
   
------- affichage console ------------------------------------------------------
----- Lancement Thread_fibo n°1 -----
*** popul-1 ->  Affichage évolution population de couples de lapins sur 6 mois
popul-1 -> 1 mois : [1] 
----- Lancement Thread_fibo n°2 -----
*** popul-2 ->  Affichage évolution population de couples de lapins sur 5 mois
popul-2 -> 1 mois : [1] 
----- Lancement Thread_nbPremier n°1 -----
*** list-1 ->  Affichage progressif des nombres premiers inférieurs à 20
list-1 -> [2] 
----- Lancement Thread_nbPremier n°2 -----
*** list-2 ->  Affichage progressif des nombres premiers inférieurs à 15
list-2 -> [2] 

--- FIN PROGRAMME PRINCIPAL, mais pas des threads... ---

popul-1 -> 2 mois : [1, 1] 
list-1 -> [2, 3] 
popul-1 -> 3 mois : [1, 1, 2] 
list-1 -> [2, 3, 5] 
list-2 -> [2, 3] 
popul-2 -> 2 mois : [1, 1] 
list-1 -> [2, 3, 5, 7] 
popul-1 -> 4 mois : [1, 1, 2, 3] 
list-1 -> [2, 3, 5, 7, 11] 
popul-1 -> 5 mois : [1, 1, 2, 3, 5] 
list-2 -> [2, 3, 5] 
popul-2 -> 3 mois : [1, 1, 2] 
list-1 -> [2, 3, 5, 7, 11, 13] 
popul-1 -> 6 mois : [1, 1, 2, 3, 5, 8] 
list-1 -> [2, 3, 5, 7, 11, 13, 17] 
popul-1 -> Population au bout de 6 mois : 8 couples de lapins
*** popul-1 -> Fin Thread
list-2 -> [2, 3, 5, 7] 
popul-2 -> 4 mois : [1, 1, 2, 3] 
list-1 -> [2, 3, 5, 7, 11, 13, 17, 19] 
*** list-1 -> Fin Thread
list-2 -> [2, 3, 5, 7, 11] 
popul-2 -> 5 mois : [1, 1, 2, 3, 5] 
list-2 -> [2, 3, 5, 7, 11, 13] 
popul-2 -> Population au bout de 5 mois : 5 couples de lapins
*** popul-2 -> Fin Thread
*** list-2 -> Fin Thread
--------------------------------------------------------------------------------
"""

from Thread_fibo import Thread_fibo
from Thread_nbPremier import Thread_nbPremier

class Thread_gestion_fibo_nbPrem(): 
   
   __numThreadFibo = 0
   __numThreadNbPrem = 0
   
   def __init__(self): 
      """ constructeur
      """
      pass

   def creerFibonnaci(self, nom='', dureeMois=1, dureeCalculEnMois=12):
      """ Lance dans un thread l'affichage de l'évolution d'une population de lapin
      """
      Thread_gestion_fibo_nbPrem.__numThreadFibo += 1
      numThread = Thread_gestion_fibo_nbPrem.__numThreadFibo
      print("----- Lancement Thread_fibo n°{} -----".format(numThread))
      popul = Thread_fibo("popul-{}".format(numThread), dureeMois, dureeCalculEnMois)
      popul.start()
      
   def creerAffichNbPremier(self, nbMax=20, dureeRech=1):
      """ Lance dans un thread l'affichage de l'évolution de la recherche des nombres premiers
      """
      __class__.__numThreadNbPrem += 1
      numThread = __class__.__numThreadNbPrem
      print("----- Lancement Thread_nbPremier n°{} -----".format(numThread))
      listeNb = Thread_nbPremier("list-{}".format(numThread), nbMax, dureeRech)
      listeNb.start()
      
if __name__ == "__main__":
   fibNb = Thread_gestion_fibo_nbPrem()
   fibNb.creerFibonnaci(dureeMois=1, dureeCalculEnMois=6)
   fibNb.creerFibonnaci(dureeMois=2.3, dureeCalculEnMois=5)

   fibNb.creerAffichNbPremier(nbMax=20, dureeRech=1)
   fibNb.creerAffichNbPremier(nbMax=15, dureeRech=2.1)
   print("\n--- FIN PROGRAMME PRINCIPAL, mais pas des threads... ---\n")