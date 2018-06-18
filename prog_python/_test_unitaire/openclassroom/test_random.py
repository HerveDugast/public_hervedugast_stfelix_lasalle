#!/usr/bin/python3.4
# coding: utf-8

"""
Programme : ....py       version 1.0
Date : 27-11-2017
Auteur : Hervé Dugast
Source : 
"""

import sys
import os
# chemin absolu de l'exécutable
# ici : /home/pi/prog/test_unitaire/
# remarque, ce chemin est automatiquement ajouté dans le python PATH
chemin = os.path.dirname(os.path.abspath(__file__))

# chemin absolu du dossier du projet en bas de l'arborescence
# ici : /home/pi/prog/ds1307/
while not chemin.endswith('test_unitaire'):
    chemin = os.path.dirname(chemin)

# chemin absolu du dossier parent pour accéder aux librairies et classes de même niveau
# ici : /home/pi/prog/
chemin = os.path.dirname(chemin)
 
# ajout du chemin dans le python PATH à la première position
# ici : /home/pi/prog/
# remarque, pour afficher le python PATH : print(sys.path)
if chemin not in sys.path:
    sys.path.insert(0, chemin)


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
        self.assertIn(elt, self.liste)

    def test_shuffle(self):
        """Test le fonctionnement de la fonction 'random.shuffle'."""
        random.shuffle(self.liste)
        self.liste.sort()
        self.assertEqual(self.liste, list(range(10)))

    def test_sample(self):
        """Test le fonctionnement de la fonction 'random.sample'."""
        extrait = random.sample(self.liste, 5)
        for element in extrait:
            self.assertIn(element, self.liste)

        with self.assertRaises(ValueError):
            random.sample(self.liste, 20)
