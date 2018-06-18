#!/usr/bin/python3
# coding: utf-8
"""
Programme : testByteArray.py     version : 1.0
Auteur : H. Dugast
Date : 24-04-2017
Matériel utilisé : ordinateur sous windows (avec wing ide par exemple)
Fonctionnement programme :
Manipulation du type bytearray (liste d'octets modifiable) et du type bytes (liste d'octets 
non modifiable)
"""

elements = [0, 200, 50, 25, 10, 13, 255]
print("liste d'éléments (uniquement des octets) : ", end='')
print(elements)
# Create bytearray from list of integers.
values = bytearray(elements)
print("conversion en bytearray, affichage brut : ", end='')
print(values)
print("Affichage élément par élément (décimal) : ", end='')
for element in values:
   print(element, end = " ")
print('')
values[1] = 201
print("Affichage élément par élément (décimal) après modification, values[1] = 201 : ", end='')
for element in values:
   print(element, end = " ")
print('\n')

print("Affichage d'un type bytes (non modifiable), affichage brut : ", end='')
data = bytes(b"abc")
print(data)
print("Affichage des 2 premiers éléments du type bytes précédent, affichage brut : ", end='')
d = data[0:2]
print(d)
print("Affichage du type bytes précédent élément par élément (décimal): ", end='')
for element in data:
   print(element, end = " ")
print('')
