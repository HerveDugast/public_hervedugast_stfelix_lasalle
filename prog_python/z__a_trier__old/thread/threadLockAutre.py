#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : threadLockAvec.py     version : 1.0
Auteur : H. Dugast
Date : 25-05-2017
Source : http://python.jpvweb.com/python/mesrecettespython/doku.php?id=thread_lock
Matériel utilisé :  ordinateur sous windows (avec wing ide par exemple)
Fonction :
Lancement de 2 threads : 1 qui incrémente une variable globale un certain nombre de fois, l'autre 
qui la décrémente le même nombre de fois, mais pas à la même vitesse.
On constate que les 2 threads ne peuvent jamais changer en même temps le contenu de la variable
globale à cause du verrou.

Exemple d'exécution pour ce programme (attention l'ordre n'est pas toujours le même):
--- Console affiche ---
+ 1
- 0
+ 1
- 0
+ 1
+ 2
- 1
+ 2
- 1
- 0
Valeur finale de la variable x =  0

"""

# inspiré de http://wikipython.flibuste.net/moin.py/QuestionsGenerales

import threading
import sys
import time

x = 0
n = 5

def fnadd() :
   global x,verrou
   for i in range(n) :
      verrou.acquire()
      x += 1
      verrou.release()
      print('+', x)
      time.sleep(1)
      
def fnsub() :
   global x,verrou
   for i in range(n) :
      verrou.acquire()
      x -= 1
      verrou.release()
      print('-', x)
      time.sleep(2)
      
verrou = threading.Lock()
t1=threading.Thread(target=fnadd)
t2=threading.Thread(target=fnsub)
t1.start()
t2.start()
t1.join()
t2.join()
print("Valeur finale de la variable x = ", x)