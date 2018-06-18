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
   Ce test unitaire doit être lancé dans une console : python3 -m unittest

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++ Affichage console en cas de succès ++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
pi@raspi3btssn:~ $ cd prog/test_unitaire/openclassroom/
pi@raspi3btssn:~/prog/test_unitaire/openclassroom $ python3 -m unittest         ...
----------------------------------------------------------------------
Ran 3 tests in 0.007s

OK
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++ Affichage console en cas d'échec ++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
pi@raspi3btssn:~/prog/test_unitaire/openclassroom $ python3 -m unittest
FE.
======================================================================
ERROR: test_sample (test_random_unittest.RandomTest)
Test le fonctionnement de la fonction 'random.sample'.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/pi/prog/test_unitaire/openclassroom/test_random_unittest.py", line 103, in test_sample
    extrait = random.sample(self.liste, 1000)  # provoque une erreur volontairement
  File "/usr/lib/python3.4/random.py", line 315, in sample
    raise ValueError("Sample larger than population")
ValueError: Sample larger than population

======================================================================
FAIL: test_choice (test_random_unittest.RandomTest)
Test le fonctionnement de la fonction 'random.choice'.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/pi/prog/test_unitaire/openclassroom/test_random_unittest.py", line 89, in test_choice
    self.assertIn(elt, ["a","b","c"])   # provoque un échec volontairement
AssertionError: 1 not found in ['a', 'b', 'c']

----------------------------------------------------------------------
Ran 3 tests in 0.005s

FAILED (failures=1, errors=1)

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
import unittest

class RandomTest(unittest.TestCase):
    """Test case utilisé pour tester les fonctions du module 'random'."""

    def setUp(self):
        """Initialisation des tests."""
        self.liste = list(range(10))

    def test_choice(self):
        """Test le fonctionnement de la fonction 'random.choice'."""
        elt = random.choice(self.liste)
        # instructions pour faire réussir ou échouer le test.
        #    succès : décommenter self.assertIn(elt, self.liste) et commenter instruction qui la suit
        #    échec  : décommenter self.assertIn(elt, ["a","b","c"]) et commenter instruction qui la précède
        #self.assertIn(elt, self.liste)
        self.assertIn(elt, ["a","b","c"])   # provoque un échec volontairement
        
    def test_shuffle(self):
        """Test le fonctionnement de la fonction 'random.shuffle'."""
        random.shuffle(self.liste)
        self.liste.sort()
        self.assertEqual(self.liste, list(range(10)))

    def test_sample(self):
        """Test le fonctionnement de la fonction 'random.sample'."""
        # instructions pour faire réussir ou échouer le test.
        #    succès : décommenter extrait = random.sample(self.liste, 5) et commenter l'autre instruction
        #    échec  : décommenter extrait = random.sample(self.liste, 1000) et commenter l'autre instruction
        #extrait = random.sample(self.liste, 5)
        extrait = random.sample(self.liste, 1000)  # provoque une erreur volontairement
        for element in extrait:
            self.assertIn(element, self.liste)

        with self.assertRaises(ValueError):
            random.sample(self.liste, 20)
