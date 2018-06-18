#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : threadLockAvec.py     version : 1.0
Auteur : H. Dugast
Date : 25-05-2017
Source : https://openclassrooms.com/courses/apprenez-a-programmer-en-python/
   la-programmation-parallele-avec-threading
Matériel utilisé :  ordinateur sous windows (avec wing ide par exemple)
Fonction :
Création de 2 threads. Le premier affiche "canard" et le deuxième "TORTUE".
On utilise la fonction lock qui permet d'attendre la libération de la ressource (ici la console 
stdout) pour lancer un autre thread qui en a besoin. Lorsque la ressource est libérée, un thread
ayant besoin de la ressource sera lancé (on ne sait pas lequel si plusieurs en ont besoin).
Les mots "canard" et "TORTUE" seront donc entiers.

Exemple d'exécution pour ce programme (attention l'ordre n'est pas toujours le même):
--- Console affiche ---
canardcanardTORTUEcanardcanardcanardTORTUETORTUETORTUETORTUE

"""

import sys
from threading import Thread, RLock
import time

verrou = RLock()

class Afficheur(Thread):

   """Thread chargé simplement d'afficher un mot dans la console."""

   def __init__(self, mot):
      Thread.__init__(self)
      self.mot = mot

   def run(self):
      """Code à exécuter pendant l'exécution du thread."""
      i = 0
      while i < 5:
         with verrou:
            for lettre in self.mot:
               sys.stdout.write(lettre)
               sys.stdout.flush()
               time.sleep(0.1)
            i += 1

# Création des threads
thread_1 = Afficheur("canard")
thread_2 = Afficheur("TORTUE")

# Lancement des threads
thread_1.start()
thread_2.start()

# Attend que les threads se terminent
thread_1.join()
thread_2.join()