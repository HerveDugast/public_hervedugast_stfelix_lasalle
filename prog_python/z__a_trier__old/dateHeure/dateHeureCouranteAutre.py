#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : dateHeureCouranteAutre.py     version : 1.0
Auteur : H. Dugast
Date : 24-04-2017
Matériel utilisé :  ordinateur sous windows (avec wing ide par exemple)
Fonction :
    Affiche la date et l'heure courante en anglais puis la formate

Exemple d'exécution :
    Date courante : 2017-04-24 15:52:58.726175
    Jour semaine : Lundi
    Jour : 24
    Mois : Avril
    Année : 2017
    Heure : 15
    Minute : 52
    Seconde : 58

"""
import time

print("Timestamp : ", end='')
print(time.time())

dateHeureNow = time.localtime()
print("Objet date avec attribut : \n\t", end='')
print(dateHeureNow)
print("Année/Mois/Date de l'objet date : \n\t", end='')
print(str(dateHeureNow.tm_year) + "/" + str(dateHeureNow.tm_mon) + "/" + 
      str(dateHeureNow.tm_mday))

print("\nDate heure en anglais : ", end='')
print(time.strftime("%A %d %B %Y %H:%M:%S"))
print("Date formatée : ", end='')
print(time.strftime("%Y-%m-%d %H:%M:%S"))
print("Date formatée : ", end='')
print(time.strftime("%Y_%m_%d"))

