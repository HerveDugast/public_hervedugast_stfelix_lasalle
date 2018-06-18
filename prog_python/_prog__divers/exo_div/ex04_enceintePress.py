#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : ex04_enceintePress.py     version : 1.0
Auteur : H. Dugast
Source : http://hebergement.u-psud.fr/iut-orsay/Pedagogie/MPHY/Python/exercices-python3.pdf
Date : 06-05-2017

Fonction :
On désire sécuriser une enceinte pressurisée.
On se fixe une pression seuil et un volume seuil : pSeuil = 2.3, vSeuil = 7.41.
On demande de saisir la pression et le volume courant de l’enceinte et d’écrire un script
qui simule le comportement suivant :
– si le volume et la pression sont supérieurs aux seuils : arrêt immédiat ;
– si seule la pression est supérieure à la pression seuil : demander d’augmenter le volume de l’enceinte ;
– si seul le volume est supérieur au volume seuil : demander de diminuer le volume
de l’enceinte ;
– sinon déclarer que « tout va bien ».
Ce comportement sera implémenté par une alternative multiple.

Exemple d'exécution :
Seuil pression : 2.3 	Seuil volume : 7.41 

Pression courante = 5
Volume courant = 10
	*** Stopper ***
   
Pression courante = 3
Volume courant = 5
	 *** Augmenter le volume ***
    
Pression courante = 2
Volume courant = 10
	 *** Diminuer le volume ***

Pression courante = 2
Volume courant = 5
	 Tout va bien !
"""
p_seuil = 2.3
v_seuil = 7.41
print("Seuil pression :", p_seuil, "\tSeuil volume :", v_seuil, "\n")
pression = float(input("Pression courante = "))
volume = float(input("Volume courant = "))
if (pression > p_seuil) and (volume > v_seuil):
   print("\t*** Stopper ***")
elif pression > p_seuil:
   print("\t *** Augmenter le volume ***")
elif volume > v_seuil:
   print("\t *** Diminuer le volume ***")
else:
   print("\t Tout va bien !")