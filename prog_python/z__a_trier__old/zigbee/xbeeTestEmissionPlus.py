#!/usr/bin/python3
# coding: utf-8
#this code runs on the xbee coordinator that is set to API mode 2
"""
Programme : xbeeTestEmissionPlus.py     version : 1.1
Auteur : H. Dugast
Date : 24-04-2017
Matériel utilisé : ordinateur sous windows (avec wing ide par exemple)
Fonctionnement programme :
Envoie des données, chaine de caractères ou octets, vers une carte arduino Mega2560, par une
liaison zigbee. Les modules XBee utilisés sont des séries 2, fonctionnant en API mode 2.
Le module xbee connecté au PC est configuré en coordinateur API. 
https://github.com/HerveDugast/public_btssn_lasalle_nantes/tree/master/python/_prog_HD/zigbee

Pour tester ce programme, on peut utiliser le programme zbReception.ino sur la carte arduino
Mega2560. Le module xbee connecté à la carte arduino est configuré en routeur API.
https://github.com/HerveDugast/public_btssn_lasalle_nantes/tree/master/arduino/_prog_HD/zigbee

***** Configuration Module XBee XB24-ZB "PC" avec XCTU (exemple) **********
Name : coord1998_API
Product family : XB24-ZB
Firmware : Zigbee Coordinator API version 21A7
PAN ID : 1998        SH : 0013A200        BD : 115200
SC : FFFF            SL : 40E96396        NB : No Parity
OI : 4E2D            MY : -               SB : One stop bit
CH : 0C              DH : 0013A200        AP : 2
                     DL : 40D967BC        D7 : Disable
                     NI : coord1998_API   D6 : disable

***** Configuration Module XBee XB24-ZB "arduino" avec XCTU (exemple) **********
Name : rout1998_API
Product family : XB24-ZB
Firmware : Zigbee Router API version 23A7
PAN ID : 1998        SH : 0013A200        BD : 115200
SC : FFFF            SL : 40D967BC        NB : No Parity
OI : 4E2D            MY : -               SB : One stop bit
CH : 0C              DH : 00000000        AP : 2
JV : 01              DL : 00000000        D7 : Disable
JN : 01              NI : rout1998_API    D6 : disable
"""

import serial
from xbee import ZigBee
from xbee.helpers.dispatch import Dispatch
import time
from datetime import datetime

# permet d'importer des modules situés dans un dossier adjacent
import sys
sys.path.append('../') # ajoute le chemin du dossier parent dans le path du import
from bytearrayTest.bytearrayConversion import *

# ----- Configuration de la communication Zigbee -----
# demande au module xbee coordinateur de chercher l'adresse 16 bits du xbee à atteindre
destAddress16bitStr = "0xFFFE"  
# adresse 64 bits du module xbee à atteindre
destAddress64bitStr = "0x0013a20040d967bc"
# octets à envoyer sous forme d'une chaine
dataHexStr = "0x1000FE134A"
# message texte à envoyer
dataTxtStr = "Hello"

BAUD_RATE = 115200
ser = serial.Serial('COM6', BAUD_RATE, timeout = 1)
zb = ZigBee(ser)

# transforme la chaine de caractères contenant l'adresse 16 bits en bytearray (liste d'octets)
destAddress16bit = byte_stringHexaToBytearray(destAddress16bitStr)
# transforme la chaine de caractères contenant l'adresse 64 bits en bytearray (liste d'octets)
destAddress64bit = byte_stringHexaToBytearray(destAddress64bitStr)

#sends data to xbee address
def sendData(address, datatosend):
    """ Envoie les données à transmettre par liaison xbee au module xbee indiqué """
    zb.send('tx', dest_addr_long = address, dest_addr = destAddress16bit, data = datatosend)

def dataPreparer():
    """ Prépare les données à transmettre
           Dans notre exemple, payload : concaténation de l'heure (HH MM SS), d'une suite d'octets et 
           d'un message texte
        Retour : tableau d'octet (type : bytearray) 
        Exemple avec 15:39:27, dataHexStr = "0x1000FE134A" et dataTxtStr = "Hello" (message texte)
           Payload envoyé (hexa) : 0f 27 1b 10 00 fe 13 4a 48 65 6c 6c 6f
           Payload envoyé (dec)  : 15 39 27 16 0 254 19 74 72 101 108 108 111
           Payload envoyé (ascii):  '   \000 ?  J H e l l o
    """
    dateCourante = datetime.now()
    #dateCourante = datetime(2017, 4, 24, 15, 39, 27)
    
    # transforme la chaine de caractères contenant la liste d'octets en bytearray (liste d'octets)
    dataHex = byte_stringHexaToBytearray(dataHexStr)
    # transforme la chaine de caractères contenant le message texte en bytearray (liste d'octets)
    dataTxt = byte_stringTextToBytearray(dataTxtStr)    

    # création du payload, les données à transmettre doivent être stockées dans un type bytearray
    payload = bytearray([])
    # ajout de l'heure courante
    payload.append(dateCourante.hour)
    payload.append(dateCourante.minute)
    payload.append(dateCourante.second)
    # ajout de la liste d'octets
    for octet in dataHex:
        payload.append(octet)
    # ajout du message texte
    for octet in dataTxt:
        payload.append(octet)
    return payload

def infoAfficher():
    """ Affiche l'adresse 64 bits du module XBee de destination et le payload à envoyer
    """
    print("Module XBee adresse 64 bits destination (hexa): ", end = '')
    byte_afficherBytearrayHexa(destAddress64bit)
    print("Payload envoyé (hexa) : ", end = '')
    byte_afficherBytearrayHexa(payload)
    print("Payload envoyé (dec)  : ", end = '')
    byte_afficherBytearrayDecimal(payload)
    print("Payload envoyé (ascii): ", end = '')
    byte_afficherBytearrayAscii(payload)

#test data sending method
while True:
    try:
        payload = dataPreparer()
        infoAfficher()
        sendData(destAddress64bit, payload)
        time.sleep(2)
    except KeyboardInterrupt:
        break
zb.halt()
ser.close()