#!/usr/bin/python3
# coding: utf-8
#this code runs on the xbee coordinator that is set to API mode 2
"""
Programme : xbeeTestEmission.py     version : 1.2
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

BAUD_RATE = 115200
ser = serial.Serial('COM6', BAUD_RATE, timeout = 1)

# ----- Configuration de la communication Zigbee -----
# demande au module xbee coordinateur de chercher l'adresse 16 bits du xbee à atteindre
destAddress16bit = bytearray([0xFF,0xFE])
# adresse 64 bits du module xbee à atteindre
destAddress64bit = bytearray([0x00,0x13,0xA2,0x00,0x40,0xD9,0x67,0xBC])
# Message texte à envoyer
#payload=b'Hello\n'
# liste d'octets à envoyer
payload=b'\x00\x01\x02\x80\xFE\xFF'
zb = ZigBee(ser)

#sends data to xbee address
def sendData(address, datatosend):
    zb.send('tx', dest_addr_long = address, dest_addr = destAddress16bit, data = datatosend)

#test data sending method
while True:
    try:
        sendData(destAddress64bit, payload)
        print("payload envoyé : ", end = '')
        print(payload)
        time.sleep(2)
    except KeyboardInterrupt:
        break

zb.halt()
ser.close()