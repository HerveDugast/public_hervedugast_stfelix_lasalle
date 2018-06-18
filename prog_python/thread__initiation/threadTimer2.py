#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : threadTimer2.py     version : 1.0
Auteur : H. Dugast
Date : 25-05-2017
Matériel utilisé :  ordinateur sous windows (avec wing ide par exemple)
Fonction :
Création de 2 threads. Un thread affiche un compteur qui s'incrémente toutes les 0,5 seconde.
Le 2ème thread affiche un compteur qui s'incrémente toutes les 2 secondes.
Ce programme ne s'arrête jamais

--- Console affiche ---
timer 0,5s :   11
timer 2s :   6.621404949566414e-07
timer 0,5s :   12
timer 0,5s :   13
timer 0,5s :   14
timer 2s :   2.033549996738958
timer 0,5s :   15
timer 0,5s :   16
timer 0,5s :   17
timer 0,5s :   18
timer 2s :   4.042817646176618
timer 0,5s :   19
timer 0,5s :   20
...
"""
import time
import threading 

def timer1(tempo):
   """ thread lancé automatiquement toutes les "tempo" secondes """
   threading.Timer(tempo, timer1, [tempo]).start() 
   ## Reste du traitement
   # initialisation variable statique
   timer1.counter = getattr(timer1, 'counter', 10)
   timer1.counter += 1
   print("timer 0,5s :  ", timer1.counter)
   
def timer2(tempo = 1.0): 
   threading.Timer(tempo, timer2, [tempo]).start() 
   ## verification de la proprete du timer 
   print("timer 2s :  ", time.clock())
   ## Reste du traitement 
   
timer1(0.5)
timer2(2.0)
while True:
   pass
print("Fin")