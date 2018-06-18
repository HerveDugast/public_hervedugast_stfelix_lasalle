#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : thread_p2_arret.py      version 1.0
Date : 17-03-2018
Auteur : Hervé Dugast
source : https://python.developpez.com/faq/?page=Thread

Fonctionnement :
   Affiche exécution de 3 threads (compteur infini). Demande l'arrêt de chacun des threads et 
   montre l'arrêt propre de chaque thread.
   
   Principe utilisé pour arrêter proprement le thread :
   Dans la méthode run, on utilise une boucle while qui exécute ses instructions tant qu'aucun
   événement de type arrêt est actif. Pour déclencher un événement de type arrêt, on utilise la 
   méthode stop qui appelera la méthode monEvent._stopevent.set(). Lorsque cette dernière est 
   appelée, la boucle while se termine, ce qui arrête proprement le thread.
   En utilisant la classe Event, on accélère l'arrêt du thread. En effet, la méthode 
   monEvent.wait(timeout) bloque l'exécution du thread pendant la durée timeout, sauf si la méthode
   monEvent._stopevent.set() est appelée entre temps. Autrement dit, l'utilisation de 
   monEvent.wait(timeout) permet d'effectuer une temporisation que l'on peut interrompre grâce à
   monEvent._stopevent.set(), ce qui n'aurait pas été possible avec un time.sleep(duree).
   
------- affichage console ------------------------------------------------------
Thread A 0
Thread B 0
Thread C 0
Thread A 1
Thread B 1
Thread C 1
-> Demande arrêt Thread B
* Le thread Thread B s'est termine proprement
Thread A 2
Thread C 2
Thread C 3
Thread A 3
Thread C 4
-> Demande arrêt Thread C
-> a.join(timeout=5) lancé. Prog principal bloqué !
Thread A 4
* Le thread Thread C s'est termine proprement
Thread A 5
Thread A 6
* timeout a.join() écoulé... Prog principal reprend... Thread A continue...
Thread A 7
Thread A 8
-> Demande arrêt Thread A
* Le thread Thread A s'est termine proprement
--- Fin programme ---
--------------------------------------------------------------------------------
"""
from threading import Thread, Event
import time

class Affiche(Thread): 
   
   def __init__(self, nom = ''): 
      """ constructeur
      """
      Thread.__init__(self) 
      self.nom = nom 
      # 
      self._stopevent = Event() 

   def run(self): 
      i = 0 
      while not self._stopevent.isSet(): 
         print(self.nom, i)
         i += 1 
         self._stopevent.wait(2.0) 
      print("* Le thread "+self.nom +" s'est termine proprement")
 
   def stop(self): 
      self._stopevent.set( ) 

a = Affiche('Thread A') 
b = Affiche('Thread B') 
c = Affiche('Thread C') 

a.start() 
b.start() 
c.start() 
time.sleep(3)
print("-> Demande arrêt Thread B")
b.stop() 
time.sleep(5) 
print("-> Demande arrêt Thread C")
c.stop()
# bloque le programme principal à cet endroit jusqu'à ce que le thread A se termine ou que le 
# timeout=7 soit écoulé. Attention, dans notre cas, le programme principal reprendra son exécution
# à la fin du timeout et le thread A continuera également son exécution.
print("-> a.join(timeout=5) lancé. Prog principal bloqué !")
a.join(timeout=5)
print("* timeout a.join() écoulé... Prog principal reprend... Thread A continue...")
time.sleep(4)
print("-> Demande arrêt Thread A")
a.stop()
# un petit délai s'écoule entre la demande d'arrêt du thread et son arrêt réel 
time.sleep(1)
print("--- Fin programme ---")
