#!/usr/bin/python3
# coding: utf-8
#this code runs on the xbee router that is set to API mode 2
"""
Programme : xbeeTestReception.py     version : 1.1
Auteur : H. Dugast
Date : 24-04-2017
Matériel utilisé : ordinateur sous windows (avec wing ide par exemple)
Fonctionnement programme :
Réceptionne puis affiche les données reçues par la liaison zigbee. Les modules XBee utilisés sont 
des séries 2, fonctionnant en API mode 2. Le module xbee connecté au PC est configuré en routeur
API. 
https://github.com/HerveDugast/public_btssn_lasalle_nantes/tree/master/python/_prog_HD/zigbee
ATTENTION ! L'instruction zb.wait_read_frame() est bloquante

Pour tester ce programme, on peut utiliser le programme zbEmission.ino sur la carte arduino
Mega2560. Le module xbee connecté à la carte arduino est configuré en coordinateur API.
https://github.com/HerveDugast/public_btssn_lasalle_nantes/tree/master/arduino/_prog_HD/zigbee

***** Configuration Module XBee XB24-ZB "PC" avec XCTU (exemple) **********
Name : rout1998_API
Product family : XB24-ZB
Firmware : Zigbee Router API version 23A7
PAN ID : 1998        SH : 0013A200        BD : 115200
SC : FFFF            SL : 40D967BC        NB : No Parity
OI : 4E2D            MY : -               SB : One stop bit
CH : 0C              DH : 00000000        AP : 2
JV : 01              DL : 00000000        D7 : Disable
JN : 01              NI : rout1998_API    D6 : disable

***** Configuration Module XBee XB24-ZB "arduino" avec XCTU (exemple) **********
Name : coord1998_API
Product family : XB24-ZB
Firmware : Zigbee Coordinator API version 21A7
PAN ID : 1998        SH : 0013A200        BD : 115200
SC : FFFF            SL : 40E96396        NB : No Parity
OI : 4E2D            MY : -               SB : One stop bit
CH : 0C              DH : 0013A200        AP : 2
                     DL : 40D967BC        D7 : Disable
                     NI : coord1998_API   D6 : disable
"""

#import config
import serial
from xbee import ZigBee
import time
# permet d'importer des modules situés dans un dossier adjacent
import sys
sys.path.append('../') # ajoute le chemin du dossier parent dans le path du import
from bytearrayTest.bytearrayConversion import *

# permet d'importer des modules situés dans un dossier adjacent
import sys
sys.path.append('../') # ajoute le chemin du dossier parent dans le path du import
from bytearrayTest.bytearrayConversion import *

BAUD_RATE = 115200
ser = serial.Serial('COM6', BAUD_RATE, timeout = 1)
zb = ZigBee(ser, escaped = True)
import pprint
pprint.pprint(zb.api_responses)

def infoAfficher(data):
    print("type trame, id : ", end ='')
    print(data['id'])
    print("Module XBee adresse source 64 bits : ", end ='')
    byte_afficherBytearrayHexa(data['source_addr_long'])
    print("Module XBee adresse source 16 bits : ", end ='')
    byte_afficherBytearrayHexa(data['source_addr'])

    print("payload reçu (hex)   : ", end ='')
    byte_afficherBytearrayHexa(data['rf_data'])
    print("payload reçu (hex)   : ", end ='')
    byte_afficherBytearrayDecimal(data['rf_data'])
    print("payload reçu (ascii) : ", end ='')
    byte_afficherBytearrayAscii(data['rf_data'])

    
while True:
    try:
        data = zb.wait_read_frame()
        pprint.pprint(data)
        print('')
        infoAfficher(data)
    except KeyboardInterrupt:
        break
zb.halt()
ser.close()