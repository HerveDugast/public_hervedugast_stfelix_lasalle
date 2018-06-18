#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : dico2dimension.py     version : 1.0
Auteur : H. Dugast
Date : 25-05-2017
Source : http://python.jpvweb.com/python/mesrecettespython/doku.php?id=thread_lock
Matériel utilisé :  ordinateur sous windows (avec wing ide par exemple)
Fonction :
Crée un dictionnaire à 2 dimensions

Exemple d'exécution pour ce programme (attention l'ordre n'est pas toujours le même):
--- Console affiche ---
{0: {'date': '01/02/1980', 'isMemBdd': False, 'valeur': 10}, 
 1: {'date': '02/02/1980', 'isMemBdd': False, 'valeur': 53}}

"""
mesure = {}
mesure[0] = {}
mesure[0]["valeur"] = 10
mesure[0]["date"] = "01/02/1980"
mesure[0]["isMemBdd"] = False
mesure[1] = {}
mesure[1]["valeur"] = 53
mesure[1]["date"] = "02/02/1980"
mesure[1]["isMemBdd"] = False
print(mesure)
