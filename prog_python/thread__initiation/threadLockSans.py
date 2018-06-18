#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : threadLockSans.py     version : 1.0
Auteur : H. Dugast
Date : 25-05-2017
Source : https://openclassrooms.com/courses/apprenez-a-programmer-en-python/
   la-programmation-parallele-avec-threading
Matériel utilisé :  ordinateur sous windows (avec wing ide par exemple)
Fonction :
Création de 2 threads. Le premier affiche "canard" et le deuxième "TORTUE".
On n'utilise pas de fonction lock qui permet d'attendre la libération de la ressource (ici la 
console stdout) utilisée par le premier thread pour lancer l'exécution du second thread demandant 
la même ressource. Les lettres des mots "canard" et "TORTUE" sont donc mélangées.

Exemple d'exécution pour ce programme (attention l'ordre n'est pas toujours le même):
--- Console affiche ---
cTOanRaTUrEdcTaOnRTaUrEdTcOanRaTUrEdcTOanRTaUrEdTcaOnRaTUrEd

"""

import sys
from threading import Thread
import time

class Afficheur(Thread):

   """Thread chargé simplement d'afficher un mot dans la console."""

   def __init__(self, mot):
      Thread.__init__(self)
      self.mot = mot

   def run(self):
      """Code à exécuter pendant l'exécution du thread."""
      i = 0
      while i < 5:
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