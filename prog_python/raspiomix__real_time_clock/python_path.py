#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : python_path.py       version 1.0
Date : 30-01-2018
Auteur : Hervé Dugast

intérêt de ce module :
   Permet d'ajouter le dossier parent du dossier contenant le projet dans le PYTHONPATH.
   Cela permet d'accéder aux modules situés dans les dossiers adjacents.

---- Affichage du PYTHONPATH dans la console si la commande print est décommentée -----------------
['/home/pi/prog', '/home/pi/prog/real_time_clock', '/usr/lib/python3.4', 
'/usr/lib/python3.4/plat-arm-linux-gnueabihf', '/usr/lib/python3.4/lib-dynload', 
'/usr/local/lib/python3.4/dist-packages', '/usr/lib/python3/dist-packages', 
'/usr/lib/python3.4/dist-packages']
---------------------------------------------------------------------------------------------------

Arborescence conseillée pour les projets raspberry de BTS SN
Exemple avec le projet real_time_clock (modules écrits par l'utilisateur pi)
/
|-- home
|     |-- pi
|     |    |-- prog
|     |    |     | -- real_time_clock  # nom du dossier contenant les modules personnels du projet
|     |    |     | -- library          # contient modules communs : bibliothèques, classes...
|     |    |     | -- test_unitaire    # contient modules tests unitaires

"""

# Ajout du chemin d'accès au dossier parent du projet dans le python PATH. 
# Cela permet d'accéder aux modules situés dans les dossiers adjacents
# RENSEIGNEZ correctement la variable NOM_DOSSIER_PROJET avec le nom de dossier de votre projet.
NOM_DOSSIER_PROJET = 'real_time_clock'
import sys, os
chemin = os.path.dirname(os.path.abspath(__file__))
while (not chemin.endswith(NOM_DOSSIER_PROJET)) and chemin != '/':
   chemin = os.path.dirname(chemin)
if chemin == '/':
   print('ERREUR ! NOM_DOSSIER_PROJET = {}'.format(NOM_DOSSIER_PROJET))
   print('Ce dossier est introuvable... FIN du programme')
   sys.exit(0)
chemin = os.path.dirname(chemin)
if chemin not in sys.path:
   sys.path.insert(0, chemin)
#print(sys.path)   #pour afficher le python PATH