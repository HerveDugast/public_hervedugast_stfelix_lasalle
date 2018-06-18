#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : CCarnivore.py     version 1.0
Date : 12-03-2018
Auteur : Hervé Dugast
"""
from CAnimal import CAnimal

class CCarnivore(CAnimal):
   
   def __init__(self):
      super().__init__()
      self.__armeAttaque = input("Arme attaque ? ")
      
   def manger(self):
      """ Affiche le repas habituel
      """
      print("{} tue avec {} pour manger d'autres animaux !" \
           .format(self._nom.upper(), self.__armeAttaque.upper()))
