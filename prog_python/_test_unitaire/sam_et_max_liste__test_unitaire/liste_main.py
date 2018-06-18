#!/usr/bin/python3.4
# coding: utf-8

"""
Programme : liste_main.py       version 1.0
Date : 27-11-2017
Auteur : Hervé Dugast
Source : http://sametmax.com/un-gros-guide-bien-gras-sur-les-tests-unitaires-en-python-partie-3/

Matériel utilisé : raspberry pi 3

Fonctionnement programme :
  Teste la fonction get d'une liste, affiche le n ème élément ou le message 'Je laisse la main'
  s'il n'existe pas

------- affichage console -------------------------------------------------------
Création de la liste simple_comme_bonjour avec les éléments :
('pomme', 'banane')

Affichage du 1er élément ou du message 'Je laisse la main' s'il n'existe pas :
pomme

Affichage du 1000è élément ou du message 'Je laisse la main' s'il n'existe pas :
je laisse la main
---------------------------------------------------------------------------------

"""

import liste_fonction as liste

print('Création de la liste simple_comme_bonjour avec les éléments :')
simple_comme_bonjour = ('pomme', 'banane')
print(simple_comme_bonjour)
print("")

print("Affichage du 1er élément ou du message 'Je laisse la main' s'il n'existe pas :")
print(liste.get(simple_comme_bonjour, 0, "je laisse la main"))
print("")

print("Affichage du 1000è élément ou du message 'Je laisse la main' s'il n'existe pas :")
print(liste.get(simple_comme_bonjour, 1000, "je laisse la main"))
