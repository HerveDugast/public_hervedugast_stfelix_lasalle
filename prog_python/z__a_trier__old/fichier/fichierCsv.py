#!/usr/bin/python3
# coding: utf-8
"""
Programme : fichierCsv.py     version : 1.0
Auteur : H. Dugast
Date : 02-05-2017
Matériel utilisé : ordinateur sous windows (avec wing ide par exemple)
Fonctionnement programme :
Manipulation de données dans un fichier au format CSV
"""

import os
import csv
import time

pathFich = "../releve/"  # chemin relatif du dossier contenant le fichier csv
nomChamp = ("Capteur", "Valeur", "Unite")
listeReleve = ( ("Temperat. ext.", 8, "degC"), ("Temperat. int.", 19.5, "degC"),
         ("Pression", 1021,"mbar") )

def fich_creerNom():
   """ Crée le nom du fichier pour chaque jour de l'année s'il n'existe pas
       Retour : chaine caractères contenant nom fichier au format :
                    releve_AAAA_MM_JJ    exemple : releve_2017_05_02"""
   dateNow = time.localtime()   # récupère la date du jour
   # crée le nom du fichier contenant la date
   fichNom = "releve_" + str('{:04d}'.format(dateNow.tm_year)) + "_" \
      + str('{:02d}'.format(dateNow.tm_mon)) + "_" + str('{:02d}'.format(dateNow.tm_mday)) + ".csv"
   return fichNom
   
# définit chemin et nom du fichier à ouvrir ou créer
pathAndFile = pathFich + fich_creerNom()

try:
   # Ouvre un fichier ou le crée s'il n'existe pas à l'emplacement indiqué
   with open(pathAndFile, 'a', newline='\n', encoding='utf-8') as fich:
      writer = csv.writer(fich, delimiter = ';')
      if os.path.getsize(pathAndFile) == 0:  # si fichier vide
         writer.writerow(nomChamp)
      for releve in listeReleve:
         writer.writerow(releve)
   fich.close()
   
   # Lit et affiche le contenu d'un fichier csv
   with open(pathAndFile, 'r', newline='', encoding='utf-8') as fich:
      reader = csv.reader(fich)
      for row in reader:
         print(row)   
   fich.close()
except FileNotFoundError as err:
   print(err)
except PermissionError as err:
   print(str(err) + '. Fichier ouvert par une application ?')
except:
   print("Erreur opération fichier")
