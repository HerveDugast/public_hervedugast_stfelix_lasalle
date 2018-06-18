#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : thread_p2_arret.py      version 1.0
Date : 17-03-2018
Auteur : Hervé Dugast
source : https://python.developpez.com/faq/?page=Thread

Fonctionnement :
  Thread a compte de 1 à 5 à une certaine vitesse, et affiche son comptage au fur et à mesure.
  Thread b compte de 1 à 5 quatre fois plus vite que thread a et affiche aussi son comptage.

------- affichage console ------------------------------------------------------
thread_a 1
thread_b 1
-> Exécution de b.join()... Bloque exécution programme principal jusqu'à arrêt thread_b
thread_b 2
thread_b 3
thread_b 4
thread_a 2
thread_b 5
thread_b 6
thread_b 7
thread_b 8
thread_a 3
thread_b 9
thread_b 10
*** Fin thread_b
-> Reprise exécution programme principal
-> Exécution de a.join()... Bloque exécution programme principal jusqu'à arrêt thread_a
thread_a 4
thread_a 5
*** Fin thread_a
-> Reprise exécution programme principal
--- Fin programme ---
--------------------------------------------------------------------------------
Principe utilisation module threading.py
threading.Thread( group=None, target=None, name=None, args=(), kwargs={}) où :
   - group doit rester à None, en attendant que la classe ThreadGroup soit implantée ;
   - target est la fonction appelée par le Thread ;
   - name est le nom du Thread ;
   - args est un tuple d'arguments pour l'appel de la fonction target ;
   - kwargs est un dictionnaire d'arguments pour l'appel de la fonction target.
"""
import threading
import time

def afficheComptage(nb, vitesse, nom=''): 
   """ Compte de 1 à nb à une certaine vitesse. Affiche le comptage et le nom du thread qui a 
       appelé la fonction.
   """
   for i in range(1, nb+1):
      print(nom, i)
      time.sleep(vitesse*0.1)      # définit la vitesse de comptage et donc d'affichage
   print("*** Fin {}".format(nom))

if __name__ == "__main__":
   # lance le thread a -> appel fonction afficheComptage(5, 4, nom='thread_a')
   a = threading.Thread(None, afficheComptage, None, (5, 4,), {'nom':'thread_a'}) 
   # lance le thread b -> appel fonction afficheComptage(10, 1, nom='thread_b')
   b = threading.Thread(None, afficheComptage, None, (10, 1,), {'nom':'thread_b'}) 
   a.start() 
   b.start()
   # Méthode join d'un thread permet de bloquer le programme principal jusqu'à l'arrêt de ce thread.
   print("-> Exécution de b.join()... Bloque exécution programme principal jusqu'à arrêt thread_b")
   b.join()
   print("-> Reprise exécution programme principal")
   print("-> Exécution de a.join()... Bloque exécution programme principal jusqu'à arrêt thread_a")
   a.join()
   print("-> Reprise exécution programme principal")
   print("--- Fin programme ---")