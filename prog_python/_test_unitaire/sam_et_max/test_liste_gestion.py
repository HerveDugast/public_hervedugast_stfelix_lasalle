#!/usr/bin/python3.4
# coding: utf-8

"""
Programme : test_liste_gestion.py       version 1.1
Date : 30-11-2017
Auteur : Hervé Dugast
Source : http://sametmax.com/un-gros-guide-bien-gras-sur-les-tests-unitaires-en-python-partie-3/

Matériel utilisé : raspberry pi 3

Fonctionnement programme :
  Teste la fonction get d'une liste, affiche le n ème élément ou le message 'Je laisse la main'
  s'il n'existe pas
  le module liste_fonction.py se trouve dans le dossier sam_et_max_liste

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++ Affichage console en cas de succès ++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
pi@raspi3btssn:~/prog/test_unitaire/sam_et_max $ pytest -s
============================= test session starts ==============================
platform linux -- Python 3.4.2, pytest-3.2.5, py-1.5.2, pluggy-0.4.0
rootdir: /home/pi/prog/test_unitaire/sam_et_max, inifile:
collected 3 items

test_liste_gestion.py Avant !
.Apres !
Avant !
.Apres !
Avant !
FApres !

=================================== FAILURES ===================================
_______________________________ test_avec_echec ________________________________

simple_comme_bonjour = ('pomme', 'banane')

    def test_avec_echec(simple_comme_bonjour):
        element = liste.get(simple_comme_bonjour, 1000, 'Je laisse la main')
>       assert element == 'Je tres clair, Luc'
E       AssertionError: assert 'Je laisse la main' == 'Je tres clair, Luc'
E         - Je laisse la main
E         + Je tres clair, Luc

test_liste_gestion.py:87: AssertionError
====================== 1 failed, 2 passed in 0.18 seconds ======================
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""
   
# Ajout des chemins d'accès aux bibliothèques et modules dans le python PATH
# chemin absolu de l'exécutable
import sys
import os
chemin = os.path.dirname(os.path.abspath(__file__))
while not chemin.endswith('test_unitaire'):
    chemin = os.path.dirname(chemin)
chemin = os.path.dirname(chemin)
if chemin not in sys.path:
    sys.path.insert(0, chemin)
#print(sys.path)   #pour afficher le python PATH

import pytest
import sam_et_max_liste.liste_fonction as liste
 
# On passe de pytest.fixture() a pytest.yield_fixture()
@pytest.yield_fixture()
def simple_comme_bonjour():
    # tout ce qui est setUp() va au dessus du yield. Ca peut etre vide.
    print('Avant !')
 
    # Ce qu'on yield sera le contenu du parametre. Ca peut etre None.
    yield ('pomme', 'banane')
 
    # Ce qu'il y a apres le yield est l'equivalent du tearDown() et peut être vide aussi
    print('Apres !')
 
def test_get(simple_comme_bonjour):
    element = liste.get(simple_comme_bonjour, 0)
    assert element == 'pomme'
 
def test_element_manquant(simple_comme_bonjour):
    element = liste.get(simple_comme_bonjour, 1000, 'Je laisse la main')
    assert element == 'Je laisse la main'
 
def test_avec_echec(simple_comme_bonjour):
    element = liste.get(simple_comme_bonjour, 1000, 'Je laisse la main')
    assert element == 'Je tres clair, Luc'
