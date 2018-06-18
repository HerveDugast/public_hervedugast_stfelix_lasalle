#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : dateCalcul.py     version : 1.1
Auteur : H. Dugast
Date : 10-01-2017
Matériel utilisé : carte raspberry, carte raspiOmix+
Fonction :
    Calcule la durée écoulée entre 2 dates
    Utilise l'appel système et non une horloge temps réel i2c (si elle est présente)

Exemple d'ecéution :
    Date courante : 2017-01-13 16:07:51.830745
    Date début : 2016-12-01 14:30:00
    Durée entre les 2 dates : 43 days, 1:37:51.830745   (à la microseconde près)
    Durée entre les 2 dates : 43 days, 1:37:52   (à la seconde près)
    Durée entre les 2 dates : 3721072 secondes
    Durée entre les 2 dates : 43 jours, 1:37:52
"""

import datetime as dat

dateCourante = dat.datetime.now()
dateDebut = dat.datetime(2016, 12, 1, 14, 30, 0)  # 1 décembre 2016 14h30m0s
duree = dateCourante - dateDebut
dureeEnSecond = round(duree.total_seconds())
if duree.days > 0:
    dureeHoraire = dureeEnSecond - duree.days * 24 * 3600
else:
    dureeHoraire = dureeEnSecond

print("Date courante : %s" % dateCourante)
print("Date début : %s" % dateDebut)
print("Durée entre les 2 dates : %s   (à la microseconde près)" % duree)
print("Durée entre les 2 dates : %s   (à la seconde près)" % dat.timedelta(seconds = dureeEnSecond))
print("Durée entre les 2 dates : %s secondes" % dureeEnSecond)
print("Durée entre les 2 dates : %i jours, %s" % (duree.days, dat.timedelta(seconds = dureeHoraire)))
