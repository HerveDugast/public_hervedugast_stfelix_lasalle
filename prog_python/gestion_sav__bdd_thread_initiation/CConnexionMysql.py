#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : CConnexionMysql.py      version 1.2
Date : 30-04-2018
Auteur : Hervé Dugast

Classe permettant de créer une connexion à une base de données et d'exécuter des requêtes de type 
SELECT, INSERT, UPDATE ou DELETE. Les éventuelles erreurs sont gérées. Toutes les opérations
réalisées sont journalisées.

------- affichage console --------------------------------------------------------------------------
2018-04-09 16:53:01,870 -- INFO -- *** 1- Affichage du nom des champs d'une table ***
['id', 'code', 'nom']
2018-04-09 16:53:01,875 -- INFO -- *** 2- Exécution requête SELECT ***
  résultat : 3 lignes
(1, 'R', 'Réparation')
(2, 'E', 'Echange')
(3, 'D', 'Devis')
  résultat : 1 lignes
('Devis',)
2018-04-09 16:53:01,887 -- INFO -- *** 3- Exécution requête INSERT sans clé étrangère ***
  résultat : 4 lignes
(1, 'R', 'Réparation')
(2, 'E', 'Echange')
(3, 'D', 'Devis')
(56, 'A', 'Attente')
2018-04-09 16:53:01,904 -- INFO -- *** 4- Exécution requête UPDATE sans clé étrangère ***
  résultat : 4 lignes
(1, 'R', 'Réparation')
(2, 'E', 'Echange')
(3, 'D', 'Devis')
(56, 'F', 'Facturation')
2018-04-09 16:53:01,925 -- INFO -- *** 5- Exécution requête DELETE ***
  résultat : 3 lignes
(1, 'R', 'Réparation')
(2, 'E', 'Echange')
(3, 'D', 'Devis')
2018-04-09 16:53:01,939 -- INFO -- *** 6- Exécution requête INSERT AVEC clé étrangère ***
2018-04-09 16:53:01,944 -- INFO -- Date mémorisation : 2018-04-09 16:53:01.944123
  résultat : 1 lignes
(22, datetime.datetime(2018, 4, 9, 16, 53, 2), 3)

Fin programme
----------------------------------------------------------------------------------------------------
--------------- Contenu fichier debugMysql.log -----------------------------------------------------
2018-04-09 16:53:01,865 -- DEBUG -- Création d'un objet 'interface de connexion' à la bdd -- CConnexionMysql.CConnexionMysql:self.__init__()
2018-04-09 16:53:01,869 -- DEBUG -- * Succès connexion/déconnexion à bdd 'dbsav' sur host '192.168.0.20' * -- CConnexionMysql.CConnexionMysql:self.__verifierConnnexionBdd()
2018-04-09 16:53:01,870 -- INFO -- *** 1- Affichage du nom des champs d'une table ***
2018-04-09 16:53:01,873 -- DEBUG -- * Succès exécution requête *
SELECT * FROM action 
-- CConnexionMysql.CConnexionMysql:self.getNomsColonnesTable()
2018-04-09 16:53:01,874 -- DEBUG --   résultat : 3 colonnes -- CConnexionMysql.CConnexionMysql:self.afficherNomsColonnesTable()
2018-04-09 16:53:01,875 -- DEBUG -- ['id', 'code', 'nom']
...
2018-04-09 16:53:01,939 -- INFO -- *** 6- Exécution requête INSERT AVEC clé étrangère ***
2018-04-09 16:53:01,943 -- DEBUG -- * Succès exécution requête *
SELECT id FROM action WHERE code LIKE 'D' 
-- CConnexionMysql.CConnexionMysql:self.executerReqSelect()
2018-04-09 16:53:01,944 -- INFO -- Date mémorisation : 2018-04-09 16:53:01.944123
2018-04-09 16:53:01,951 -- DEBUG -- * Succès exécution requête *
INSERT INTO journal (date_heure, id_action) VALUES ('2018-04-09 16:53:01.944123', 3) 
-- CConnexionMysql.CConnexionMysql:self.executerReqInsUpdDel()
2018-04-09 16:53:01,955 -- DEBUG -- * Succès exécution requête *
SELECT * FROM journal 
-- CConnexionMysql.CConnexionMysql:self.executerReqSelect()
2018-04-09 16:53:01,956 -- DEBUG --   résultat : 1 lignes -- CConnexionMysql.CConnexionMysql:self.afficherResultatReqSelect()
2018-04-09 16:53:01,956 -- DEBUG -- (22, datetime.datetime(2018, 4, 9, 16, 53, 2), 3) -- CConnexionMysql.CConnexionMysql:self.afficherResultatReqSelect()
2018-04-09 16:53:01,964 -- DEBUG -- Objet connexion bdd a été détruit -- CConnexionMysql.CConnexionMysql:self.__del__()
----------------------------------------------------------------------------------------------------
"""

import sys
import time
# importe modules contenus dans le dossier mysql\connector (C:\Python34\Lib\site-packages\)
import mysql.connector
# dans le module datetime.py import de la classe datetime (C:\Python34\Lib\)
from datetime import datetime
# classe gérant les loggers et les handlers
from CLogger import CLogger

class CConnexionMysql():
   """ Classe permettant de créer une connexion à une base de données et d'exécuter des requêtes 
       de type SELECT, INSERT, UPDATE ou DELETE. Les éventuelles erreurs sont gérées.
       Toutes les opérations réalisées sont journalisées.
   """
   
   def __init__(self, paramBdd, logger):
      """ Constructeur, création d'un objet connexion MySQL. 
          Exemple de paramètres de connexion :
             paramBdd = [    host,       port,   user,     password,   database]
             paramBdd = ["192.168.0.20", 3306, "user_dbsav", "password", "dbsav"]
      """
      fonction = "CConnexionMysql.CConnexionMysql:self.__init__(host={0[0]}, port={0[1]}, user={0[2]}, " \
         "password={0[3]}, database={0[4]})".format(paramBdd)
      # mémorisation des paramètres de connexion de la bdd dans une liste
      self.__paramBdd = paramBdd
      self.logger = logger
      # liste modifiable qui contiendra les lignes (tuples) retournées par une requête SELECT
      # 1 tuple correspond à une ligne de résultat retourné par une requête de type SELECT.
      # 1 tuple peut donc contenir le résultat d'une ou plusieurs colonnes. 
      self.__resultReqSelect = []
      # création de la connexion à la bdd
      try:
         self.__codeResult = 0
         # création objet connexion à la bdd indiquée
         message = "*** Connexion à la bdd : host={0[0]}, port={0[1]}, user={0[2]}, " \
            "password={0[3]}, database={0[4]}".format(paramBdd)
         print(message)
         self.logger.debug("{} -- {}".format(message, fonction))
         self.__cnx = mysql.connector.connect(host=self.__paramBdd[0], port=self.__paramBdd[1], \
                                              user=self.__paramBdd[2], password=self.__paramBdd[3],\
                                              database=self.__paramBdd[4])
         self.logger.debug("* Succès connexion à la bdd * -- {}".format(fonction))
      except mysql.connector.Error as erreur:
         self.__codeResult = 1
         message = "code {} \n{} -- {}".format(self.__codeResult, erreur, fonction)
         self.logger.error(message)
      except:
         self.__codeResult = 2
         message = "code {} \n{} \n-- {}".format(self.__codeResult, sys.exc_info(), fonction)
         self.logger.error(message)
      
   def verifierConnexionBdd(self):
      """ Vérifie si la connexion à la bdd est opérationnelle
          Retour : bool    True : Succès connexion bdd 
      """
      fonction = "CConnexionMysql.CConnexionMysql:self.verifierConnexionBdd()"
      isCnxBddOk = self.__cnx.is_connected()
      if isCnxBddOk:
         message = "Vérification connexion bdd : Succès -- {}".format(fonction)
         self.__codeResult = 0
      else:
         message = "Vérification connexion bdd : Echec -- {}".format(fonction)
      self.logger.debug(message)
      return self.__cnx.is_connected()
      
   def __del__(self):
      """ Destructeur, cette méthode est appelée lorsque toutes les références à cet objet ont
          été supprimées. Dans ce cas, on considère que l'objet est détruit (l'instant exact de
          destruction n'est pas connu).
          AFFICHE un message lorsque l'objet est considéré "détruit". Si rien ne s'affiche lors de 
          l'exécution de la destruction de l'objet, c'est qu'il existe encore au moins une 
          référence sur cet objet qui traine quelque part !
          Rappel :
          Pour détruire un objet, il suffit de supprimer toutes ses références. Le garbage 
          collector (ramasse-miettes, gestionnaire mémoire) se chargera de le supprimer 
          définitivement de la mémoire RAM dans un délai plus ou moins grand (délai non connu).
          Utilisez l'instruction suivante pour supprimer une référence : 
          nomObjet = None ou del nomObjet
      """
      fonction = "CConnexionMysql.CConnexionMysql:self.__del__()"
      self.logger.debug("Objet connexion bdd a été détruit -- {}".format(fonction))
      
   def refaireConnexionBdd(self):
      """ Essaie à nouveau de se connecter à une base de données MySQL
          Retour : int     codeResult = 0 -> connexion réussie       > 0 -> échec connexion
      """
      fonction = "CConnexionMysql.CConnexionMysql:self.__seConnecter()"
      try:
         self.__codeResult = 0
         # essaie de se reconnecter à la bdd 
         message = "*** Essai reconnexion à la bdd : host={0[0]}, port={0[1]}, user={0[2]}, " \
            "password={0[3]}, database={0[4]}".format(self.__paramBdd)
         print(message)
         self.logger.debug("{} -- {}".format(message, fonction))
         self.__cnx.connect(host=self.__paramBdd[0], \
                            port=self.__paramBdd[1], user=self.__paramBdd[2], \
                            password=self.__paramBdd[3], database=self.__paramBdd[4])
         self.logger.debug("* Succès connexion à la bdd * -- {}".format(fonction))
      except mysql.connector.Error as erreur:
         self.__codeResult = 3
         message = "code {} \n{} -- {}".format(self.__codeResult, erreur, fonction)
         self.logger.error(message)
      except:
         self.__codeResult = 4
         message = "code {} \n{} \n-- {}".format(self.__codeResult, sys.exc_info(), fonction)
         self.logger.error()
      finally:
         return self.__codeResult                  
      
   def seDeconnecterBdd(self):
      """ Se déconnecte d'une base de données MySQL, ferme la connexion à la bdd
      """
      fonction = "CConnexionMysql.CConnexionMysql:self.seDeconnecterBdd()"
      try:
         self.__cnx.close()
         self.logger.debug("Fermeture de la connexion bdd (objet cnx) -- {}".format(fonction))
      except:
         self.__codeResult = 5
         message = "code {}, échec fermeture de la connexion bdd (objet cnx)\n{} \n-- {}" \
            .format(self.__codeResult, sys.exc_info(), fonction)
         self.logger.error(message)
      
   def getNomsColonnesTable(self, sqlQuery, nomTable='0'):
      """ Retourne le nom des colonnes de la table demandée à l'aide d'une requête de type SELECT
          Paramètres : nomTable -> nom table dont on veut connaître le nom des colonnes
          Mise à jour de l'attribut __resultReqSelect : contiendra lignes retournées par req SELECT
          Retour : int     codeResult = 0 -> succès       codeResult > 0 -> échec 
      """
      try:
         fonction = "CConnexionMysql.CConnexionMysql:self.getNomsColonnesTable()"
         # vérifie la connexion de la bdd et en cas d'échec essaie de se reconnecter
         if not self.__cnx.is_connected():
            self.refaireConnexionBdd()
         # Création curseur (mémoire tampon que l'on peut parcourir avec curseur ligne par ligne)
         if self.__codeResult == 0:
            # Succès connexion à la bdd
            cur = self.__cnx.cursor()
            if nomTable != '0':
               # nom table passé en argument à fonction getNomsColonnesTable, création req SELECT
               sqlQuery = "SELECT * FROM {}".format(nomTable)
            cur.execute(sqlQuery)
            # Copie du résultat de la requête dans une liste
            cur.fetchall()
            self.__resultReqSelect = []
            # récupération des noms de table
            for idx, nom in enumerate(cur._description):
               champ = str(nom[0])
               self.__resultReqSelect.append(champ)
            cur.close()
            message = "* Succès exécution requête :\n{} \n-- {}".format(sqlQuery, fonction)
            self.logger.debug(message)
      except mysql.connector.Error as erreur:
         self.__codeResult = 10
         message = "code {}\n{}\n! Echec exécution requête :\n{} \n-- {}" \
            .format(self.__codeResult, erreur, sqlQuery, fonction)
         self.logger.error(message)
         self.__resultReqSelect = []
      except:
         self.__codeResult = 11
         message = "code {}\n{}\n! Echec exécution requête :\n{} \n-- {}" \
            .format(self.__codeResult, sys.exc_info(), sqlQuery, fonction)
         self.logger.error(message)
         self.__resultReqSelect = []
      finally:
         return self.__codeResult

   def afficherNomsColonnesTable(self, nomTable):
      """ Affiche le nom des colonnes de la table demandée
          Paramètres : nomTable -> nom table dont on veut connaître le nom des colonnes
          Retour : int     codeResult = 0 -> succès       codeResult > 0 -> échec 
      """
      fonction = "CConnexionMysql.CConnexionMysql:self.afficherNomsColonnesTable()"
      sqlQuery = "SELECT * FROM {}".format(nomTable)
      self.getNomsColonnesTable(sqlQuery, nomTable) 
      if self.__codeResult == 0:
         # affiche nombre de colonnes trouvées pour la table
         message = "  résultat : {} colonnes -- {}".format(len(self.__resultReqSelect), fonction)
         self.logger.debug(message)
         colonneTable = []
         if self.__resultReqSelect:
            # résultat non vide, mémorise chaque colonne retournée dans une liste 
            for row in self.__resultReqSelect:
               colonneTable.append(row)
            print(colonneTable)
            self.logger.debug(colonneTable)
      return self.__codeResult     

   def executerReqSelect(self, sqlQuery):
      """ Exécute une requête de type SELECT
          Paramètres : sqlQuery -> requête SQL (format chaine caractères) de type SELECT
          Mise à jour de l'attribut __resultReqSelect : contiendra lignes retournées par req SELECT
          Retour : int     codeResult = 0 -> succès       codeResult > 0 -> échec 
      """
   
      try:
         fonction = "CConnexionMysql.CConnexionMysql:self.executerReqSelect()"
         # vérifie la connexion de la bdd et en cas d'échec essaie de se reconnecter
         if not self.__cnx.is_connected():
            self.refaireConnexionBdd()
         if self.__codeResult == 0:
            # Succès connexion à la bdd 
            # Création curseur (mémoire tampon que l'on peut parcourir avec curseur ligne par ligne)
            cur = self.__cnx.cursor()
            cur.execute(sqlQuery)
            # Copie du résultat de la requête dans une liste
            self.__resultReqSelect = []
            for row in cur.fetchall() :
               self.__resultReqSelect.append(row)    # ajout de chaque ligne dans la séquence
            cur.close()
            message = "* Succès exécution requête :\n{} \n-- {}".format(sqlQuery, fonction)
            self.logger.debug(message)
      except mysql.connector.Error as erreur:
         self.__codeResult = 10
         message = "code {}\n{}\n! Echec exécution requête :\n{} \n-- {}" \
            .format(self.__codeResult, erreur, sqlQuery, fonction)
         self.logger.error(message)
         self.__resultReqSelect = []
      except:
         self.__codeResult = 11
         message = "code {}\n{}\n! Echec exécution requête :\n{} \n-- {}" \
            .format(self.__codeResult, sys.exc_info(), sqlQuery, fonction)
         self.logger.error(message)
         self.__resultReqSelect = []
      finally:
         return self.__codeResult
      
   def afficherResultatReqSelect(self, sqlQuery):
      """ Exécute et affiche le résultat d'une requête SELECT
          Paramètres : sqlQuery -> requête SQL (format chaine caractères) de type SELECT
          Mise à jour de l'attribut __resultReqSelect : contiendra lignes retournées par req SELECT
          Retour : int     codeResult = 0 -> succès       codeResult > 0 -> échec 
      """
      fonction = "CConnexionMysql.CConnexionMysql:self.afficherResultatReqSelect()"
      self.executerReqSelect(sqlQuery) 
      if self.__codeResult == 0:
         # Succès connexion à la bdd
         message = "  résultat : {} lignes".format(len(self.__resultReqSelect))
         print(message)
         self.logger.debug("{} -- {}".format(message, fonction))
         if self.__resultReqSelect:
            # une ou plusieurs lignes de résultats à la requête, affiche chaque ligne
            for row in self.__resultReqSelect:
               print(row)
               self.logger.debug("{} -- {}".format(row, fonction))
      return self.__codeResult
   
   def executerReqInsUpdDel(self, sqlQuery):
      """ Exécute une requête SQL de type INSERT/UPDATE/DELETE
          Paramètres : sqlQuery -> requête SQL (format chaine caractères) type INSERT/UPDATE/DELETE
      """
      try:
         fonction = "CConnexionMysql.CConnexionMysql:self.executerReqInsUpdDel()"
         # vérifie la connexion de la bdd et en cas d'échec essaie de se reconnecter
         if not self.__cnx.is_connected():
            self.refaireConnexionBdd()
         if self.__codeResult == 0:
            # Succès connexion à la bdd
            # Création curseur (mémoire tampon que l'on peut parcourir avec curseur ligne par ligne)
            # prépare le traitement de la requête, qui sera effectué lors de l'envoi d'un commit
            cur = self.__cnx.cursor()
            cur.execute(sqlQuery)
            self.__cnx.commit()
            cur.close()
            message = "* Succès exécution requête :\n{} \n-- {}".format(sqlQuery, fonction)
            self.logger.debug(message)
      except mysql.connector.Error as erreur:
         self.__codeResult = 20
         message = "code {}\n{}\n! Echec exécution requête :\n{} \n-- {}" \
            .format(self.__codeResult, erreur, sqlQuery, fonction)
         self.logger.error(message)
      except:
         # sys.exc_info()[0] : donne un tupple de 3 valeurs sur l'exception qui vient d'arriver
         self.__codeResult = 21
         message = "code {}\n{}\n! Echec exécution requête :\n{} \n-- {}" \
            .format(self.__codeResult, sys.exc_info(), sqlQuery, fonction)
         self.logger.error(message)
      finally:
         return self.__codeResult
      
   def recupererValeurId(self, nomTable, nomColonneId):
      """ Retourne la valeur d'une clé primaire (id) de type auto-increment. Vérifie que cette 
          valeur est bien un entier.
          Retour : int     succès -> valeurId      échec -> -1
      """
      fonction = "CConnexionMysql.CConnexionMysql:self.recupererValeurId()"
      # vérifie la connexion de la bdd et en cas d'échec essaie de se reconnecter
      if not self.__cnx.is_connected():
         self.refaireConnexionBdd()
      sqlQuery = "SELECT id FROM {} WHERE code LIKE '{}'".format(nomTable, nomColonneId)
      self.executerReqSelect(sqlQuery)
      # get_resultReqSelect retourne liste modifiable contenant un tuple qui contient le résultat
      if self.__codeResult == 0:
         # Succès exécution requête
         if self.get_resultReqSelect():
            # succès, requête retourne un résultat
            idValeur = self.get_resultReqSelect().pop()[0]   # idValeur est un entier (int)
            # vérifie que la valeur idValeur est bien un entier
            if not isinstance(idValeur, int):
               # échec ! la valeur de l'id n'est pas un entier
               self.__codeResult = 30
               message = "code {}, échec récupération valeur id, idValeur ({}) n'est pas entier !"\
                  "Requête exécutée :\n{} -- {}" \
                  .format(self.__codeResult, idValeur, sqlQuery, fonction)
               self.logger.error(message)
               idValeur = -1
         else:
            # échec ! la valeur de l'id demandée n'a pas été trouvée
            self.__codeResult = 31
            message = "code {}, échec, valeur id non trouvée ! Requête exécutée :\n{} -- {}" \
               .format(self.__codeResult, sqlQuery, fonction)
            self.logger.error(message)
            idValeur = -1
      else:
         # Echec exécution requête
         idValeur = -1
      return idValeur
      
   def get_host(self):
      return self.__paramBdd[0]
   
   def get_port(self):
      return self.__paramBdd[1]

   def get_user(self):
      return self.__paramBdd[2]

   def get_password(self):
      return self.__paramBdd[3]

   def get_database(self):
      return self.__paramBdd[4]
   
   def get_codeResult(self):
      return self.__codeResult
   
   def get_resultReqSelect(self):
      # __resultReqSelect est une liste modifiable de tuples. 
      # 1 tuple correspond à une ligne de résultat retourné par une requête de type SELECT.
      # 1 tuple peut donc contenir le résultat d'une ou plusieurs colonnes. 
      return self.__resultReqSelect

if __name__ == "__main__":
   CLogger.effacerFichierLog("debugMysql.log")
   # ----- Mise en place du logger qui va gérer les handlers console et fichier rotatif
   logger = CLogger(loggerName="debugMysql", loggerLevel="DEBUG", \
                    consoleLevel="INFO", fileName="debugMysql.log", fileLevel="DEBUG")      
   # ---- Création d'un objet 'Interface connexion bdd', cela teste aussi l'accès à la bdd -------
   # créer une connexion à la bdd
   paramBdd = ("192.168.0.20", 3306, "user_sav", "password", "dbsav") 
   #paramBdd = ("10.16.3.232", 3306, "user_dbsav", "password", "dbsav")
   bdd = CConnexionMysql(paramBdd, logger)

   if bdd.get_codeResult() != 0:
      # échec connexion à bdd
      print("!!! Echec connexion à bdd -> destruction objet interface bdd2 !!!")
      bdd = None    # destruction de l'objet
      time.sleep(1)      
   else:
      # Succès connexion à la bdd
      
      # ---------- Requête de type SELECT ---------------------------------------------------
      # Affichage du contenu de la table Action
      bdd.logger.info("*** 1- Affichage du nom des champs d'une table ***")
      bdd.afficherNomsColonnesTable("action")
   
      # Affichage du contenu de la table Action
      bdd.logger.info("*** 2- Exécution requête SELECT ***")
      sqlQuery = "SELECT * FROM action"
      bdd.afficherResultatReqSelect(sqlQuery)
      
      # Requête SELECT : affichage de la valeur d'un champ
      sqlQuery = "SELECT nom FROM action WHERE code LIKE '{}'".format('D')
      bdd.afficherResultatReqSelect(sqlQuery)
      
      # ---------- Requête de type INSERT (sans clé étrangère) ------------------------------
      bdd.logger.info("*** 3- Exécution requête INSERT sans clé étrangère ***")
      codeVal = 'A'
      nomVal = "Attente"
      # requête à exécuter pour insérer les 2 éléments précédents
      # INSERT INTO action (code, nom) VALUES ('A', 'Attente')
      sqlQuery = "INSERT INTO action (code, nom) VALUES ('{}', '{}')".format(codeVal, nomVal)
      bdd.executerReqInsUpdDel(sqlQuery)
      sqlQuery = "SELECT * FROM action"
      bdd.afficherResultatReqSelect(sqlQuery)
      
      # ---------- Requête de type UPDATE (sans clé étrangère) ------------------------------
      bdd.logger.info("*** 4- Exécution requête UPDATE sans clé étrangère ***")
      codeNew = 'F'
      nomNew = "Facturation"
      # requête pour remplacer 'A', 'ATTENTE' par 'F', 'Facturation'
      # UPDATE action SET code = 'F', nom = 'Facturation' WHERE code = 'A'
      sqlQuery = "UPDATE action SET code = '{}', nom = '{}' WHERE code = 'A'" \
         .format(codeNew, nomNew)
      bdd.executerReqInsUpdDel(sqlQuery)
      sqlQuery = "SELECT * FROM action"
      bdd.afficherResultatReqSelect(sqlQuery)
      
      # ---------- Requête de type DELETE ---------------------------------------------------
      bdd.logger.info("*** 5- Exécution requête DELETE ***")
      codeAEffacer = 'F'
      # requête pour supprimer la ligne correspondant au code 'F'
      # DELETE FROM action WHERE code = 'F'
      sqlQuery = "DELETE FROM action WHERE code = '{}'".format(codeAEffacer)
      bdd.executerReqInsUpdDel(sqlQuery)
      sqlQuery = "SELECT * FROM action"
      bdd.afficherResultatReqSelect(sqlQuery)
      
      # ---------- Requête de type INSERT (AVEC clé étrangère) ------------------------------
      bdd.logger.info("*** 6- Exécution requête INSERT AVEC clé étrangère ***")
      # on souhaite mémoriser une action ('D') dans la table journal contenant les colonnes : 
      # table journal contient les colonnes : 'id':int, date_heure:datetime, id_action:int
      # table action contient les colonnes : 'id':int, code:str, nom:str
      codeActionAMem = 'D'

      # - étape 1 : récupérer valeur id de la ligne correspondant au code 'D' dans table 'action'
      idAction = bdd.recupererValeurId('action', codeActionAMem)
      if idAction != -1:
         # succès, codeActionAMem reconnu et peut donc être mémorisé
         # - étape 2 : insérer l'enregistrement dans la table journal
         # date et heure courante de la mémorisation. Dans une colonne de type datetime,
         # on peut insérer objet datetime ou chaine datetime (exemple : '2018-03-26 19:25:05')
         dateHeure = datetime.now()
         bdd.logger.info("Date mémorisation : {}".format(dateHeure)) # les microsecond sont ignorées
         # requête à exécuter pour insérer l'action à mémoriser
         # INSERT INTO journal (date_heure, id_action) VALUES ('2018-03-26 19:25:05.319559', 3)
         sqlQuery = "INSERT INTO journal (date_heure, id_action) VALUES ('{}', {})" \
            .format(dateHeure, idAction)
         bdd.executerReqInsUpdDel(sqlQuery)
      
      # vérification de la mémorisation dans la bdd
      sqlQuery = "SELECT * FROM journal"
      bdd.afficherResultatReqSelect(sqlQuery)   
      
   bdd.seDeconnecterBdd()
   bdd = None   # destruction objet
   time.sleep(1)
   print("\nFin programme")
      