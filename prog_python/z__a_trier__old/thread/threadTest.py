#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : threadTest.py     version : 1.0
Auteur : H. Dugast
Date : 25-05-2017
Source : https://python.developpez.com/faq/?page=Thread
Matériel utilisé :  ordinateur sous windows (avec wing ide par exemple)
Fonction :
Création de 2 threads. Chacun affiche un compteur de 0 à 5.
Utilisation de la méthode join qui permet de stopper le programme principal tant que le thread
ou le timeout n'est pas terminé. La méthode join ne stoppe pas les threads.

Rappel : il est fortement déconseillé de stopper un thread de manière brutale car l'exécution
d'un thread utilise souvent d'autres threads en python. L'arrêt brutal du thread "utilisateur" ne 
garantit que l'arrêt du processus du thread "utilisateur", pas des autres utiles à ce dernier.

Exemple d'exécution pour ce programme (attention l'ordre n'est pas toujours le même):
--- Console affiche ---
*** Début Thread a
thread a 0
*** Début Thread b
thread b 0
thread a 1
thread b 1
thread a 2
thread b 2
thread a 3
thread b 3
*** Fin blocage programme principal par le thread a
Bonjour, je suis le programme principal !!!
thread a 4
thread b 4
thread a 5
thread b 5
thread a 6
*** Fin blocage programme principal par le thread b
Fin programme

"""

import threading 
import time

def affiche(nb, nom = ''): 
   for i in range(nb): 
      print(nom, i)
      time.sleep(1)

# constructeur threading.Thread( group=None, target=None, name=None, args=(), kwargs={}) où :
# group doit rester à None, en attendant que la classe ThreadGroup soit implantée.
# target est la fonction appelée par le Thread.
# name est le nom du Thread, construit par défaut sous la forme "Thread-N" avec N le numéro.
# args est un tuple d'arguments pour l'invocation de la fonction target
# kwargs est un dictionnaire d'arguments pour l'invocation de la fonction target
a = threading.Thread(None, affiche, None, (6666,), {'nom':'thread a'}) 
b = threading.Thread(None, affiche, None, (6,), {'nom':'thread b'}) 
print("*** Début Thread a")
a.start() 
print("*** Début Thread b")
b.start()
a.join(timeout=3)
print("*** Fin blocage programme principal par le thread a")
print("Bonjour, je suis le programme principal !!!")
b.join()
print("*** Fin blocage programme principal par le thread b")
print("Fin programme")
