#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : ex01_vitesse.py     version : 1.0
Auteur : H. Dugast
Source : http://hebergement.u-psud.fr/iut-orsay/Pedagogie/MPHY/Python/exercices-python3.pdf
Date : 06-05-2017

Fonction :
Affectez les variables temps et distance par les valeurs 6.892 et 19.7. Calculez et affichez la 
valeur de la vitesse. Améliorez l’affichage en imposant un chiffre après le point décimal.

Résultat (affiché):
vitesse = 2.8583865351131745
------------------------------

vitesse = 2.86 m/s
"""
temps = 6.892
distance = 19.7
vitesse = distance/temps

# affichage simple :
print("vitesse =", vitesse)

# affichage formate :
print("{}".format("-"*30))
print("\nvitesse = {:.2f} m/s".format(vitesse)) # arrondi a 2 chiffres