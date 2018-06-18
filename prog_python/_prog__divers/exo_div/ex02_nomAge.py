#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : ex02_nomAge.py     version : 1.0
Auteur : H. Dugast
Source : http://hebergement.u-psud.fr/iut-orsay/Pedagogie/MPHY/Python/exercices-python3.pdf
Date : 06-05-2017

Fonction :
Saisir un nom et un âge en utilisant l’instruction input(). Les afficher. L'âge doit être 
transtypé (chaine -> nombre).

ton nom ? Bob
age ? 21
----------------------------------------
	 Nom : Bob	 Age : 21
"""
nom = input("ton nom ? ") # pour une chaine
age = int(input("age ? ")) # sinon : transtyper explicitement
print("{}\n\t Nom : {}\t Age : {}".format("-"*40, nom, age))