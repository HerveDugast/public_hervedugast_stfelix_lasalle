#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : dateHeureCourante.py     version : 1.0
Auteur : H. Dugast
Date : 24-04-2017
Matériel utilisé :  ordinateur sous windows (avec wing ide par exemple)
Fonction :
    Affiche l'heure courante puis chaque élément de la date de manière isolée

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

from datetime import datetime

dateCourante = datetime.now()
nomJourSemaine = ('Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche')
nomMois = ('Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 
           'Octobre', 'Novembre', 'Décembre') 

print("Date courante : %s" % dateCourante)
print("Date courante : %s" % dateCourante.date())
print("Date courante : %s" % dateCourante.time())
print("Jour semaine : %s" % nomJourSemaine[dateCourante.weekday()])
print("Jour : %s" % dateCourante.day)
print("Mois : %s" % nomMois[dateCourante.month - 1])
print("Année : %s" % dateCourante.year)
print("Heure : %s" % dateCourante.hour)
print("Minute : %s" % dateCourante.minute)
print("Seconde : %s" % dateCourante.second)
