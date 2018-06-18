#!/usr/bin/python3
# coding: utf-8
"""
Programme : bytearrayConversion.py     version : 1.0
Auteur : H. Dugast
Date : 24-04-2017
Matériel utilisé : ordinateur sous windows (avec wing ide par exemple)
Fonctions du programme :
Convertit une chaine de caractères correspondant à un grand nombre hexadécimal en type bytearray
Affiche une liste d'octets (type bytearray) sur une même ligne au format décimal, hexa ou ASCII
"""
import sys

def byte_stringHexaToBytearray(chaineCaract):
   """ Convertit une chaine de caractères contenant un nombre hexadécimal en un tableau d'octets
       Les éléments non numériques sont ignorés
       Retour : tableau d'octet (type : bytearray)
       
       Exemple 1 : 
          paramètre entrée -> chaine caractère = "0x1000FE134A"
          retour -> bytearray[0x10, 0x00, 0xFE, 0x13, 0x4A]
          (si affichage brut du bytearray -> bytearray(b'\x10\x00\xfe\x13J')) 
       Exemple 2 : cas anormal, au cas où l'entrée serait un texte
          paramètre entrée ->  chaineCaract = 'Hello world!'
          retour -> bytearray[]     # ne contient aucun élément
          (si affichage brut du bytearray -> bytearray(b'')) 
   """
   tableOctet = bytearray([])
   for i in range(0, len(chaineCaract), 2):
      octetHex = chaineCaract[i:i+2]
      # copie l'élément uniquement si celui-ci est un nombre
      try:
         tableOctet.append(int(octetHex, 16))
      except:
         pass
   return tableOctet
   
def byte_stringTextToBytearray(chaineCaract):
   """ Convertit une chaine de caractères contenant un texte en un tableau d'octets
       Retour : tableau d'octet (type : bytearray)
       
       Exemple 1 : 
          paramètre entrée -> chaine caractère = "0x1000FE134A"
          retour -> 
             bytearray[0x30, 0x78, 0x31, 0x30, 0x30, 0x30, 0x46, 0x45, 0x31, 0x33, 0x34, 0x41]
          (si affichage brut du bytearray -> bytearray(b'\x10\x00\xfe\x13J')) 
       Exemple 2 : 
          paramètre entrée ->  chaineCaract = 'Hello world!'
          retour -> 
             (bytearray[0x48, 0x65, 0x6c, 0x6c, 0x6f, 0x20, 0x77, 0x6f, 0x72, 0x6c, 0x64, 0x21]
          (si affichage brut du bytearray -> bytearray(b'0x1000FE134A')) 
       
       """
   tableOctet = bytearray([])
   # la conversion est effectuée uniquement si le message correspond à un texte
   try:
      tableOctet = bytearray(chaineCaract.encode())
   except:
      pass
   return tableOctet
   
def byte_afficherBytearrayHexa(tableOctet, separateur = ' '):
   """ Affiche le contenu d'un type bytearray (tableau d'octets) en hexadécimal
       Chaque octet est séparé par le séparateur passé en paramètre : '', ' ', '/' ...
       Exemple 1 : 
          paramètre entrée -> (bytearray[0x10, 0x00, 0xFE, 0x13, 0x4A], ' ')
          affichage -> 10 00 fe 13 4a
       Exemple 2 : bytearray contenant les codes ascii du message textuel "Hello world!"
          paramètre entrée ->  
            (bytearray[0x48, 0x65, 0x6c, 0x6c, 0x6f, 0x20, 0x77, 0x6f, 0x72, 0x6c, 0x64, 0x21], ' ') 
          affichage -> 48 65 6c 6c 6f 20 77 6f 72 6c 64 21
   """
   for idx, octet in enumerate(tableOctet):
      if idx != len(tableOctet) - 1:
         print("%s%s" % ('{:02x}'.format(octet), separateur), end ='')
      else:    # évite d'afficher le séparateur après le dernier octet affiché
         print('{:02x}'.format(octet))
   
def byte_afficherBytearrayDecimal(tableOctet, separateur = ' '):
   """ Affiche le contenu d'un type bytearray (tableau d'octets) en décimal
       Chaque octet est séparé par le séparateur passé en paramètre : '', ' ', '/' ...

       Exemple 1 : 
          paramètre entrée -> (bytearray[0x10, 0x00, 0xFE, 0x13, 0x4A], ' ')
          affichage -> 16 0 254 19 74
       Exemple 2 : bytearray contenant les codes ascii du message textuel "Hello world!"
          paramètre entrée ->  
            (bytearray[0x48, 0x65, 0x6c, 0x6c, 0x6f, 0x20, 0x77, 0x6f, 0x72, 0x6c, 0x64, 0x21], ' ') 
          affichage -> 72 101 108 108 111 32 119 111 114 108 100 33
   """
   for idx, octet in enumerate(tableOctet):
      if idx != len(tableOctet) - 1:
         print("%d%s" % (octet, separateur), end ='')
      else:    # évite d'afficher le séparateur après le dernier octet affiché
         print(octet)

def byte_afficherBytearrayAscii(tableOctet, separateur = ' '):
   """ Affiche le contenu d'un type bytearray (tableau d'octets) en code ASCII
       Pour éviter les erreurs, les codes supérieurs à 127 sont transformés en '?'
       Chaque octet est séparé par le séparateur passé en paramètre : '', ' ', '/' ...

       Exemple 1 : bytearray correspondant à chaine de caractères "0x1000FE134A"
          paramètre entrée -> (bytearray[0x10, 0x00, 0xFE, 0x13, 0x4A], ' ')
          affichage ->  \000 ?  J  
       Exemple 2 : bytearray contenant les codes ascii du message textuel "Hello world!"
          paramètre entrée ->  
            (bytearray[0x48, 0x65, 0x6c, 0x6c, 0x6f, 0x20, 0x77, 0x6f, 0x72, 0x6c, 0x64, 0x21], ' ') 
          affichage -> H e l l o   w o r l d !
   """
   # Remplace les codes non ASCII par le caractère '?'
   tableOctet2 = bytearray([])
   for octet in tableOctet:
      if octet <= 127:
         tableOctet2.append(octet)
      else:
         tableOctet2.append(ord('?'))  # ord() convertit caractère ascii en int
   
   for idx, octet in enumerate(tableOctet2.decode()):
      if idx != len(tableOctet) - 1:
         print("%s%s" % (octet, separateur), end ='')
      else:    # évite d'afficher le séparateur après le dernier octet affiché
         print(octet)
   print('')

# -----------  TEST des fonctions ---------------------------------------------
if __name__ == '__main__':
   print("********** Test fonctions de conversion de bytearray **********")

   # ---------- Entrée -> chaine de caractères correspondant à un message textuel
   print("Entrée -> chaine de caractères correspondant à un nombre hexadécimal")
   chaineCaract = "0x1000FE134A"
   #chaineCaract = "Hello world!"

   print("Nombre hexa sous forme de chaine de caractères : " + chaineCaract)
   
   tableOctet = byte_stringHexaToBytearray(chaineCaract)
   
   print("Conversion Nb hexa long en bytearray puis affichage brut : ", end = '')
   print(tableOctet)
   
   print("Affichage liste d'octets (bytearray) en hexadécimal : ", end ='')
   byte_afficherBytearrayHexa(tableOctet, ' ')
   
   print("Affichage liste d'octets (bytearray) en décimal     : ", end ='')
   byte_afficherBytearrayDecimal(tableOctet, ' ')
   
   print("Affichage liste d'octets (bytearray) en ASCII       : ", end ='')
   byte_afficherBytearrayAscii(tableOctet, ' ')

   # ---------- Entrée -> chaine de caractères correspondant à un message textuel
   print("Entrée -> chaine de caractères correspondant à un message textuel")
   #chaineCaract = "0x1000FE134A"
   chaineCaract = "Hello world!"

   print("Message textuel sous forme de chaine de caractères : " + chaineCaract)
   
   tableOctet = byte_stringTextToBytearray(chaineCaract)
   
   print("Conversion Nb hexa long en bytearray puis affichage brut : ", end = '')
   print(tableOctet)
   
   print("Affichage liste d'octets (bytearray) en hexadécimal : ", end ='')
   byte_afficherBytearrayHexa(tableOctet, ' ')
   
   print("Affichage liste d'octets (bytearray) en décimal     : ", end ='')
   byte_afficherBytearrayDecimal(tableOctet, ' ')
   
   print("Affichage liste d'octets (bytearray) en ASCII       : ", end ='')
   byte_afficherBytearrayAscii(tableOctet, ' ')

