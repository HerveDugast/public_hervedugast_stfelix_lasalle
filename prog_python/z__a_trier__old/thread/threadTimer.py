#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : threadTimer.py     version : 1.0
Auteur : H. Dugast
Date : 25-05-2017
Source : https://www.developpez.net/forums/d147558/autres-langages/python-zope/general-python/
   arreter-redemarrer-thread/
Matériel utilisé :  ordinateur sous windows (avec wing ide par exemple)
Fonction :
Création de 2 threads. Chacun affiche un compteur de 0 à 9.
Test des méthodes pause, reprendre et stop.
Ce programme ne s'arrête jamais

--- Console affiche ---
*** Début prog
1 0
1 1
*** timer 1 en pause
2 0
2 1
2 2
2 3
*** timer 1 reprise
2 4
1 2
1 3
2 5
1 4
2 6
1 5
2 7
*** timer 1 reset
2 8
1 0
2 9
1 1
2 0
1 2
*** timer 1 arrêt
2 1
1 3
*** Fin prog


"""

import threading
import time

class monThread(threading.Thread):
   def __init__(self, timerNum, compteurMax):
      threading.Thread.__init__(self)
      self._etat = False
      self._pause = False
      self._timerNum = timerNum
      self._cptMax = compteurMax
      self._cpt = 0

   def run(self):
      self._etat = True
      while self._etat:
         time.sleep(0.5)
         if not self._pause:
            print(self._timerNum, self._cpt)
            self._cpt = self._cpt + 1
            if self._cpt == self._cptMax:
               self._cpt = 0
            
   def stop(self):
      """Arrête l'exécution du thread. Après avoir appelé cette fonction le thread n'est plus
      utilisable.  """
      self._etat = False

   def pause(self):
      """Arrête l'exécution du thread momentanément."""
      self._pause = True
      
   def raz(self):
      """Remet à 0 le timer, l'exécution du thread continue mais reprend à 0"""
      self._cpt = 0      

   def reprendre(self):
      """Reprendre l'exécution d'un thread 'mis en pause'."""
      self._pause = False

print("*** Début prog")
timer1 = monThread(1, 10)
timer1.start()
time.sleep(1)
timer2 = monThread(2, 10)
timer2.start()
timer1.pause()
print("*** timer 1 en pause")
time.sleep(2)
print("*** timer 1 reprise")
timer1.reprendre()
time.sleep(2)
print("*** timer 1 reset")
timer1.raz()
time.sleep(2)
print("*** timer 1 arrêt")
timer1.stop()
while(1):
   pass
