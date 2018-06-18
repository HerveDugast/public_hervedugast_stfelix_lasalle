#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : citroen_ds.py       version 1.0
Date : 09-02-2018
Auteur : Hervé Dugast
Source : http://deusyss.developpez.com/tutoriels/Python/Pyreverse/

Fonction classe :
   crée un objet voiture avec les méthodes : démarrer, stopper, état_moteur...

------- affichage console ----------------
Citroen
DS moderne (>2000)
Hydractives
False
True
Suppression de la voiture
------------------------------------------
"""
from voiture import Voiture
from citroen import Citroen
from cb import CB

class CitroenDs(Voiture, Citroen):
   def __init__(self):
      Voiture.__init__(self)
      Citroen.__init__(self)
      self.modele = "DS moderne (>2000)"
      self._option_payante_ds_01 = False
      self._option_payante_ds_02 = False
      self._option_payante_ds_03 = False
      self.__option_calculateur_ds_01 = False
      self.__option_calculateur_ds_02 = False
      self.__option_calculateur_ds_03 = False
      self.start_options()
      self.cb = CB()

   def __del__(self):
      print("Suppression de la voiture")

   def start_options(self):
      if self._option_payante_ds_01:
         print("GPS activé")
      if self._option_payante_ds_02:
         print("Anti dépassement lignes blanches activé")
      if self._option_payante_ds_03:
         print("Freinage urgence activé")

      if self.__option_calculateur_ds_01:
         print("Puissance moteur: 120 cv")
      elif self.__option_calculateur_ds_02:
         print("Puissance moteur: 150 cv")
      elif self.__option_calculateur_ds_03:
         print("Puissance moteur: 180 cv")

if __name__ == "__main__":
   ma_ds = CitroenDs()
   print(ma_ds.marque)
   print(ma_ds.modele)
   print(ma_ds.type_suspension)
   print(ma_ds.statut_moteur())
   ma_ds.start_moteur()
   print(ma_ds.statut_moteur())