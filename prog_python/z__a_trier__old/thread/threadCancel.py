#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : threadCancel.py     version : 1.0
!!!!!!!!!!!!!!!!!!!!!!! Programme en cours de développement !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Ne fonctionne pas car non terminé
https://stackoverflow.com/questions/9812344/cancellable-threading-timer-in-python

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

import threading
import time

class TimerThread(threading.Thread):
   def __init__(self, timeout=3, sleep_chunk=0.25, callback=None, *args):
      threading.Thread.__init__(self)

      self.timeout = timeout
      self.sleep_chunk = sleep_chunk
      if callback == None:
         self.callback = None
      else:
         self.callback = callback
      self.callback_args = args

      self.terminate_event = threading.Event()
      self.start_event = threading.Event()
      self.reset_event = threading.Event()
      self.count = self.timeout/self.sleep_chunk

   def run(self):
      while not self.terminate_event.is_set():
         while self.count > 0 and self.start_event.is_set():
            # print self.count
            # time.sleep(self.sleep_chunk)
            # if self.reset_event.is_set():
            if self.reset_event.wait(self.sleep_chunk):  # wait for a small chunk of timeout
               self.reset_event.clear()
               self.count = self.timeout/self.sleep_chunk  # reset
            self.count -= 1
         if self.count <= 0:
            self.start_event.clear()
            #print 'timeout. calling function...'
            self.callback(*self.callback_args)
            self.count = self.timeout/self.sleep_chunk  #reset

   def start_timer(self):
      self.start_event.set()

   def stop_timer(self):
      self.start_event.clear()
      self.count = self.timeout / self.sleep_chunk  # reset

   def restart_timer(self):
      # reset only if timer is running. otherwise start timer afresh
      if self.start_event.is_set():
         self.reset_event.set()
      else:
         self.start_event.set()

   def terminate(self):
      self.terminate_event.set()

#=================================================================
def my_callback_function():
   print('timeout, do this...')
   
def saisie_clavier():
   reponse = input("Q:quit S:Stop R:Restart  Q, S ou R ? ")
   

timeout = 6  # sec
sleep_chunk = .25  # sec

tmr = TimerThread(timeout, sleep_chunk, my_callback_function)
saisie = TimerThread(timeout, sleep_chunk, my_callback_function)

tmr.start()
saisie.start()

quit = '0'
while True:
   quit = input("Proceed or quit: ")
   if quit == 'q':
      tmr.terminate()
      tmr.join()
      break
   tmr.start_timer()
   #if input("Stop ? : ") == 's':
      #tmr.stop_timer()
   #if input("Restart ? : ") == 'r':
      #tmr.restart_timer()