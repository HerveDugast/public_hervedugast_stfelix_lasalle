#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : p5_nbAmstrong.py       version 1.0
Date : 16-01-2018
Auteur : Claude Monteil            Maj : Hervé Dugast
Source : http://cregut.perso.enseeiht.fr/ENS/2015-apad-algo1/   (Xavier Crégut)
(Claude Monteil et Xavier Crégut)
 
Fonctionnement programme :
  Affiche les nombres de Amstrong : nombres entre 100 et 499 égaux à la
  somme des cubes de leurs 3 chiffres
  
------- affichage console --------------------------
Nombres de Amstrong (version simple)
153 = 1**3 + 5**3 + 3**3
370 = 3**3 + 7**3 + 0**3
371 = 3**3 + 7**3 + 1**3
407 = 4**3 + 0**3 + 7**3
----------------------------------------------------
"""
nb = int() # le nombre considéré
centaine = int() ; dizaine = int() ; unite = int() # les trois chiffres du nombre
sommeCubes = int() # le somme des cubes des trois chiffres
print ("Nombres de Amstrong (version simple)")
for centaine in range(1,5) :     # chiffre des centaines de 1 à 4 inclus
   for dizaine in range(0,10) :  # chiffre des dizaines de 0 à 9 inclus
      for unite in range(0,10) : # chiffre des unités de 0 à 9 inclus
         sommeCubes = centaine**3 + dizaine**3 + unite**3  # somme des cubes
         nb = centaine * 100 + dizaine * 10 + unite # nombre reconstitué
         if nb == sommeCubes :   # c’est un nombre de Amstrong
            print("{} = {}**3 + {}**3 + {}**3".format(nb, centaine, dizaine, unite))
