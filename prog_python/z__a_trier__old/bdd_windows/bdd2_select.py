#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : bdd2_select.py     version : 1.0
Auteur : H. Dugast
Date : 31-03-2017
Matériel utilisé : carte raspberry pi ou exécution sous windows (avec wing ide par exemple)

Fonction programme :
Récupère et affiche les lignes retournées par une requête SQL de type SELECT.

Il faut commencer par installer un connecteur mysql-python :
   https://dev.mysql.com/doc/connector-python/en/connector-python-installation.html
"""

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
        cnx = mysql.connector.connect(host="217.128.90.45",
                                      user="dbformation_user",
                                      password="Btssn44",
                                      database="dbformation_test")
        return cnx
    except mysql.connector.Error as err:
        bddMessageError = err
    except:
        bddMessageError = "Erreur inattendue bdd_connecter() : " + str(sys.exc_info()[0])
    finally:
        if bddMessageError != "OK":
            print("Erreur connexion à bdd :\n" + str(bddMessageError))
            return bddMessageError
        return cnx

def bdd_deconnecter(cnx):
    """ Déconnexion de la base de données MySQL """
    cnx.close()

def sql_getResultatReqSelect(sqlQuery, *args):
    """ Exécute une requête de type SELECT
        maj variable globale bddMessageError : "OK" ou message d'erreur s'il y a une erreur
        Paramètres : sqlQuery -> requête SQL (format chaine caractères) de type SELECT
                     *arg  -> liste de valeurs (facultatif) des variables contenues dans la requête
                              après la clause WHERE
        Retour : liste -> résultat de la requête ou liste vide si erreur """
    
    global bddMessageError
    try:
        cnx = bdd_connecter()
        if bddMessageError == "OK":
            cur = cnx.cursor()
            cur.execute(sqlQuery, args)
            # Copie du résultat dans une séquence
            resultSelect = []
            for row in cur.fetchall() :
                resultSelect.append(row)    # ajout de chaque ligne dans la séquence
            cur.close()
            bdd_deconnecter(cnx)     # déconnexion de la base de données
    except mysql.connector.Error as err:
        bddMessageError = err
    except:
        bddMessageError = "Erreur inattendue sql_reqExecuterSelect() : " + str(sys.exc_info()[0])
    finally:
        if bddMessageError != "OK":
            resultSelect = []
            print("Erreur exécution requête SQL :\n" + str(bddMessageError))
        return resultSelect
    
def sql_getNomChampTable(nomTable):
    """ Exécute une requête de type SELECT puis retourne le nom des champs de la table demandée
        maj variable globale bddMessageError : "OK" ou message d'erreur s'il y a une erreur
        Retour : nomTable -> liste contenant les noms des champs ou liste vide si erreur"""
    global bddMessageError
    try:
        cnx = bdd_connecter()
        if bddMessageError == "OK":
            cur = cnx.cursor()
            cur.execute("SELECT * FROM %s LIMIT 1" % nomTable)
            # Copie du résultat dans une séquence
            cur.fetchall()
            resultSelect = []
            for idx, nom in enumerate(cur._description):
                champ = str(nom[0])
                resultSelect.append(champ)
            cur.close()
            bdd_deconnecter(cnx)     # déconnexion de la base de données
    except mysql.connector.Error as err:
        bddMessageError = err
    except:
        bddMessageError = "Erreur inattendue sql_getNomChampTable() : " + str(sys.exc_info()[0])
    finally:
        if bddMessageError != "OK":
            resultSelect = []
            print("Erreur exécution requête SQL :\n" + str(bddMessageError))
        return resultSelect

def sql_afficherResultatReqSelect(sqlQuery, *args):
    """ Exécute et affiche le résultat d'une requête SELECT
        maj variable globale bddMessageError : "OK" ou message d'erreur s'il y a une erreur
        Paramètres : sqlQuery -> requête SQL (format chaine caractères) de type SELECT
                     *arg  -> liste de valeurs (facultatif) des variables contenues dans la requête
                              après la clause WHERE
        Retour : nombre de lignes affichées par la requête SELECT """
    
    resultSelect = sql_getResultatReqSelect(sqlQuery, *args) 
    if bddMessageError == "OK":
        for row in resultSelect:
            print(row)
    return len(resultSelect)


#----------------------------------------------------------------------------------------
#  PROGRAMME PRINCIPAL
#----------------------------------------------------------------------------------------

# Affichage du nom des champs d'une table à partir du connecteur mysql-python
nomTable = "enseignant"
print("Récupération du nom des champs de la table " + nomTable + " :")
resultSelect = sql_getNomChampTable(nomTable)
print(resultSelect)
print("--------------------------------------------------------------------------")

# Affichage résultat requête SELECT
sqlQuery = "SELECT * FROM enseignant"
print("Résultat requête suivante :")
print("\t" + sqlQuery)
nbLigneAffich = sql_afficherResultatReqSelect(sqlQuery)
print("\nNombre de lignes retourné par la requête : " + str(nbLigneAffich))
print("--------------------------------------------------------------------------")

# Affichage de la valeur d'un seul champ d'un enregistrement
numeroEnseignant = 56
sqlQuery = "SELECT nom FROM enseignant " \
    "WHERE numeroEnseignant = '%s' "
resultSelect = sql_getResultatReqSelect(sqlQuery, numeroEnseignant)
print("Valeur du champ retournée par la requête suivante :")
print("\t" + sqlQuery + "\n\t\tavec '%s' = ", str(numeroEnseignant))
print(resultSelect[0][0])
print("--------------------------------------------------------------------------")

# Affichage de la valeur de plusieurs champs d'un enregistrement
nomEnseignant = "Didier"
sqlQuery = "SELECT numeroEnseignant, grade  FROM enseignant " \
    "WHERE nom LIKE %s "
resultSelect = sql_getResultatReqSelect(sqlQuery, nomEnseignant)
print("Valeurs des champs retournées par la requête suivante :")
print("\t" + sqlQuery + "\n\t\tavec %s = '" + nomEnseignant +"'")
print(resultSelect)
print("--------------------------------------------------------------------------")

# Affichage du résultat de la requête suivant plusieurs critères
grade = "Professeur"
salaireMin = 1000
sqlQuery = "SELECT * FROM enseignant " \
    "WHERE grade LIKE %s AND salaire >= '%s' "
resultSelect = sql_getResultatReqSelect(sqlQuery, grade, salaireMin)
print("Valeurs des champs retournées par la requête suivante :")
print("\t" + sqlQuery + "\n\t\tavec %s = '" + grade +"' et '%s' = " + str(salaireMin))
for element in resultSelect:
    print(element)
print("--------------------------------------------------------------------------")
# Affichage du nom des champs d'une table (méthode 2)
nomTable = "enseignant"
print("Récupération du nom des champs de la table " + nomTable + " (méthode 2):")
sqlQuery = "SELECT COLUMN_NAME FROM information_schema.COLUMNS " \
    "WHERE TABLE_NAME LIKE %s"
print("\t" + sqlQuery + "\n\t\tavec %s = '" + nomTable + "'")
sql_afficherResultatReqSelect(sqlQuery, nomTable)