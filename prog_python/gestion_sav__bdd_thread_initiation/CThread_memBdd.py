#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : CThread_memBdd.py      version 1.0
Date : 02-04-2018
Auteur : Hervé Dugast

Fonctionnement
   Lance 2 threads affichant la liste des nombres premiers inférieurs à une certaine valeur, dans 
   l'ordre, au fur et à mesure de son élaboration et à une vitesse différente.

------- affichage console ------------------------------------------------------

--------------------------------------------------------------------------------
"""

from threading import Thread
from time import sleep
from CConnexionMysql import CConnexionMysql
from datetime import datetime

class CThread_memBdd(Thread): 
   
   def __init__(self, nom='', codeAction='0', nbEssais=20, dureeAttente=1, verbeux=False): 
      """ constructeur
      """
      Thread.__init__(self) 
      self.__nom = nom 
      self.__codeAction = codeAction
      self.__nbEssais = nbEssais
      self.__dureeAttente = dureeAttente
      self.__verbeux = verbeux
      # préparation date_heure,format str   (exemple : '2018-03-30 17:45:21')
      self.__dateHeureBdd = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

   def run(self): 
      self.__gererMiseEnBdd()
      
   def __gererMiseEnBdd(self):
      """ Gère les opérations de mise en base de données. Répète ces opérations nb fois en cas 
          d'erreurs avant d'abandonner. Chaque essai est espacé de x minutes.
      """
      numEssai = 1
      while numEssai <= self.__nbEssais:
         dateHeure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         if self.__verbeux:
            print("\n{} == INFO == Exécution Thread {} essai n°{}, Mémorisation en Bdd " \
                  "codeAction = '{}'".format(dateHeure, self.__nom, numEssai, self.__codeAction))
         codeResult = self.__mettreEnBddAction()
         if codeResult != 0:
            dateHeure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("{} == ERROR == Echec mémorisation en Bdd codeAction = '{}'" \
                  .format(dateHeure, self.__codeAction))
            numEssai += 1
            if numEssai <= self.__nbEssais:
               print("    Prochain essai de mémorisation dans {} secondes". \
                     format(self.__dureeAttente))
            else:
               print("   Tous les essais ont échoué ! Abandon opération ! ")
            sleep(self.__dureeAttente)
         else:
            if self.__verbeux:
               print("* Succès mémorisation codeAction = '{}'".format(self.__codeAction))
            
      
   def __creerConnexionABdd(self):
      """ Crée un objet connexion à la bdd. 
          Retour : objet connexion
      """
      # self.__verbeux -> True, affiche des informations sur les opérations exécutées avec succès
      return CConnexionMysql.creerInterfaceBdd_dbsav(self.__verbeux)      
   
   def __mettreEnBddAction(self):
      """ Mémorise une action en bdd 
          Retour int : codeResult = 0 -> succès     codeResult > 0 -> Echec
      """
      # ----- Vérification validité du code action à mémoriser dans la bdd -----
      # création d'un objet connexion à la bdd
      bdd = self.__creerConnexionABdd()
      # récupération des actions mémorisées dans la bdd (actions possibles)
      sqlQuery = "SELECT code FROM action"
      bdd.executerReqSelect(sqlQuery)
      codeActionListTemp = bdd.get_resultReqSelect()
      # codeActionListTemp est une liste contenant une autre liste (ex: [('R',),('E',),('D',)]
      # transformation de codeActionListTemp en une liste simple (ex. ['R', 'E', 'D'])
      codeActionList = []
      for code in codeActionListTemp:
         codeActionList.append(code[0])
      # vérification validitité de code action à mémoriser dans la bdd
      if self.__codeAction != '0' and self.__codeAction not in codeActionList:
         print("Erreur ! Code action '{}' non valide !".format(self.__codeAction))
      else:
         # Demande de saisie d'une action jusqu'à ce qu'elle soit valide
         while self.__codeAction not in codeActionList:
            self.__codeAction = input("Saisir un code action parmi {} ? ".format(codeActionList))
            if self.__codeAction not in codeActionList:
               print("Erreur ! Code action '{}' non valide !".format(self.__codeAction))
      
      # ----- mise en base de données l'action -----
      # récupération valeur du champ id de l'action à mémoriser
      idAction = bdd.recupererValeurId('action', self.__codeAction)
      if idAction != -1:
         # la valeur de idAction est valide
         sqlQuery = "INSERT INTO journal (date_heure, id_action) VALUES ('{}', {})" \
            .format(self.__dateHeureBdd, idAction)
      bdd.executerReqInsUpdDel(sqlQuery) 

         
if __name__ == "__main__":
   bdd1 = CThread_memBdd(nom="bdd-1", codeAction='Dg', nbEssais=3, dureeAttente=3, verbeux=False)
   bdd1.start()
   bdd1.join()
   print("\n--- Fin programme CThread_memBdd.py ---")