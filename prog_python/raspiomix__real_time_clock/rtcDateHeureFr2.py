#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : rtcDateHeureFr2.py       version 1.1
Date : 30-01-2018
Auteur : Hervé Dugast
Source : http://www.python-exemplary.com    (timer)

Matériel utilisé : raspberry pi 3, carte raspiO'Mix+

Fonctionnement programme :
  affiche la date et l'heure de l'horloge temps réel de la raspiO'Mix au format français

------- affichage console ----------------
30-01-2018 17:21:12
------------------------------------------

Remarque
---------------------------------------------------------------------------------------------------
Si vous avez l'erreur : "OSError: [Errno 16] Device or resource busy"
Exécutez la commande shell suivante : $ sudo rmmod rtc_ds1307
Cela décharge le pilote rtc_ds1307 permettant à l'OS linux d'accéder à l'horloge temps réel.
La ressource est alors libérée. Le programme doit maintenant s'exécuter sans erreur.

Explications :
L'horloge temps réel (RTC) se trouve sur la carte raspiomix+. C'est une puce électronique, une
ressource hardware à laquelle on accède en utilisant le bus i2c. Un programme python ne peut
pas accéder à une ressource harware si celle-ci est utilisée par le système d'exploitation.
Tapez la commande shell :   $ i2cdetect -y 1
   - si 0x68 = 68 alors le périphérique RTC est dispo, un programme python peut l'utiliser
   - si 0x68 = UU alors le périphérique RTC est utilisé par l'OS linux. Il faut décharger 
                  le pilote qui communique avec la ressource pour pouvoir l'utiliser.
Remarque : Voici la commande pour charger à nouveau le pilote de la ressource RTC dans l'OS Linux
$ sudo modprobe rtc_ds1307
"""

# Ajout du chemin d'accès au dossier parent du projet dans le python PATH.
# Cela permet d'accéder aux modules se situant dans les dossiers adjacents.
import python_path

# Ajout des bibliothèques
from library.RTC_DS1307_HD.RTC_DS1307_HD import *

rtc = RTC()

# Affichage de la date et de l'heure
print(rtc.getDateStrFr())
