#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : CHerbivore.py     version 1.0
Date : 12-03-2018
Auteur : Hervé Dugast
"""
from CAnimal import CAnimal

class CHerbivore(CAnimal):
   
   def __init__(self):
      super().__init__()
      self.__armeDefense = input("Arme défense ? ")
      
   def manger(self):
      """ Affiche le repas habituel
      """
      print("{} se défend avec {} et mange des plantes !" \
           .format(self._nom.upper(), self.__armeDefense.upper()))
