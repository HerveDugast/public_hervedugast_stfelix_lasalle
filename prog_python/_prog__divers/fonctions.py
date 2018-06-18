#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : fonctions.py       version 1.4
Date : 07-12-2017
Auteur : Hervé Dugast
Source : https://openclassrooms.com/courses/apprenez-a-programmer-en-python

Fonctionnement programme :
  Module fonctions contenant des fonctions arithmétiques

------- affichage console ----------------
Table de multiplication de  4
1  *  4  =  4
2  *  4  =  8
...
10  *  4  =  40
Table d'addition de  4
0  +  4  =  4
1  +  4  =  5
...
10  +  4  =  14
Soustraction entre 2 nombres
2  -  9  =  -7
Division entre 2 nombres
10  /  3  =  3.3333333333333335
------------------------------------------
"""

def tableMultiplication(nb, nbMax=10):
   """Fonction affichant la table de multiplication par nb
      de 1 * nb jusqu'à nbMax * nb  """
   print("Table de multiplication de ", nb)
   i = 0
   while i < nbMax:
      print(i+1, " * ", nb, " = ", (i+1) * nb)
      i += 1

def tableAddition(nb, nbmax=10):
   """Fonction affichant la table d'addition de nb
      de nb + 0  à  jusqu'à  nb + nbMax  """
   print("Table d'addition de ", nb)
   for i in range(nbmax+1):
      print(i, " + ", nb, " = ", i+nb)
      i += 1
      
def soustraction(nb1, nb2):
   """Fonction affichant la soustraction entre 2 nombres"""
   print("Soustraction entre 2 nombres")
   print(nb1, " - ", nb2, " = ", nb1 - nb2)

def division(nb1, nb2):
   """Fonction affichant la division entre 2 nombres
      Vérifie la validité des paramètres saisis"""
   print("\nDivision entre 2 nombres")
   try:
      print(nb1, " / ", nb2, " = ", end='')
      nb = int(nb1)  # pour tester si c'est un nombre
      nb = int(nb2)
      result = nb1 / nb2
      print(result)
   except ValueError as err:
      print("\nErreur : ", str(err))
      print("variable numérateur ou dénominateur possède type incompatible avec division !")
   except ZeroDivisionError as err:
      print("\nErreur : ", str(err))

# test des fonctions arithmétiques
if __name__ == "__main__":
   tableMultiplication(4)
   tableAddition(4)
   soustraction(2, 9)
   division(10, 3)