#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : voiture.py       version 1.0
Date : 09-02-2018
Auteur : Hervé Dugast
Source : http://deusyss.developpez.com/tutoriels/Python/Pyreverse/

Fonction classe :
   crée un objet voiture avec les méthodes : démarrer, stopper, état_moteur

------- affichage console ----------------
Etat moteur : False
Appel méthode start_moteur()
Etat moteur : True
------------------------------------------
"""
class Voiture():
   def __init__(self):
      self.nombre_roues = 4
      self.nombre_fauteuils = 1
      self.moteur = False
      self.volant = True

   def start_moteur(self):
      self.moteur = True
      return self.moteur

   def stop_moteur(self):
      self.moteur = False
      return self.moteur

   def statut_moteur(self):
      return self.moteur

if __name__ == "__main__":
   ma_voiture_basique = Voiture()
   print("Etat moteur :", ma_voiture_basique.statut_moteur())
   print("Appel méthode start_moteur()")
   ma_voiture_basique.start_moteur()
   print("Etat moteur :", ma_voiture_basique.statut_moteur())
   