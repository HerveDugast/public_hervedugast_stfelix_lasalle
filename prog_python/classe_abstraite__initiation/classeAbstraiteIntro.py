#!/usr/bin/python3.4
# coding: utf-8

""" 
Programme (classe) : classeAbstraiteIntro.py       version 1.0
Date : 13-02-2018
Auteur : Hervé Dugast
source https://www.python-course.eu/python3_abstract_classes.php

Fonctionnement :
   Mise en évidence du fonctionnement d'une classe abstraite. 
   Essai d'instanciation la classe abstraite -> Error si classe réellement abstraite
   Essai d'instanciation de la classe fille -> Error si classe mère réellement abstraite
   
------- affichage console ------------------------------------------------------
<__main__.AbstractClass object at 0x00000000047A7198>

<__main__.B object at 0x00000000047A7208>

La classe AbstractClass n'est pas une classe abstraite car il est possible
- de créer une instance à partir de la classe mère
- de créer une instance à partir de la classe fille B sans implémenter la méthode
  abstraite do_something dans celle-ci
--------------------------------------------------------------------------------
"""

class AbstractClass:

   def do_something(self):
      pass

class B(AbstractClass):
   pass

if __name__ == "__main__":
   a = AbstractClass()
   print(a)
   print("")
   
   b = B()
   print(b)
   print("")
   print("La classe AbstractClass n'est pas une classe abstraite car il est possible")
   print("- de créer une instance à partir de la classe mère")
   print("- de créer une instance à partir de la classe fille B sans implémenter la méthode")
   print("  abstraite do_something dans celle-ci")
   