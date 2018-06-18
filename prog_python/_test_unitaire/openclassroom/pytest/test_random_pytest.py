#!/usr/bin/python3.4
# coding: utf-8

"""
Programme : test_random_unittest.py       version 1.1
Date : 30-11-2017
Auteur : Hervé Dugast
Source : https://openclassrooms.com/courses/apprenez-a-programmer-en-python/les-tests-unitaires-
    avec-unittest
Fonctionnement :
   Ce programme réalise 3 tests unitaires sur certaines méthodes du module random : random.choice,
   random.shuffle et random.sample. Le résultat est forcément un succès car random est un module
   officiel de python.
   Ce test unitaire doit être lancé dans une console : pytest   ou   pytest -s
   Pour installer le module pytest : $ sudo pip3 install -U pytest 

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++ Affichage console en cas de succès ++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
pi@raspi3btssn:~/prog/test_unitaire/openclassroom/pytest $ pytest
============================= test session starts ==============================
platform linux -- Python 3.4.2, pytest-3.2.5, py-1.5.2, pluggy-0.4.0
rootdir: /home/pi/prog/test_unitaire/openclassroom/pytest, inifile:
collected 3 items

test_random_pytest.py ...

=========================== 3 passed in 0.11 seconds ===========================

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++ Affichage console en cas de succès ++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
pi@raspi3btssn:~/prog/test_unitaire/openclassroom/pytest $ pytest -s
============================= test session starts ==============================
platform linux -- Python 3.4.2, pytest-3.2.5, py-1.5.2, pluggy-0.4.0
rootdir: /home/pi/prog/test_unitaire/openclassroom/pytest, inifile:
collected 3 items

test_random_pytest.py --- Début TU ---
.--- Fin TU ---
.--- Début TU ---
.--- Fin TU ---

=========================== 3 passed in 0.11 seconds ===========================

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++ Affichage console en cas d'échec ++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
pi@raspi3btssn:~/prog/test_unitaire/openclassroom/pytest $ pytest -s
============================= test session starts ==============================
platform linux -- Python 3.4.2, pytest-3.2.5, py-1.5.2, pluggy-0.4.0
rootdir: /home/pi/prog/test_unitaire/openclassroom/pytest, inifile:
collected 3 items

test_random_pytest.py --- Début TU ---
F--- Fin TU ---
.--- Début TU ---
F--- Fin TU ---

=================================== FAILURES ===================================
_________________________________ test_choice __________________________________

liste_exemple = [0, 1, 2, 3, 4, 5, ...], liste_pour_echec = ['a', 'b', 'c']
    def test_choice(liste_exemple, liste_pour_echec):
    ...
>       assert elt in liste_pour_echec
E       AssertionError: assert 4 in ['a', 'b', 'c']

test_random_pytest.py:136: AssertionError
_________________________________ test_sample __________________________________

liste_exemple = [0, 1, 2, 3, 4, 5, ...], liste_pour_echec = ['a', 'b', 'c']

    def test_sample(liste_exemple, liste_pour_echec):
    ...
>       extrait = random.sample(liste_exemple, 1000)  # provoque une erreur volontairement

test_random_pytest.py:150:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <random.Random object at 0xfec208>, population = [0, 1, 2, 3, 4, 5, ...]
k = 1000

    def sample(self, population, k):
    ...
>           raise ValueError("Sample larger than population")
E           ValueError: Sample larger than population

/usr/lib/python3.4/random.py:315: ValueError
====================== 2 failed, 1 passed in 0.29 seconds ======================
pi@raspi3btssn:~/prog/test_unitaire/openclassroom/pytest $

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

import random
import pytest

# décorateur pour retourner juste la liste aux fonctions qui le demandent
@pytest.fixture(scope="function")
def liste_exemple():
    """ Crée une liste qui sera utilisée pour les tests """
    return list(range(10))

# décorateur qui exécute un bout de code avant de passer la liste aux fonctions qui le demandent
# et qui exécute un bout de code après avoir passé la liste
@pytest.yield_fixture(scope="function")
def liste_pour_echec():
    """ Crée une liste qui sera utilisée pour les tests pour provoquer un échec"""
    # bout de code exécuté avant passage liste, équivalent setUp() dans unittest 
    print("--- Début TU --- ")
    # ce qu'on renvoie (yield), ça peut être None 
    yield(["a","b","c"])
    # bout de code exécuté après passage liste, équivalent tearDown() dans unittest 
    print("--- Fin TU --- ")

def test_choice(liste_exemple, liste_pour_echec):
    """Test le fonctionnement de la fonction 'random.choice'."""
    elt = random.choice(liste_exemple)
    # instructions pour faire réussir ou échouer le test.
    #    succès : décommenter elt in liste_exemple et commenter l'autre instruction
    #    échec  : décommenter assert elt in liste_pour_echec et commenter l'autre instruction
    assert elt in liste_exemple
    #assert elt in liste_pour_echec
        
def test_shuffle(liste_exemple):
    """Test le fonctionnement de la fonction 'random.shuffle'."""
    random.shuffle(liste_exemple)
    liste_exemple.sort()
    assert liste_exemple == list(range(10))

def test_sample(liste_exemple, liste_pour_echec):
    """Test le fonctionnement de la fonction 'random.sample'."""
    # instructions pour faire réussir ou échouer le test.
    #    succès : décommenter extrait = random.sample(liste_exemple, 5) et commenter l'autre instruction
    #    échec  : décommenter extrait = random.sample(liste_exemple, 1000) et commenter l'autre instruction
    extrait = random.sample(liste_exemple, 5)
    #extrait = random.sample(liste_exemple, 1000)  # provoque une erreur volontairement
    for element in extrait:
        assert element in liste_exemple

    # vérifie que python lève bien l'erreur sans stopper le programme
    with pytest.raises(ValueError):
        random.sample(liste_exemple, 1000)
