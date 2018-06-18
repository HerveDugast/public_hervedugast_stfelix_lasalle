#!/usr/bin/python3.4
# coding: utf-8

""" 
Programme (classe) : classeAbstraiteOk.py       version 1.0
Date : 13-02-2018
Auteur : Hervé Dugast
source https://www.python-course.eu/python3_abstract_classes.php

Fonctionnement :
   Mise en évidence du fonctionnement d'une classe abstraite. 
   Essai d'instanciation la classe abstraite -> Error si classe réellement abstraite
   Essai d'instanciation de la classe fille -> Ok si classe mère réellement abstraite
   
------- affichage console ------------------------------------------------------
Exécution de !  a = AbstractClassExample() 
Can't instantiate abstract class AbstractClassExample with abstract methods do_something
Cette erreur est normale puisque AbstractClassExample est une classe abstraite !

Exécution de  x = DoAdd42(10) puis de print(x.do_something())
x = 52

Exécution de  y = DoMul42(10) puis de print(y.do_something())
y = 420
--------------------------------------------------------------------------------
"""

from abc import ABC, abstractmethod

class AbstractClassExample(ABC):

   def __init__(self, value):
      self.value = value
      super().__init__()

   @abstractmethod
   def do_something(self):
      pass


class DoAdd42(AbstractClassExample):
   
   def do_something(self):
      return self.value + 42

   
class DoMul42(AbstractClassExample):
   
   def do_something(self):
      return self.value * 42   


if __name__ == "__main__":
   try:
      print("Exécution de !  a = AbstractClassExample() ")
      a = AbstractClassExample()
   except TypeError as e:
      print(e)
      print("Cette erreur est normale puisque AbstractClassExample est une classe abstraite !")
   
   print("\nExécution de  x = DoAdd42(10) puis de print(x.do_something())")
   x = DoAdd42(10)
   print("x = {}".format(x.do_something()))
   
   print("\nExécution de  y = DoMul42(10) puis de print(y.do_something())")
   y = DoMul42(10)
   print("y = {}".format(y.do_something()))
   