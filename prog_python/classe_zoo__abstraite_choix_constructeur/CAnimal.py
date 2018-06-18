#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : CAnimal.py     version 1.0
Date : 12-03-2018
Auteur : Hervé Dugast
"""

from abc import ABC, abstractmethod

class CAnimal(ABC):
   
   def __init__(self):
      self._nom = input("Nom animal ? ")
      
   @abstractmethod
   def manger(self):
      """ Méthode abstraite, affiche le repas habituel
          Doit être définie dans les classes filles
      """
      pass   
