#!/usr/bin/python3
# coding: utf-8
"""
Programme : XbeeGestion.py     version : 1.0
Auteur : H. Dugast
Date : 07-04-2017
Matériel utilisé : ordinateur sous windows (avec wing ide par exemple)
Fonctionnement programme :
Gère une communication zigBee 
https://github.com/HerveDugast/public_btssn_lasalle_nantes/tree/master/python/_prog_HD/zigbee
"""

import sys

class XbeeGestion():
   def __init__(self, port, baudRate, myAddress64, destAddress64, destAddress16):
      """ initialise l'objet :  port (COMx, avec x >= 3), vitesse de transmission uart 
          adresse 64 bits de ce module Xbee et du module à atteindre) """
      self.m_port = port  # COM3, COM4... ?
      self.m_baudRate = baudRate   # généralement 9600 ou 115200 bauds
      # mémorisation adresse 64 bits de ce module xbee dans un bytearray
      self.m_myAdress64 = conv_stringHexaToBytearray(myAddress64)
      # mémorisation adresse 64 bits du module xbee à atteindre
      self.m_destAdress64 = conv_stringHexaToBytearray(destAddress64)
      # mémorisation adresse 64 bits du module xbee à atteindre
      self.m_destAdress16 = conv_stringHexaToBytearray(destAddress16)
      
   def conv_stringHexaToBytearray(chaineCaract):
      """ Convertit une chaine de caractères contenant un nombre hexadécimal en un tableau d'octets
          Retour : tableau d'octet (type : bytearray)
          Exemple :    paramètre entrée -> chaineCaract = '0x1000FE4A'
                       retour -> bytearray[0x10, 0x00, 0xFE, 0x4A]
          """
      try:
         tableOctet = bytearray([])
         for i in range(0, len(chaineCaract), 2):
            octetHex = chaineCaract[i:i+2]
            if octetHex != "0x":
               tableOctet.append(int(octetHex, 16))
         return tableOctet
      except:
         print("Erreur ! Nombre hexadécimal ? ... " + str(sys.exc_info()[0]))
         return bytearray([])
      
   def conv_stringTextToBytearray(chaineCaract):
      """ Convertit une chaine de caractères contenant un texte en un tableau d'octets
          Retour : tableau d'octet (type : bytearray)
          Exemple :    paramètre entrée -> chaineCaract = 'Hello world'
                       retour -> bytearray[0x10, 0x00, 0xFE, 0x4A]
          """
      try:
         tableOctet = bytearray(chaineCaract.encode())
         return tableOctet
      except:
         print("Erreur ! Nombre hexadécimal ? ... " + str(sys.exc_info()[0]))
         return bytearray([])
      
   def afficherBytearrayHexa(tableOctet, separateur = ' '):
      """ Affiche le contenu d'un type bytearray (tableau d'octets) en hexadécimal
          Chaque octet est séparé par un séparateur : '', ' ', '/', ':' ...
          Exemple :    paramètre entrée -> (bytearray[0x10, 0x00, 0xFE, 0x4A], ' ') 
                       affichage -> 10 00 fe 4a  """
      for idx, octet in enumerate(tableOctet):
         if idx != len(tableOctet) - 1:
            print("%s%s" % ('{:02x}'.format(octet), separateur), end ='')
         else:    # évite d'afficher le séparateur après le dernier octet affiché
            print('{:02x}'.format(octet))
      
   def afficherBytearrayDecimal(tableOctet, separateur = ' '):
      """ Affiche le contenu d'un type bytearray (tableau d'octets) en décimal
          Chaque octet est séparé par un séparateur : '', ' ', '/', ':' ...
          Exemple :    paramètre entrée -> (bytearray[0x10, 0x00, 0xFE, 0x4A], ' ') 
                       affichage -> 16 0 254 74  """
      for idx, octet in enumerate(tableOctet):
         if idx != len(tableOctet) - 1:
            print("%d%s" % (octet, separateur), end ='')
         else:    # évite d'afficher le séparateur après le dernier octet affiché
            print(octet)
   
   def afficherBytearrayAscii(tableOctet, separateur = ' '):
      """ Affiche le contenu d'un type bytearray (tableau d'octets) en décimal
          Chaque octet est séparé par un séparateur : '', ' ', '/' ...
          Exemple :    paramètre entrée -> (bytearray[0x10, 0x00, 0xFE, 0x4A], ' ')
                       affichage -> 16 0 254 74  """
      for idx, octet in enumerate(tableOctet.decode()):
         if idx != len(tableOctet) - 1:
            print("%s%s" % (octet, separateur), end ='')
         else:    # évite d'afficher le séparateur après le dernier octet affiché
            print(octet)
      print('')   
   