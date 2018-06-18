#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : bdd3_insert.py     version : 1.0
Auteur : H. Dugast
Date : 31-03-2017
Matériel utilisé : carte raspberry pi ou exécution sous windows (avec wing ide par exemple)

Fonction programme :
Insère des enregistrements dans une base de données à l'aide de requêtes SQL de type INSERT.

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
            print("Erreur exécution requête SQL :\n" + str(bddMessageError))
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
# --- Insertion de données sans clé étrangère ---
# Affichage contenu table avant insertion de données
print("Contenu table 'etudiant' avant insertion données :")
sqlQuery = "SELECT * FROM etudiant"
nbLigneAffich = sql_afficherResultatReqSelect(sqlQuery)
print("\nNombre de lignes retourné par la requête : " + str(nbLigneAffich))
print("--------------------------------------------------------------------------")

# Insertion de données dans une bdd
numeroEtudiant = 900
nom = "toto"
adresse = "Paris"
# Remarque : à la 2è exécution de ce programme, une erreur se produira si on ne modifie les données
# à insérer... Erreur exécution req INSERT : 1062 (23000): Duplicate entry '900' for key 'PRIMARY'
sqlQuery = "INSERT INTO etudiant (numeroEtudiant, nom, adresse) VALUES ('%s', %s, %s)"
print("Insertion de données (sans clé étrangère) avec la requête suivante :")
print("\t" + sqlQuery + "\n\t\tavec '%s' = ", str(numeroEtudiant), "   %s = ", nom,
      "   %s = ", adresse)
sql_reqExecuterInsertUpdateDelete(sqlQuery, numeroEtudiant, nom, adresse)
print("--------------------------------------------------------------------------")

# Affichage contenu table après insertion de données
print("Contenu table 'etudiant' après insertion données :")
sqlQuery = "SELECT * FROM etudiant"
nbLigneAffich = sql_afficherResultatReqSelect(sqlQuery)
print("\nNombre de lignes retourné par la requête : " + str(nbLigneAffich))
print("--------------------------------------------------------------------------")
print("--------------------------------------------------------------------------")
print("--------------------------------------------------------------------------")

# --- Insertion de données dont une clé étrangère ---
# Affichage contenu table avant insertion de données
print("Contenu table 'tbmodule' avant insertion données :")
sqlQuery = "SELECT * FROM tbmodule"
nbLigneAffich = sql_afficherResultatReqSelect(sqlQuery)
print("\nNombre de lignes retourné par la requête : " + str(nbLigneAffich))
print("--------------------------------------------------------------------------")

# Insertion de données dans une bdd
# Récupération de la clé étrangère numeroEnseignant
# On considère que le professeur Didier est unique
nomEnseignant = "Didier"
grade = "Professeur"
sqlQuery = "SELECT numeroEnseignant FROM enseignant "  \
    "WHERE nom LIKE %s AND grade LIKE %s"
resultSelect = sql_getResultatReqSelect(sqlQuery, nomEnseignant, grade)
fk_tbmodule_numeroEnseignant = resultSelect[0][0]
numeroModule = 990
titre = "Informatique"
# Remarque : à la 2è exécution de ce programme, une erreur se produira si on ne modifie les données
# à insérer... Erreur exécution req INSERT : 1062 (23000): Duplicate entry '990' for key 'PRIMARY'
sqlQuery = "INSERT INTO tbmodule (numeroModule, titre, numeroEnseignant) " \
    "VALUES ('%s', %s, '%s')"
print("Insertion de données avec la requête suivante :")
print("\t" + sqlQuery + "\n\t\tavec '%s' = ", str(numeroModule), "   %s = ", titre,
      "   '%s' = ", fk_tbmodule_numeroEnseignant)
sql_reqExecuterInsertUpdateDelete(sqlQuery, numeroModule, titre, fk_tbmodule_numeroEnseignant)
print("--------------------------------------------------------------------------")

# Affichage contenu table après insertion de données
print("Contenu table 'tbmodule' avant insertion données :")
sqlQuery = "SELECT * FROM tbmodule"
nbLigneAffich = sql_afficherResultatReqSelect(sqlQuery)
print("\nNombre de lignes retourné par la requête : " + str(nbLigneAffich))


