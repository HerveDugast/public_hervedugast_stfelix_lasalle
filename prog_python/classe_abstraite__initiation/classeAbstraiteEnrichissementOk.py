#!/usr/bin/python3.4
# coding: utf-8

""" 
Programme (classe) : classeAbstraiteEnrichissementOk.py       version 1.0
Date : 13-02-2018
Auteur : Hervé Dugast
source https://www.python-course.eu/python3_abstract_classes.php

Fonctionnement :
   Mise en évidence du fonctionnement d'une classe abstraite. 
   Implémentation de la méthode abstraite dans la classe mère.
   Enrichissement de cette méthode dans la classe fille.
   
------- affichage console ------------------------------------------------------
Exécution de !  a = AbstractClassExample() 
Can't instantiate abstract class AbstractClassExample with abstract methods do_something
Cette erreur est normale puisque AbstractClassExample est une classe abstraite !

Exécution de  x = AnotherSubclass() puis de print(x.do_something())
Some implementation!
The enrichment from AnotherSubclass
--------------------------------------------------------------------------------
"""

from abc import ABC, abstractmethod

class AbstractClassExample(ABC):

   @abstractmethod
   def do_something(self):
      print("Some implementation!")

class AnotherSubclass(AbstractClassExample):
   def do_something(self):
      super().do_something()
      print("The enrichment from AnotherSubclass")


if __name__ == "__main__":
   try:
      print("Exécution de :   a = AbstractClassExample() ")
      a = AbstractClassExample()
   except TypeError as e:
      print(e)
      print("Cette erreur est normale puisque AbstractClassExample est une classe abstraite !")
   
   print("\nExécution de  x = AnotherSubclass() puis de print(x.do_something())")
   x = AnotherSubclass()
   x.do_something()
   