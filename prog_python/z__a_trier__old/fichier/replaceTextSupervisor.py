#!/usr/bin/python3
# coding: utf-8
"""
Programme : replaceTextSupervisor.py     version : 1.0
Auteur : H. Dugast
Date : 01-05-2017
Matériel utilisé : ordinateur sous windows (avec wing ide par exemple)
Fonctionnement programme :
Remplace des chaines de texte d'un fichier par d'autres dans un autre fichier
"""

print("Début recherche/remplacement")

f1 = open('D:/_githubHd/private_hd/miniprojet_supervisor/bdd_dbsn/supervisor_v10.sql').read()
f2 = open('D:/_githubHd/private_hd/miniprojet_supervisor/bdd_dbsn/supervisorNew_v10.sql', 'w')

replacements = {'id_local':'local_id', 
                'id_type_capteur':'type_capteur_id', 
                'id_emplacement':'emplacement_id', 
                'id_systeme_embarque':'systeme_embarque_id',
                'id_etat_capteur':'etat_capteur_id',
                'id_capteur':'capteur_id',
                'id_evenement':'evenement_id'}

for oldChaine in replacements.keys():
   f1 = f1.replace(oldChaine, replacements[oldChaine])
f2.write(f1)
f2.close

print("FIN recherche/remplacement")
