#!/usr/bin/python3.4
#coding: utf-8

"""
Programme (classe) : CGestionBanque.py       version 1.0
Date : 12-02-2018
Auteur : Hervé Dugast
Source :  https://www.python-course.eu/python3_properties.php

------- affichage console ------------------------------------------------------
1000
0
--------------------------------------------------------------------------------
"""
class P:

   def __init__(self,x):
      self.set_x(x)

   def get_x(self):
      return self.__x

   def set_x(self, x):
      if x < 0:
         self.__x = 0
      elif x > 1000:
         self.__x = 1000
      else:
         self.__x = x

   x = property(get_x, set_x)
         
if __name__ == "__main__":
   p1 = P(1001)
   print(p1.x)
   p1.x = -12
   print(p1.x)
   