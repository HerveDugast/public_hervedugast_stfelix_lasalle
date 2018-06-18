#!/usr/bin/python3.4
# coding: utf-8

"""
Programme : liste_fonction.py       version 1.0
Date : 27-11-2017
Auteur : Hervé Dugast
Source : http://sametmax.com/un-gros-guide-bien-gras-sur-les-tests-unitaires-en-python-partie-3/

Matériel utilisé : raspberry pi 3

"""

def get(lst, index, default=None):
    """
        Retourne l'élément de `lst` situé à `index`.
 
        Si aucun élément ne se trouve à `index`,
        retourne la valeur par défaut.
    """
    try:
        return lst[index]
    except IndexError:
        return default
    
