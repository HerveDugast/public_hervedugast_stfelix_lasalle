#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : bdd1_connect.py     version : 1.0
Auteur : H. Dugast
Date : 27-03-2017
Matériel utilisé : carte raspberry pi ou exécution sous windows (avec wing ide par exemple)
Fonctionnement programme :
Se connecte à une base de données distante avec le port standard, puis se déconnecte.
Il faut commencer par installer un connecteur mysql-python :
   https://dev.mysql.com/doc/connector-python/en/connector-python-installation.html
"""

import sys
import mysql.connector
import time

global bddMessageError

def bdd_connecter():
    """ Connexion à une base de données MySQL
        maj variable globale bddMessageError : "OK" ou message d'erreur s'il y a une erreur
        Retour : objet connecteur bdd """
    global bddMessageError
    bddMessageError = "OK"
    try:
        # ATTENTION ! host -> mettre adresse IP du serveur de base de données de la section
        # ATTENTION ! password -> mettre même mot de passe que compte windows local installateur     
        cnx = mysql.connector.connect(host = "adresse_ip_srv_bdd_section",
                                      user = "dbformation_user",
                                      password = "mot_de_passe_installateur",
                                      database = "dbformation_test")
    except mysql.connector.Error as err:
        bddMessageError = err
    except:
        bddMessageError = "Erreur inattendue bdd_connecter() : " + str(sys.exc_info()[0])
    finally:
        if bddMessageError != "OK":
            print("Erreur connexion à bdd :\n" + str(bddMessageError))
            return bddMessageError
        return cnx

def bdd_déconnecter(cnx):
    """ Déconnexion de la base de données MySQL """
    cnx.close()

#----------------------------------------------------------------------------------------
#  PROGRAMME PRINCIPAL
#----------------------------------------------------------------------------------------

print("Tentative de connexion à la base de données")
print("Remarque : En cas d'échec, la réponse du serveur de bdd peut tarder\n" \
      "           car elle dépend du timeout configuré sur ce serveur !\n")
cnx = bdd_connecter()
if bddMessageError == "OK":
    print("Connexion à la base de données réussie :")
    print("   Hôte : " + cnx._host)
    print("   Port : " + str(cnx._port))
    print("   Base de données : " + cnx._database)
    print("   Utilisateur : " + cnx._user)
    print("   Mot de passe : " + cnx._password)
    time.sleep(2)
    bdd_déconnecter(cnx)     # déconnexion de la base de données
    print("Déconnexion de la base de données réussie")
else:
    print("Echec connexion à base de données")
