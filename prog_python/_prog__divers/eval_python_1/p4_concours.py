#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : p4_concours.py       version 1.2
Date : 17-01-2018
Auteur : Hervé Dugast
 
Fonctionnement programme :
  Calcule et affiche le nombre de points obtenu par les pêcheurs
  lors d'un concours de pêche
  
------- affichage console exemple 1 ----------------
Taille poisson n° 1 (en cm) ? 0
Nombre de prises : 0
Total point concours : 0
----------------------------------------------------

------- affichage console exemple 2 ----------------
Taille poisson n° 1 (en cm) ? 10
Poids poisson n° 1 (en g) ? 100
Taille poisson n° 2 (en cm) ? 23
Poids poisson n° 2 (en g) ? 500
Taille poisson n° 3 (en cm) ? 0
Nombre de prises : 2
Total point concours : 639
----------------------------------------------------
"""
POINT_PAR_POISSON = 3
# saisie des prises lors du concours
tailleP = []      # en cm
poidsP = []       # en gramme

def saisiePeche():
    nbPoissons = 0
    taille = 1
    while taille > 0:
        taille = int(input("Taille poisson n° {} (en cm) ? ".format(nbPoissons+1)))
        if taille > 0:
            tailleP.append(taille)
            poids = int(input("Poids poisson n° {} (en g) ? ".format(nbPoissons+1)))
            poidsP.append(poids)
            nbPoissons += 1
    return nbPoissons

def calculerPoints(nbPoissons):
    totalPoints = 0
    for i in range(nbPoissons):
        totalPoints += POINT_PAR_POISSON + tailleP[i] + poidsP[i]
    return totalPoints

# *** 2ème solution pour coder la fonction calculerPoints ***
# def calculerPoints(nbPoissons):
    # totalPoints = nbPoissons*POINT_PAR_POISSON + sum(tailleP) + sum(poidsP)
    # return totalPoints

# ------------------ Programme principal -----------------------------
nombrePoissons = saisiePeche()
points = calculerPoints(nombrePoissons)
print("Nombre de prises : {}".format(nombrePoissons))
print("Total point concours : {}".format(points))
        

