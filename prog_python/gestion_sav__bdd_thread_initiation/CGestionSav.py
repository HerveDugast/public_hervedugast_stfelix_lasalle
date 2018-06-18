#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : CGestionSav.py      version 1.2
Date : 30-04-2018
Auteur : Hervé Dugast

Fonctionnement :
   Gère les retours de matériel en panne. Mémorise en base de données le type d'intervention 
   effectué parmi : 'R', 'E' ou 'D'.
       'R' : Réparation du matériel    'E' : Echange     'D' : Devis, dommages hors garantie
   Toutes les opérations sont journalisées en mode DEBUG dans le fichier debugSav.log.
   Les erreurs et problèmes de connexion sont gérés.

------- affichage console --------------------------------------------------------------------------
*** Connexion à la bdd : host=192.168.0.20, port=3306, user=user_sav, password=password, database=dbsav
*** Mise en bdd de l'action 'R'
  Succès mise en base
*** Mise en bdd de l'action 'E'
  Succès mise en base
*** Mise en bdd de l'action 'R'
  Succès mise en base
*** Mise en bdd de l'action 'D'
  Succès mise en base

----- Affichage BRUT des actions mémorisées dans la bdd dbsav -----
  résultat : 4 lignes
(83, datetime.datetime(2018, 5, 1, 10, 50, 43), 'R', 'Réparation')
(84, datetime.datetime(2018, 5, 1, 10, 50, 43), 'E', 'Echange')
(85, datetime.datetime(2018, 5, 1, 10, 50, 43), 'R', 'Réparation')
(86, datetime.datetime(2018, 5, 1, 10, 50, 43), 'D', 'Devis')

----- Affichage des actions mémorisées dans la bdd dbsav -----
83   2018-05-01 10:50:43   R   Réparation   
84   2018-05-01 10:50:43   E   Echange   
85   2018-05-01 10:50:43   R   Réparation   
86   2018-05-01 10:50:43   D   Devis   

----- EFFACEMENT des 4 actions mémorisées dans la bdd dbsav -----

----- Affichage des actions mémorisées dans la bdd dbsav -----
0 action mémorisée dans la bdd

Fin programme CGestionSav.py
----------------------------------------------------------------------------------------------------

--------------- Contenu fichier debugSav.log -------------------------------------------------------
2018-05-01 10:50:43,924 -- DEBUG -- *** Connexion à la bdd : host=192.168.0.20, port=3306, user=user_sav, password=password, database=dbsav -- CConnexionMysql:self.__init__(host=192.168.0.20, port=3306, user=user_sav, password=password, database=dbsav)
2018-05-01 10:50:43,929 -- DEBUG -- * Succès connexion à la bdd * -- CConnexionMysql:self.__init__(host=192.168.0.20, port=3306, user=user_sav, password=password, database=dbsav)
2018-05-01 10:50:43,929 -- DEBUG -- Création d'un objet 'gestion sav' avec lien à bdd et logger -- CGestionSav:self.__init__()
2018-05-01 10:50:43,930 -- DEBUG -- *** Mise en bdd de l'action 'R' -- CGestionSav:mettreEnBddAction()
2018-05-01 10:50:43,931 -- DEBUG -- Vérification connexion bdd : Succès
2018-05-01 10:50:43,933 -- DEBUG -- * Succès exécution requête :
SELECT code FROM action 
-- CConnexionMysql:self.executerReqSelect()
2018-05-01 10:50:43,935 -- DEBUG -- * Succès exécution requête :
SELECT id FROM action WHERE code LIKE 'R' 
-- CConnexionMysql:self.executerReqSelect()
2018-05-01 10:50:43,942 -- DEBUG -- * Succès exécution requête :
INSERT INTO journal (date_heure, id_action) VALUES ('2018-05-01 10:50:43', 1) 
-- CConnexionMysql:self.executerReqInsUpdDel()
2018-05-01 10:50:43,943 -- DEBUG --   Succès mise en base
...
-- CConnexionMysql:self.executerReqSelect()
2018-05-01 10:50:47,041 -- DEBUG -- Fermeture de la connexion bdd (objet cnx) -- CConnexionMysql:self.seDeconnecterBdd()
----------------------------------------------------------------------------------------------------
"""
from CConnexionMysql import CConnexionMysql
from datetime import datetime
# classe gérant les loggers et les handlers
from CLogger import CLogger
import time
import sys


class CGestionSav:
   """ Gère les retours de matériel en panne. Mémorise le type d'intervention effectué parmi :
       'R', 'E' ou 'D' dans une base de donnée MySQL de façon à faire des statistiques.
       'R' : Réparation du matériel    'E' : Echange     'D' : Devis, dommages hors garantie 
   """
   
   def __init__(self, bdd, logger):
      """ Constructeur
      """
      fonction = "CGestionSav:self.__init__()"
      self.__bdd = bdd
      self.logger = logger
      self.__codeResult = 0
      message = "Création d'un objet 'gestion sav' avec lien à bdd et logger -- {}".format(fonction)
      self.logger.debug(message)
      
   def mettreEnBddAction(self, codeAction='0'):
      """ Mémorise une action en bdd 
          Retour int : codeResult = 0 -> succès     codeResult > 0 -> Echec
      """
      fonction ="CGestionSav:mettreEnBddAction()"
      message = "*** Mise en bdd de l'action '{}'".format(codeAction)
      print(message)
      self.logger.debug("{} -- {}".format(message, fonction))
      try:
         # ----- Vérification validité du code action à mémoriser dans la bdd -----
         # vérifie la connexion de la bdd et en cas d'échec essaie de se reconnecter
         if self.__bdd.verifierConnexionBdd() == False:
            self.__bdd.refaireConnexionBdd()
         if self.__bdd.get_codeResult() != 0:
            raise ValueError  # lève exception si échec connexion
         # récupération des actions mémorisées dans la bdd (actions possibles)
         sqlQuery = "SELECT code FROM action"
         self.__codeResult = self.__bdd.executerReqSelect(sqlQuery)
         if self.__codeResult != 0:
            raise ValueError  # lève exception si échec exécution requête
         codeActionListTemp = self.__bdd.get_resultReqSelect()
         # codeActionListTemp est une liste contenant une autre liste (ex: [('R',),('E',),('D',)]
         # transformation de codeActionListTemp en une liste simple (ex. ['R','E','D'])
         codeActionList = []
         for code in codeActionListTemp:
            codeActionList.append(code[0])
         # vérification validitité de code action à mémoriser dans la bdd
         if codeAction != '0' and codeAction not in codeActionList:
            self.__codeResult = 100
            raise ValueError
         else:
            # Demande de saisie d'une action jusqu'à ce qu'elle soit valide
            while codeAction not in codeActionList:
               codeAction = input("Saisir un code action parmi {} ? ".format(codeActionList))
               if codeAction not in codeActionList:
                  print("Erreur ! Code action '{}' non valide !".format(codeAction))
      
         # ----- mise en base de données l'action -----
         # récupération valeur du champ id de l'action à mémoriser
         idAction = self.__bdd.recupererValeurId('action', codeAction)
         if self.__bdd.get_codeResult() != 0:
            raise ValueError  # lève exception si échec requête  
         if idAction != -1:
            # la valeur de idAction est valide
            # préparation date_heure,format str   (exemple : '2018-03-30 17:45:21')
            dateHeure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sqlQuery = "INSERT INTO journal (date_heure, id_action) VALUES ('{}', {})" \
               .format(dateHeure, idAction)
            self.__codeResult = self.__bdd.executerReqInsUpdDel(sqlQuery)
         else:
            raise ValueError  # erreur lors récupération id
         message = "  Succès mise en base"
         print(message)
         self.logger.debug(message)
      except ValueError as erreur:
         # ----- gestion des éventuelles erreurs survenues -----
         if self.__codeResult == 100:
            message = "code {}, échec mise en bdd, code action '{}' non valide ! -- {}" \
               .format(self.__codeResult, codeAction, fonction)
            self.logger.error(message)
         else:
            self.__codeResult = 102
            message = "code {}, échec mise en bdd codeAction '{}' -- {}" \
               .format(self.__codeResult, codeAction, fonction)
            self.logger.error(message)
      except:
         self.__codeResult = 103
         message = "code {}, échec mise en bdd codeAction '{}'\n{} -- {}" \
            .format(self.__codeResult, codeAction, sys.exc_info(), fonction)
         self.logger.error(message)
      
   def afficherActionMemBddBrut(self, debug=False):
      """ Affiche les actions mémorisées dans la table journal de la bdd, résultats bruts
      """
      fonction ="CGestionSav:afficherActionMemBddBrut()"
      message ="\n----- Affichage BRUT des actions mémorisées dans la bdd dbsav -----"
      print(message)
      self.logger.debug("{} -- {}".format(message, fonction))
      try:
         # vérifie la connexion de la bdd et en cas d'échec essaie de se reconnecter
         if self.__bdd.verifierConnexionBdd() == False:
            self.__bdd.refaireConnexionBdd()
         if self.__bdd.get_codeResult() != 0:
            raise ValueError  # lève exception si échec connexion
         sqlQuery = " SELECT j.id, j.date_heure, a.code, a.nom " \
            "FROM journal j INNER JOIN action a ON j.id_action = a.id " \
            "ORDER BY j.id"
         self.__bdd.afficherResultatReqSelect(sqlQuery)
         if not self.__bdd.get_resultReqSelect():
            # Aucune action mémorisée dans la bdd
            print("0 action mémorisée dans la bdd")
      except:
         pass

   def afficherActionMemBdd(self, debug=False):
      """ Affiche les actions mémorisées dans la table journal de la bdd
      """
      fonction ="CGestionSav:afficherActionMemBdd()"
      message = "\n----- Affichage des actions mémorisées dans la bdd dbsav -----"
      print(message)
      self.logger.debug("{} -- {}".format(message, fonction))
      try:
         # vérifie la connexion de la bdd et en cas d'échec essaie de se reconnecter
         if self.__bdd.verifierConnexionBdd() == False:
            self.__bdd.refaireConnexionBdd()
         if self.__bdd.get_codeResult() != 0:
            raise ValueError  # lève exception si échec connexion
         sqlQuery = " SELECT j.id, j.date_heure, a.code, a.nom " \
            "FROM journal j INNER JOIN action a ON j.id_action = a.id " \
            "ORDER BY j.id"
         self.__bdd.executerReqSelect(sqlQuery)
         resultReq = self.__bdd.get_resultReqSelect()
         if resultReq:
            # il existe des actions mémorisées
            for ligne in resultReq:
               for index, col in enumerate(ligne):
                  if index != 1:
                     # champ différent de datetime
                     print("{}   ".format(col), end='')
                  else:
                     print("{}   ".format(col.strftime("%Y-%m-%d %H:%M:%S")), end='')
               print("")
         else:
            print("0 action mémorisée dans la bdd")
      except:
         pass
            
   def effacerActionMemBdd(self):
      """ Efface toutes les actions enregistrées dans la bdd. 
          Autrement dit efface toutes les données de la table journal
      """
      fonction ="CGestionSav:effacerActionMemBdd()"
      try:
         # vérifie la connexion de la bdd et en cas d'échec essaie de se reconnecter
         if self.__bdd.verifierConnexionBdd() == False:
            self.__bdd.refaireConnexionBdd()
         if self.__bdd.get_codeResult() != 0:
            raise ValueError  # lève exception si échec connexion
         sqlQuery = " SELECT id from journal"
         self.__bdd.executerReqSelect(sqlQuery)
         resultReq = self.__bdd.get_resultReqSelect()
         message = "\n----- EFFACEMENT des {} actions mémorisées dans la bdd dbsav -----" \
            .format(len(resultReq))
         print(message)
         self.logger.debug(message)
         for ligne in resultReq:
            idVal = ligne[0]   # récupère valeur id de la table
            sqlQuery = "DELETE FROM journal WHERE id = {}".format(idVal)
            self.__bdd.executerReqInsUpdDel(sqlQuery)
      except:
         pass
   
if __name__ == "__main__":
   CLogger.effacerFichierLog("debugSav.log")
   # ----- Mise en place du logger qui va gérer les handlers console et fichier rotatif
   loggerSav = CLogger(loggerName="debugSav", loggerLevel="DEBUG", \
                       consoleLevel="INFO", fileName="debugSav.log", fileLevel="DEBUG")      
   # ---- Création d'un objet 'Interface connexion bdd', cela teste aussi l'accès à la bdd -------
   # créer une connexion à la bdd
   paramBdd = ("192.168.0.20", 3306, "user_sav", "password", "dbsav")
   #paramBdd = ("10.16.3.232", 3306, "user_dbsav", "password", "dbsav")
   bdd = CConnexionMysql(paramBdd, loggerSav)
   if bdd.get_codeResult() != 0:
      # échec connexion à bdd
      print("!!! Echec connexion à bdd -> destruction objet interface bdd2 !!!")
      bdd = None    # destruction de l'objet
      time.sleep(1)      
   else:
      # Succès connexion à la bdd   
   
      sav = CGestionSav(bdd, loggerSav)
   #   sav.mettreEnBddAction()
      sav.mettreEnBddAction('R')
      sav.mettreEnBddAction('E')
      sav.mettreEnBddAction('R')
      sav.mettreEnBddAction('D')
      sav.afficherActionMemBddBrut()
      sav.afficherActionMemBdd()
      time.sleep(1)
      sav.effacerActionMemBdd()
      time.sleep(1)
      sav.afficherActionMemBdd()
      time.sleep(1)
      bdd.seDeconnecterBdd()
      bdd = None   # destruction objet
      time.sleep(1)
      print("\nFin programme CGestionSav.py")
   
