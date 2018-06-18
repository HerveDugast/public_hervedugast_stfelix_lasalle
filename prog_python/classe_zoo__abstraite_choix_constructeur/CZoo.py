#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : CZoo.py     version 1.0
Date : 12-03-2018
Auteur : Hervé Dugast

------- affichage console ------------------------------------------------------
Saisir catégorie animal ('CARN' ou 'HERB') ? CARN
Nom animal ? loup
Arme attaque ? machoire
<class 'CCarnivore.CCarnivore'>
LOUP tue avec MACHOIRE pour manger d'autres animaux !

Saisir catégorie animal ('CARN' ou 'HERB') ? HERB
Nom animal ? zèbre
Arme défense ? sabots
<class 'CHerbivore.CHerbivore'>
ZÈBRE se défend avec SABOTS et mange des plantes !
--------------------------------------------------------------------------------
"""
from CAnimal import CAnimal
from CCarnivore import CCarnivore
# permet d'appeler un constructeur à l'aide de variables
import importlib

class CZoo:
   
   # Attribut statique
   # Associe la chaine d'une catégorie ("CARN"...) au nom d'un module (CCarnivore.py...) et  
   # d'une classe portant le même nom (CCarnivore()...)
   __categorie = {"CARN":"CCarnivore", "HERB":"CHerbivore"}

   def __init__(self):
      self.__animal = []
   
   def creerAnimal(self):
      """ Crée un animal dans l'une des 2 catégories : carnivore ou herbivore
      """
      categorieAnimal = input("Saisir catégorie animal ('CARN' ou 'HERB') ? ")
      for cleCat, valeurCat in CZoo.__categorie.items():
         if categorieAnimal == cleCat:
            # *****  *****
            # récupération nom du module contenant la classe du constructeur à utiliser
            # exemple : myModule = "CCarnivore" si categorieAnimal = "CARN"
            myModule = importlib.import_module(valeurCat)
            # récupération nom de la classe définie dans le module désigné
            # exemple : MyClass = CCarnivore si categorieAnimal = "CARN"
            MyClass = getattr(myModule, valeurCat)
            # crée un animal avec la classe précédemment trouvée
            animal = MyClass()
            self.__animal.append(animal)
   
   def get_animal(self, num):
      return self.__animal[num]
            
if __name__ == "__main__":
   zoo = CZoo()
   
   zoo.creerAnimal() # CARN, loup, machoire
   print(type(zoo.get_animal(0)))
   zoo.get_animal(0).manger() ; print("")
   
   zoo.creerAnimal() # HERB, zèbre, sabots
   print(type(zoo.get_animal(1)))
   zoo.get_animal(1).manger()
      
      
