#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : ex05_volumeSphere.py     version : 1.0
Auteur : H. Dugast
Source : http://hebergement.u-psud.fr/iut-orsay/Pedagogie/MPHY/Python/exercices-python3.pdf
Date : 06-05-2017

Fonction :
Écrire une fonction volumeSphere qui calcule le volume d’une sphère de rayon r fourni en argument
et qui utilise la fonction cube.
Tester la fonction volumeSphere par un appel dans le programme principal.

Exemple d'exécution pour un rayon de 3 cm :
Rayon (cm) : 3
Volume de la sphere de rayon 3.0 cm : 113.097 cm3
"""
result1 = []
for i in range(6):
   result1.append(i+3)
print(" boucle for ".center(50, '-'))
print(result1, '\n')
rien = input('"Entree"')
result2 = [i+3 for i in range(6)]
print(" forme 1 ".center(50, '-'))
print(result2)