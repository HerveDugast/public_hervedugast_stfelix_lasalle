#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : bddmysql_test.py     version : 1.1
Auteur : H. Dugast
Date : 04-04-2017
Matériel utilisé : carte raspberry pi ou exécution sous windows (avec wing ide par exemple)
Fonctionnement programme :
Test de la classe Bddmysql.py
- récupérer les résultats d'une requête de type SELECT dans une liste
- insérer, modifier ou supprimer des données dans une table
- afficher le résultat d'une requête de type SELECT
- récupérer le nom des champs d'une table

Il faut commencer par installer un connecteur mysql-python :
   https://dev.mysql.com/doc/connector-python/en/connector-python-installation.html
"""

from Bddmysql.Bddmysql import *
import sys
import mysql.connector
import time

#----------------------------------------------------------------------------------------
#  PROGRAMME PRINCIPAL
#----------------------------------------------------------------------------------------

# Création d'un objet base de données qui mémorisera les paramètres de connexion et permettra
# d'accéder à des méthodes bien pratiques pour manipuler les base de données.
# ATTENTION ! host -> mettre adresse IP du serveur de base de données de la section
# ATTENTION ! password -> mettre même mot de passe que compte windows local installateur     
host = "adresse_ip_srv_bdd_section"
port = 3306
user = "dbformation_user"
password = "mot_de_passe_installateur"
database = "dbformation_test"
errorMsg = "OK"

print("********** Test classe Bddmysql.py **********\n")
# ---------- Test de connexion ----------
print('---------- Test de connexion à la base de données ----------')
try:
   bdd = Bddmysql(host, port, user, password, database)
   bdd.afficherAttributDebug()
except NameError as err:
   errorMsg = "Erreur 'NameError', pb importation module Bddmysql.py : " + str(err) + "\n"
   print(errorMsg)
   print("---------- Fin des tests à cause de l'erreur !!! ----------")

if errorMsg == "OK":
   # Les lignes ci-dessous ne sont là que pour montrer le principe d'une connexion à une base
   # de données. Elles seront inutiles dans la majorité des cas car elles sont incluses dans les
   # méthodes de l'objet. D'ailleurs, ces méthodes commencent par un caractère soulignement pour 
   # indiquer qu'elles doivent être utilisées comme un type privé (les variables et méthodes privées
   # n'existent pas en python).
   print("Tentative de connexion à la base de données " + bdd.m_database)
   print("\tRemarque : En cas d'échec, la réponse du serveur de bdd peut tarder\n" \
         "\t           car elle dépend du timeout configuré sur ce serveur !")
   cnx = bdd._bdd_connecter()
   if bdd.m_messageError == "OK":
      print("Connexion à la base de données "  + bdd.m_database + " réussie")
      time.sleep(1)
      bdd._bdd_deconnecter(cnx)   
      print("Déconnexion de la base de données réussie")
      print("***** Test OK *****")
   else:
      print("\nECHEC lors de la connexion à la base de données "  + bdd.m_database)
      print("!!!!! Test en échec !!!!!")

   
   # ---------- Requête de type SELECT ----------
   print('\n---------- Requête de type SELECT ----------')
   #Affichage du nom des champs d'une table à partir du connecteur mysql-python
   nomTable = "enseignant"
   print("Récupération du nom des champs de la table " + nomTable + " :")
   resultSelect = bdd.getNomChampTable(nomTable)
   print(resultSelect)
   print("--------------------------------------------")
   
   # Affichage résultat requête SELECT
   sqlQuery = "SELECT * FROM enseignant"
   print("Résultat requête suivante :")
   print("\t" + sqlQuery)
   nbLigneAffich = bdd.afficherResultatReqSelect(sqlQuery)
   print("\nNombre de lignes retourné par la requête : " + str(nbLigneAffich))
   print("--------------------------------------------")
   
   
   # ---------- Requête de type INSERT (sans clé étrangère) ----------
   print('\n---------- Requête de type INSERT (sans clé étrangère)  ----------')
   # Insertion de données dans une bdd
   numeroEtudiant = 901
   nom = "toto"
   adresse = "Paris"
   # Remarque : à la 2è exécution de ce programme, une erreur se produira si on ne modifie les données
   # à insérer... Erreur exécution req INSERT : 1062 (23000): Duplicate entry '900' for key 'PRIMARY'
   sqlQuery = "INSERT INTO etudiant (numeroEtudiant, nom, adresse) VALUES ('%s', %s, %s)"
   print("Insertion de données (sans clé étrangère) avec la requête suivante :")
   print("\t" + sqlQuery + "\n\t\tavec '%s' = ", str(numeroEtudiant), "   %s = ", nom,
         "   %s = ", adresse)
   bdd.executerReqInsertUpdateDelete(sqlQuery, numeroEtudiant, nom, adresse)
   print("--------------------------------------------")
   
   # Affichage contenu table après insertion de données
   print("Contenu table 'etudiant' après insertion données :")
   sqlQuery = "SELECT * FROM etudiant"
   nbLigneAffich = bdd.afficherResultatReqSelect(sqlQuery)
   print("\nNombre de lignes retourné par la requête : " + str(nbLigneAffich))
   print("--------------------------------------------")
   
   print('\n---------- Requête de type INSERT (avec clé étrangère) ----------')
   # --- Insertion de données dont une clé étrangère ---
   # Affichage contenu table avant insertion de données
   print("Contenu table 'tbmodule' avant insertion données :")
   sqlQuery = "SELECT * FROM tbmodule"
   nbLigneAffich = bdd.afficherResultatReqSelect(sqlQuery)
   print("\nNombre de lignes retourné par la requête : " + str(nbLigneAffich))
   print("--------------------------------------------")
   
   # Insertion de données dans une bdd
   # Récupération de la clé étrangère numeroEnseignant
   # On considère que le professeur Didier est unique
   nomEnseignant = "Didier"
   grade = "Professeur"
   sqlQuery = "SELECT numeroEnseignant FROM enseignant "  \
      "WHERE nom LIKE %s AND grade LIKE %s"
   resultSelect = bdd.getResultatReqSelect(sqlQuery, nomEnseignant, grade)
   if len(resultSelect) != 0:
      fk_tbmodule_numeroEnseignant = resultSelect[0][0]
      numeroModule = 990
      titre = "Informatique"
      # Remarque : à la 2è exécution de ce programme, une erreur se produira si on ne modifie les
      # données à insérer... Erreur exécution req INSERT : 1062 (23000): Duplicate entry '990' for
      # key 'PRIMARY'
      sqlQuery = "INSERT INTO tbmodule (numeroModule, titre, numeroEnseignant) " \
         "VALUES ('%s', %s, '%s')"
      print("Insertion de données avec la requête suivante :")
      print("\t" + sqlQuery + "\n\t\tavec '%s' = ", str(numeroModule), "   %s = ", titre,
            "   '%s' = ", fk_tbmodule_numeroEnseignant)
      bdd.executerReqInsertUpdateDelete(sqlQuery, numeroModule, titre, fk_tbmodule_numeroEnseignant)
      print("--------------------------------------------")
   else:
      print("Erreur : retour requête sans enregistrement")
   
   # Affichage contenu table après insertion de données
   print("Contenu table 'tbmodule' avant insertion données :")
   sqlQuery = "SELECT * FROM tbmodule"
   nbLigneAffich = bdd.afficherResultatReqSelect(sqlQuery)
   print("\nNombre de lignes retourné par la requête : " + str(nbLigneAffich))
   
   # ---------- Requête de type UPDATE ----------
   print('\n---------- Requête de type UPDATE ----------')
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
   bdd.executerReqInsertUpdateDelete(sqlQuery, numeroEnseignant, nom, grade, salaire)
   print("--------------------------------------------------------------------------")
   
   # Affichage contenu table après insertion de données
   print("Affichage de l'enregistrement précédemment inséré avec la requête suivante :")
   sqlQuery = "SELECT * FROM enseignant WHERE numeroEnseignant = '%s'"
   print("\t" + sqlQuery + "\n\t\tavec '%s' = " + str(numeroEnseignant))
   bdd.afficherResultatReqSelect(sqlQuery, numeroEnseignant)
   print("--------------------------------------------------------------------------")
   
   # --- Modification d'un enregistrement ---
   # Titi est en fait un Assistant et non un professeur et gagne 900€
   grade = "Assistant"
   salaire = 900
   sqlQuery = "UPDATE enseignant SET grade = %s, salaire = '%s' WHERE numeroEnseignant = '%s'"
   print("Modification de données avec la requête suivante :")
   print("\t" + sqlQuery + "\n\t\tavec %s = ", grade, "   '%s' = ", salaire,
         "   '%s' = ", numeroEnseignant)
   bdd.executerReqInsertUpdateDelete(sqlQuery, grade, salaire, numeroEnseignant)
   print("--------------------------------------------------------------------------")
   
   # Affichage contenu table après modification de données
   print("Affichage de l'enregistrement modifié avec la requête suivante :")
   sqlQuery = "SELECT * FROM enseignant WHERE numeroEnseignant = '%s'"
   print("\t" + sqlQuery + "\n\t\tavec '%s' = " + str(numeroEnseignant))
   bdd.afficherResultatReqSelect(sqlQuery, numeroEnseignant)
   print("--------------------------------------------------------------------------")
   
   # ---------- Requête de type DELETE ----------
   print('\n---------- Requête de type DELETE ----------')
   # --- Suppression d'un enregistrement dans la bdd ---
   # Ajout du professeur Tutu, de numéro 975, avec un salaire de 1300€
   numeroEnseignant = 975
   nom = "Tutu"
   grade = "Professeur"
   salaire = 1300
   # Remarque : à la 2è exécution de ce programme, une erreur se produira si on ne modifie les données
   # à insérer... Erreur exécution req INSERT : 1062 (23000): Duplicate entry '975' for key 'PRIMARY'
   sqlQuery = "INSERT INTO enseignant (numeroEnseignant, nom, grade, salaire) "  \
      "VALUES ('%s', %s, %s, '%s')"
   print("Insertion de données avec la requête suivante :")
   print("\t" + sqlQuery + "\n\t\tavec '%s' = ", str(numeroEnseignant), "   %s = ", nom,
         "   %s = ", grade, "   '%s' = ", salaire)
   bdd.executerReqInsertUpdateDelete(sqlQuery, numeroEnseignant, nom, grade, salaire)
   print("--------------------------------------------------------------------------")
   
   # Affichage contenu table avant suppression de données
   print("Affichage de l'enregistrement précédemment inséré avec la requête suivante :")
   sqlQuery = "SELECT * FROM enseignant WHERE numeroEnseignant = '%s'"
   print("\t" + sqlQuery + "\n\t\tavec '%s' = " + str(numeroEnseignant))
   nbLigneAffich = bdd.afficherResultatReqSelect(sqlQuery, numeroEnseignant)
   print("Nombre de lignes retourné par la requête : " + str(nbLigneAffich))
   print("--------------------------------------------------------------------------")
   
   # --- Suppression d'un enregistrement ---
   sqlQuery = "DELETE FROM enseignant WHERE numeroEnseignant = '%s'"
   print("Suppression d'un enregistrement avec la requête suivante :")
   print("\t" + sqlQuery + "\n\t\tavec '%s' = ", numeroEnseignant)
   bdd.executerReqInsertUpdateDelete(sqlQuery, numeroEnseignant)
   print("--------------------------------------------------------------------------")
   
   # Affichage contenu table après suppression de données
   print("Vérification de la suppression de l'enregistrement avec la requête suivante :")
   sqlQuery = "SELECT * FROM enseignant WHERE numeroEnseignant = '%s'"
   print("\t" + sqlQuery + "\n\t\tavec '%s' = " + str(numeroEnseignant))
   nbLigneAffich = bdd.afficherResultatReqSelect(sqlQuery, numeroEnseignant)
   print("Nombre de lignes retourné par la requête : " + str(nbLigneAffich))
   print("--------------------------------------------------------------------------\n")
   
   print("---------- Fin des tests de la classe Bddmysql.py ----------")   