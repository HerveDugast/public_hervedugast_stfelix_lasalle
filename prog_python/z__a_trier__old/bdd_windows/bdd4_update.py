#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : bdd4_update.py     version : 1.0
Auteur : H. Dugast
Date : 31-03-2017
Matériel utilisé : carte raspberry pi ou exécution sous windows (avec wing ide par exemple)

Fonction programme :
Insère un enregistrement dans une base de données à l'aide d'une requête SQL de type INSERT,
puis change (met à jour) ses valeurs à l'aide d'une requête UPDATE.

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
            print("Erreur exécution sql_reqExecuterSelect :\n" + str(bddMessageError))
        return resultSelect

def sql_reqExecuterInsertUpdateDelete(sqlQuery, *args):
    """ Exécute une requête SQL de type INSERT/UPDATE/DELETE, insère 1 à plusieurs données dans la 
        bdd MySQL
        maj variable globale bddMessageError : "OK" ou message d'erreur s'il y a une erreur
        Paramètres : sqlQuery -> requête SQL (format chaine caractères) de type SELECT
                     *arg  -> liste de valeurs (facultatif) des variables contenues dans la requête
                              après la clause WHERE """
    global bddMessageError
    try:
        cnx = bdd_connecter()
        if bddMessageError == "OK":
            cur = cnx.cursor()
            cur.execute(sqlQuery, args)
            cnx.commit()
            cur.close()
            bdd_deconnecter(cnx)     # déconnexion de la base de données
    except mysql.connector.Error as err:
        bddMessageError = err
    except:
        bddMessageError = "Erreur inattendue sql_reqExecuterInsertUpdateDelete() : " \
            + str(sys.exc_info()[0])
    finally:
        if bddMessageError != "OK":
            print("Erreur exécution sql_reqExecuterInsertUpdateDelete :\n" + str(bddMessageError))
    
def sql_getNomChampTable(nomTable):
    """ Copie les noms de champs de la table demandée dans une liste
        maj variable globale bddMessageError : "OK" ou message d'erreur s'il y a une erreur
        Paramètre : nomTable -> nom de la table dont on veut récupérer le nom des champs
        Retour : listeNomTable -> liste contenant les noms des champs ou liste vide si erreur"""
    global bddMessageError
    try:
        cnx = bdd_connecter()
        if bddMessageError == "OK":
            cur = cnx.cursor()
            cur.execute("SELECT * FROM %s LIMIT 1" % nomTable)
            # Copie du résultat dans une séquence
            cur.fetchall()
            listeNomTable = []
            for idx, nom in enumerate(cur._description):
                champ = str(nom[0])
                listeNomTable.append(champ)
            cur.close()
            bdd_deconnecter(cnx)     # déconnexion de la base de données
    except mysql.connector.Error as err:
        bddMessageError = err
    except:
        bddMessageError = "Erreur inattendue sql_getNomChampTable() : " + str(sys.exc_info()[0])
    finally:
        if bddMessageError != "OK":
            listeNomTable = []
            print("Erreur exécution sql_getNomChampTable :\n" + str(bddMessageError))
        return listeNomTable

def sql_afficherResultatReqSelect(sqlQuery, *args):
    """ Affiche dans l'interpréteur le résultat d'une requête SELECT après l'avoir exécuté
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
# --- Insertion d'un enregistrement dans la bdd ---
# Ajout du professeur Titi, de numéro 950, avec un salaire de 1000€
numeroEnseignant = 950
nom = "Titi"
grade = "Professeur"
salaire = 1000
# Remarque : à la 2è exécution de ce programme, une erreur se produira si on ne modifie les données
# à insérer... Erreur exécution req INSERT : 1062 (23000): Duplicate entry '950' for key 'PRIMARY'
sqlQuery = "INSERT INTO enseignant (numeroEnseignant, nom, grade, salaire) "  \
    "VALUES ('%s', %s, %s, '%s')"
print("Insertion de données avec la requête suivante :")
print("\t" + sqlQuery + "\n\t\tavec '%s' = ", str(numeroEnseignant), "   %s = ", nom,
      "   %s = ", grade, "   '%s' = ", salaire)
sql_reqExecuterInsertUpdateDelete(sqlQuery, numeroEnseignant, nom, grade, salaire)
print("--------------------------------------------------------------------------")

# Affichage contenu table après insertion de données
print("Affichage de l'enregistrement précédemment inséré avec la requête suivante :")
sqlQuery = "SELECT * FROM enseignant WHERE numeroEnseignant = '%s'"
print("\t" + sqlQuery + "\n\t\tavec '%s' = " + str(numeroEnseignant))
sql_afficherResultatReqSelect(sqlQuery, numeroEnseignant)
print("--------------------------------------------------------------------------")

# --- Modification d'un enregistrement ---
# Titi est en fait un Assistant et non un professeur et gagne 900€
grade = "Assistant"
salaire = 900
sqlQuery = "UPDATE enseignant SET grade = %s, salaire = '%s' WHERE numeroEnseignant = '%s'"
print("Modification de données avec la requête suivante :")
print("\t" + sqlQuery + "\n\t\tavec %s = ", grade, "   '%s' = ", salaire,
      "   '%s' = ", numeroEnseignant)
sql_reqExecuterInsertUpdateDelete(sqlQuery, grade, salaire, numeroEnseignant)
print("--------------------------------------------------------------------------")

# Affichage contenu table après modification de données
print("Affichage de l'enregistrement modifié avec la requête suivante :")
sqlQuery = "SELECT * FROM enseignant WHERE numeroEnseignant = '%s'"
print("\t" + sqlQuery + "\n\t\tavec '%s' = " + str(numeroEnseignant))
sql_afficherResultatReqSelect(sqlQuery, numeroEnseignant)
print("--------------------------------------------------------------------------")