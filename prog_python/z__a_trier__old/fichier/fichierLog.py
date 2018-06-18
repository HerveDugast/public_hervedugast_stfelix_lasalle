#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : fichierLog.py     version : 1.0
Auteur : H. Dugast
Date : 06-05-2017
Matériel utilisé :  ordinateur sous windows (avec wing ide par exemple)
Fonction :
Ecrit des messages horodatés dans un fichier log avec le niveau d'importance :
CRITICAL > ERROR > WARNING > INFO > DEBUG

Source : http://www.planet-libre.org/index.php?post_id=9718
Lire la documentation à l'URL indiquée pour avoir plus de précisions

Exemple d'exécution pour ce programme :
--- Contenu fichier prog.log ---
06-05-2017 23:10:47 :: WARNING :: Testing foo

--- Contenu fichier debug.log ---
06/05/2017 23:58:33 INFO - Mon programme demarre
06/05/2017 23:58:35 WARNING - Oh, quelque chose ce passe !
06/05/2017 23:58:35 INFO - fin du prog
"""

import logging
import time

logging.basicConfig(
   filename='prog.log',
   level=logging.INFO,
   format='%(asctime)s %(levelname)s - %(message)s',
   datefmt='%d/%m/%Y %H:%M:%S',
)

# Attention aux accents, il faut passer par des handlers pour spécifier l'encodage UTF-8
logging.info('Mon programme demarre')
time.sleep(2)
logging.warning('Oh, quelque chose ce passe !')
logging.info('fin du prog')