#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : CGestionSavThread.py      version 1.3
Date : 02-05-2018
Auteur : Hervé Dugast

Fonctionnement :
   Gère les retours de matériel en panne. Mémorise en base de données le type d'intervention 
   effectué parmi : 'R', 'E' ou 'D'.
       'R' : Réparation du matériel    'E' : Echange     'D' : Devis, dommages hors garantie
   Toutes les opérations sont journalisées en mode DEBUG dans le fichier debugSav.log.
   Les erreurs et problèmes de connexion sont gérés.
   Chaque demande de mise en bdd est effectuée à l'aide d'un thread. Ainsi, le programme principal
   n'est pas bloqué en cas d'échec de connexion à la bdd. En cas d'échec, le thread essaiera
   un nombre de fois défini de mettre en bdd avec un temps défini entre chaque essai.

------- affichage console --------------------------------------------------------------------------
*** Connexion à la bdd : host=192.168.0.20, port=3306, user=user_sav, password=password, database=dbsav

----- EFFACEMENT des 10 actions mémorisées dans la bdd dbsav -----
Thread-1 2018-05-03 17:37:15.755664
  *** Mise en bdd de l'action 'R'
  * Succès mise en base de codeAction 'R'
Thread-2 2018-05-03 17:37:16.762701
  *** Mise en bdd de l'action 'R'
  * Succès mise en base de codeAction 'R'
Thread-3 2018-05-03 17:37:17.768057
  *** Mise en bdd de l'action 'R'
  * Succès mise en base de codeAction 'R'
Thread-4 2018-05-03 17:37:18.773280
  *** Mise en bdd de l'action 'R'
  * Succès mise en base de codeAction 'R'
Thread-5 2018-05-03 17:37:19.777735
  *** Mise en bdd de l'action 'R'
  * Succès mise en base de codeAction 'R'
Thread-6 2018-05-03 17:37:20.782940
  *** Mise en bdd de l'action 'R'
*** Essai reconnexion à la bdd : host=192.168.0.20, port=3306, user=user_sav, password=password, database=dbsav
2018-05-03 17:37:21,803 -- ERROR -- code 3 
2003: Can't connect to MySQL server on '192.168.0.20:3306' (10061 Aucune connexion n’a pu être établie car l’ordinateur cible l’a expressément refusée) -- CConnexionMysql.CConnexionMysql:self.__seConnecter()
2018-05-03 17:37:21,805 -- ERROR -- code 102, échec mise en bdd codeAction 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:21,806 -- ERROR -- Thread-6. Echec mise en bdd action 'R'. Reste 4 essai(s). Prochaine tentative dans 3 secondes -- CGestionSavThread.CThreadMemBdd:run()
Thread-7 2018-05-03 17:37:21.807343
  *** Mise en bdd de l'action 'R'
*** Essai reconnexion à la bdd : host=192.168.0.20, port=3306, user=user_sav, password=password, database=dbsav
2018-05-03 17:37:22,819 -- ERROR -- code 3 
2003: Can't connect to MySQL server on '192.168.0.20:3306' (10061 Aucune connexion n’a pu être établie car l’ordinateur cible l’a expressément refusée) -- CConnexionMysql.CConnexionMysql:self.__seConnecter()
2018-05-03 17:37:22,820 -- ERROR -- code 102, échec mise en bdd codeAction 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:22,821 -- ERROR -- Thread-7. Echec mise en bdd action 'R'. Reste 4 essai(s). Prochaine tentative dans 3 secondes -- CGestionSavThread.CThreadMemBdd:run()
Thread-8 2018-05-03 17:37:22.821322
  *** Mise en bdd de l'action 'R'
*** Essai reconnexion à la bdd : host=192.168.0.20, port=3306, user=user_sav, password=password, database=dbsav
2018-05-03 17:37:23,829 -- ERROR -- code 3 
2003: Can't connect to MySQL server on '192.168.0.20:3306' (10061 Aucune connexion n’a pu être établie car l’ordinateur cible l’a expressément refusée) -- CConnexionMysql.CConnexionMysql:self.__seConnecter()
2018-05-03 17:37:23,831 -- ERROR -- code 102, échec mise en bdd codeAction 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:23,832 -- ERROR -- Thread-8. Echec mise en bdd action 'R'. Reste 4 essai(s). Prochaine tentative dans 3 secondes -- CGestionSavThread.CThreadMemBdd:run()
Thread-9 2018-05-03 17:37:23.832870
  *** Mise en bdd de l'action 'R'
*** Essai reconnexion à la bdd : host=192.168.0.20, port=3306, user=user_sav, password=password, database=dbsav
  * Succès mise en base de codeAction 'R'
Thread-10 2018-05-03 17:37:24.884738
  *** Mise en bdd de l'action 'R'
  * Succès mise en base de codeAction 'R'
Thread-6 2018-05-03 17:37:24.902264
  *** Mise en bdd de l'action 'R'
  * Succès mise en base de codeAction 'R'
Thread-7 2018-05-03 17:37:25.822376
  *** Mise en bdd de l'action 'R'
  * Succès mise en base de codeAction 'R'
Thread-8 2018-05-03 17:37:26.834373
  *** Mise en bdd de l'action 'R'
  * Succès mise en base de codeAction 'R'

----- Affichage des actions mémorisées dans la bdd dbsav -----
333   2018-05-03 17:37:16   R   Réparation   
334   2018-05-03 17:37:17   R   Réparation   
335   2018-05-03 17:37:18   R   Réparation   
336   2018-05-03 17:37:19   R   Réparation   
337   2018-05-03 17:37:20   R   Réparation   
338   2018-05-03 17:37:24   R   Réparation   
339   2018-05-03 17:37:25   R   Réparation   
340   2018-05-03 17:37:21   R   Réparation   
341   2018-05-03 17:37:22   R   Réparation   
342   2018-05-03 17:37:23   R   Réparation   

Fin programme CGestionSav.py
----------------------------------------------------------------------------------------------------

--------------- Contenu fichier debugSav.log -------------------------------------------------------
2018-05-03 17:37:15,579 -- DEBUG -- *** Connexion à la bdd : host=192.168.0.20, port=3306, user=user_sav, password=password, database=dbsav -- CConnexionMysql.CConnexionMysql:self.__init__(host=192.168.0.20, port=3306, user=user_sav, password=password, database=dbsav)
2018-05-03 17:37:15,584 -- DEBUG -- * Succès connexion à la bdd * -- CConnexionMysql.CConnexionMysql:self.__init__(host=192.168.0.20, port=3306, user=user_sav, password=password, database=dbsav)
2018-05-03 17:37:15,585 -- DEBUG -- Création d'un objet 'CGestionSav' avec lien à bdd et logger -- CGestionSavThread.CGestionSav:self.__init__()
2018-05-03 17:37:15,586 -- DEBUG -- Vérification connexion bdd : Succès -- CConnexionMysql.CConnexionMysql:self.verifierConnexionBdd()
2018-05-03 17:37:15,590 -- DEBUG -- * Succès exécution requête :
 SELECT id from journal 
-- CConnexionMysql.CConnexionMysql:self.executerReqSelect()
2018-05-03 17:37:15,591 -- DEBUG -- 
----- EFFACEMENT des 10 actions mémorisées dans la bdd dbsav -----
2018-05-03 17:37:15,596 -- DEBUG -- * Succès exécution requête :
DELETE FROM journal WHERE id = 323 
-- CConnexionMysql.CConnexionMysql:self.executerReqInsUpdDel()
2018-05-03 17:37:15,602 -- DEBUG -- * Succès exécution requête :
DELETE FROM journal WHERE id = 324 
-- CConnexionMysql.CConnexionMysql:self.executerReqInsUpdDel()
2018-05-03 17:37:15,607 -- DEBUG -- * Succès exécution requête :
DELETE FROM journal WHERE id = 325 
-- CConnexionMysql.CConnexionMysql:self.executerReqInsUpdDel()
2018-05-03 17:37:15,612 -- DEBUG -- * Succès exécution requête :
DELETE FROM journal WHERE id = 326 
-- CConnexionMysql.CConnexionMysql:self.executerReqInsUpdDel()
2018-05-03 17:37:15,620 -- DEBUG -- * Succès exécution requête :
DELETE FROM journal WHERE id = 327 
-- CConnexionMysql.CConnexionMysql:self.executerReqInsUpdDel()
2018-05-03 17:37:15,626 -- DEBUG -- * Succès exécution requête :
DELETE FROM journal WHERE id = 328 
-- CConnexionMysql.CConnexionMysql:self.executerReqInsUpdDel()
2018-05-03 17:37:15,633 -- DEBUG -- * Succès exécution requête :
DELETE FROM journal WHERE id = 329 
-- CConnexionMysql.CConnexionMysql:self.executerReqInsUpdDel()
2018-05-03 17:37:15,640 -- DEBUG -- * Succès exécution requête :
DELETE FROM journal WHERE id = 330 
-- CConnexionMysql.CConnexionMysql:self.executerReqInsUpdDel()
2018-05-03 17:37:15,645 -- DEBUG -- * Succès exécution requête :
DELETE FROM journal WHERE id = 331 
-- CConnexionMysql.CConnexionMysql:self.executerReqInsUpdDel()
2018-05-03 17:37:15,651 -- DEBUG -- * Succès exécution requête :
DELETE FROM journal WHERE id = 332 
-- CConnexionMysql.CConnexionMysql:self.executerReqInsUpdDel()
2018-05-03 17:37:15,652 -- DEBUG -- PROG PRINCIPAL. Demande mise en bdd action 'R' -- CGestionSavThread, main
2018-05-03 17:37:15,653 -- DEBUG -- Création d'un objet 'CThreadMemBdd' avec lien à bdd et logger -- CGestionSavThread.CThreadMemBdd:self.__init__()
2018-05-03 17:37:15,654 -- DEBUG -- Thread-1 lancé pour mémoriser l'action en bdd -- CGestionSavThread.CGestionSav:mettreEnBddActionThread()
2018-05-03 17:37:15,755 -- DEBUG -- Thread-1. Essai 1/5 : demande mise en bdd action 'R' -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:15,756 -- DEBUG --   *** Mise en bdd de l'action 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:15,757 -- DEBUG -- Vérification connexion bdd : Succès -- CConnexionMysql.CConnexionMysql:self.verifierConnexionBdd()
2018-05-03 17:37:15,762 -- DEBUG -- * Succès exécution requête :
SELECT code FROM action 
-- CConnexionMysql.CConnexionMysql:self.executerReqSelect()
2018-05-03 17:37:15,764 -- DEBUG -- * Succès exécution requête :
SELECT id FROM action WHERE code LIKE 'R' 
-- CConnexionMysql.CConnexionMysql:self.executerReqSelect()
2018-05-03 17:37:15,769 -- DEBUG -- * Succès exécution requête :
INSERT INTO journal (date_heure, id_action) VALUES ('2018-05-03 17:37:15.653876', 1) 
-- CConnexionMysql.CConnexionMysql:self.executerReqInsUpdDel()
2018-05-03 17:37:15,770 -- DEBUG --   * Succès mise en base de codeAction 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:15,771 -- DEBUG -- Thread-1. Succès mise en bdd action 'R' -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:15,771 -- DEBUG -- Thread-1. Fin thread. -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:16,656 -- DEBUG -- PROG PRINCIPAL. Demande mise en bdd action 'R' -- CGestionSavThread, main
2018-05-03 17:37:16,658 -- DEBUG -- Création d'un objet 'CThreadMemBdd' avec lien à bdd et logger -- CGestionSavThread.CThreadMemBdd:self.__init__()
2018-05-03 17:37:16,662 -- DEBUG -- Thread-2 lancé pour mémoriser l'action en bdd -- CGestionSavThread.CGestionSav:mettreEnBddActionThread()
2018-05-03 17:37:16,762 -- DEBUG -- Thread-2. Essai 1/5 : demande mise en bdd action 'R' -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:16,765 -- DEBUG --   *** Mise en bdd de l'action 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:16,767 -- DEBUG -- Vérification connexion bdd : Succès -- CConnexionMysql.CConnexionMysql:self.verifierConnexionBdd()
2018-05-03 17:37:16,772 -- DEBUG -- * Succès exécution requête :
SELECT code FROM action 
-- CConnexionMysql.CConnexionMysql:self.executerReqSelect()
2018-05-03 17:37:16,775 -- DEBUG -- * Succès exécution requête :
SELECT id FROM action WHERE code LIKE 'R' 
-- CConnexionMysql.CConnexionMysql:self.executerReqSelect()
2018-05-03 17:37:16,784 -- DEBUG -- * Succès exécution requête :
INSERT INTO journal (date_heure, id_action) VALUES ('2018-05-03 17:37:16.658631', 1) 
-- CConnexionMysql.CConnexionMysql:self.executerReqInsUpdDel()
2018-05-03 17:37:16,785 -- DEBUG --   * Succès mise en base de codeAction 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:16,786 -- DEBUG -- Thread-2. Succès mise en bdd action 'R' -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:16,787 -- DEBUG -- Thread-2. Fin thread. -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:17,663 -- DEBUG -- PROG PRINCIPAL. Demande mise en bdd action 'R' -- CGestionSavThread, main
2018-05-03 17:37:17,666 -- DEBUG -- Création d'un objet 'CThreadMemBdd' avec lien à bdd et logger -- CGestionSavThread.CThreadMemBdd:self.__init__()
2018-05-03 17:37:17,668 -- DEBUG -- Thread-3 lancé pour mémoriser l'action en bdd -- CGestionSavThread.CGestionSav:mettreEnBddActionThread()
2018-05-03 17:37:17,768 -- DEBUG -- Thread-3. Essai 1/5 : demande mise en bdd action 'R' -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:17,769 -- DEBUG --   *** Mise en bdd de l'action 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:17,771 -- DEBUG -- Vérification connexion bdd : Succès -- CConnexionMysql.CConnexionMysql:self.verifierConnexionBdd()
2018-05-03 17:37:17,775 -- DEBUG -- * Succès exécution requête :
SELECT code FROM action 
-- CConnexionMysql.CConnexionMysql:self.executerReqSelect()
2018-05-03 17:37:17,779 -- DEBUG -- * Succès exécution requête :
SELECT id FROM action WHERE code LIKE 'R' 
-- CConnexionMysql.CConnexionMysql:self.executerReqSelect()
2018-05-03 17:37:17,787 -- DEBUG -- * Succès exécution requête :
INSERT INTO journal (date_heure, id_action) VALUES ('2018-05-03 17:37:17.665584', 1) 
-- CConnexionMysql.CConnexionMysql:self.executerReqInsUpdDel()
2018-05-03 17:37:17,788 -- DEBUG --   * Succès mise en base de codeAction 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:17,789 -- DEBUG -- Thread-3. Succès mise en bdd action 'R' -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:17,791 -- DEBUG -- Thread-3. Fin thread. -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:18,670 -- DEBUG -- PROG PRINCIPAL. Demande mise en bdd action 'R' -- CGestionSavThread, main
2018-05-03 17:37:18,671 -- DEBUG -- Création d'un objet 'CThreadMemBdd' avec lien à bdd et logger -- CGestionSavThread.CThreadMemBdd:self.__init__()
2018-05-03 17:37:18,672 -- DEBUG -- Thread-4 lancé pour mémoriser l'action en bdd -- CGestionSavThread.CGestionSav:mettreEnBddActionThread()
2018-05-03 17:37:18,773 -- DEBUG -- Thread-4. Essai 1/5 : demande mise en bdd action 'R' -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:18,774 -- DEBUG --   *** Mise en bdd de l'action 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:18,776 -- DEBUG -- Vérification connexion bdd : Succès -- CConnexionMysql.CConnexionMysql:self.verifierConnexionBdd()
2018-05-03 17:37:18,781 -- DEBUG -- * Succès exécution requête :
SELECT code FROM action 
-- CConnexionMysql.CConnexionMysql:self.executerReqSelect()
2018-05-03 17:37:18,785 -- DEBUG -- * Succès exécution requête :
SELECT id FROM action WHERE code LIKE 'R' 
-- CConnexionMysql.CConnexionMysql:self.executerReqSelect()
2018-05-03 17:37:18,792 -- DEBUG -- * Succès exécution requête :
INSERT INTO journal (date_heure, id_action) VALUES ('2018-05-03 17:37:18.671332', 1) 
-- CConnexionMysql.CConnexionMysql:self.executerReqInsUpdDel()
2018-05-03 17:37:18,794 -- DEBUG --   * Succès mise en base de codeAction 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:18,795 -- DEBUG -- Thread-4. Succès mise en bdd action 'R' -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:18,796 -- DEBUG -- Thread-4. Fin thread. -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:19,673 -- DEBUG -- PROG PRINCIPAL. Demande mise en bdd action 'R' -- CGestionSavThread, main
2018-05-03 17:37:19,675 -- DEBUG -- Création d'un objet 'CThreadMemBdd' avec lien à bdd et logger -- CGestionSavThread.CThreadMemBdd:self.__init__()
2018-05-03 17:37:19,677 -- DEBUG -- Thread-5 lancé pour mémoriser l'action en bdd -- CGestionSavThread.CGestionSav:mettreEnBddActionThread()
2018-05-03 17:37:19,777 -- DEBUG -- Thread-5. Essai 1/5 : demande mise en bdd action 'R' -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:19,779 -- DEBUG --   *** Mise en bdd de l'action 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:19,781 -- DEBUG -- Vérification connexion bdd : Succès -- CConnexionMysql.CConnexionMysql:self.verifierConnexionBdd()
2018-05-03 17:37:19,785 -- DEBUG -- * Succès exécution requête :
SELECT code FROM action 
-- CConnexionMysql.CConnexionMysql:self.executerReqSelect()
2018-05-03 17:37:19,789 -- DEBUG -- * Succès exécution requête :
SELECT id FROM action WHERE code LIKE 'R' 
-- CConnexionMysql.CConnexionMysql:self.executerReqSelect()
2018-05-03 17:37:19,799 -- DEBUG -- * Succès exécution requête :
INSERT INTO journal (date_heure, id_action) VALUES ('2018-05-03 17:37:19.675107', 1) 
-- CConnexionMysql.CConnexionMysql:self.executerReqInsUpdDel()
2018-05-03 17:37:19,800 -- DEBUG --   * Succès mise en base de codeAction 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:19,801 -- DEBUG -- Thread-5. Succès mise en bdd action 'R' -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:19,802 -- DEBUG -- Thread-5. Fin thread. -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:20,678 -- DEBUG -- PROG PRINCIPAL. Demande mise en bdd action 'R' -- CGestionSavThread, main
2018-05-03 17:37:20,680 -- DEBUG -- Création d'un objet 'CThreadMemBdd' avec lien à bdd et logger -- CGestionSavThread.CThreadMemBdd:self.__init__()
2018-05-03 17:37:20,682 -- DEBUG -- Thread-6 lancé pour mémoriser l'action en bdd -- CGestionSavThread.CGestionSav:mettreEnBddActionThread()
2018-05-03 17:37:20,782 -- DEBUG -- Thread-6. Essai 1/5 : demande mise en bdd action 'R' -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:20,784 -- DEBUG --   *** Mise en bdd de l'action 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:20,786 -- DEBUG -- Vérification connexion bdd : Succès -- CConnexionMysql.CConnexionMysql:self.verifierConnexionBdd()
2018-05-03 17:37:20,799 -- DEBUG -- *** Essai reconnexion à la bdd : host=192.168.0.20, port=3306, user=user_sav, password=password, database=dbsav -- CConnexionMysql.CConnexionMysql:self.__seConnecter()
2018-05-03 17:37:21,684 -- DEBUG -- PROG PRINCIPAL. Demande mise en bdd action 'R' -- CGestionSavThread, main
2018-05-03 17:37:21,687 -- DEBUG -- Création d'un objet 'CThreadMemBdd' avec lien à bdd et logger -- CGestionSavThread.CThreadMemBdd:self.__init__()
2018-05-03 17:37:21,689 -- DEBUG -- Thread-7 lancé pour mémoriser l'action en bdd -- CGestionSavThread.CGestionSav:mettreEnBddActionThread()
2018-05-03 17:37:21,803 -- ERROR -- code 3 
2003: Can't connect to MySQL server on '192.168.0.20:3306' (10061 Aucune connexion n’a pu être établie car l’ordinateur cible l’a expressément refusée) -- CConnexionMysql.CConnexionMysql:self.__seConnecter()
2018-05-03 17:37:21,805 -- ERROR -- code 102, échec mise en bdd codeAction 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:21,806 -- ERROR -- Thread-6. Echec mise en bdd action 'R'. Reste 4 essai(s). Prochaine tentative dans 3 secondes -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:21,807 -- DEBUG -- Thread-7. Essai 1/5 : demande mise en bdd action 'R' -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:21,809 -- DEBUG --   *** Mise en bdd de l'action 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:21,811 -- DEBUG -- Vérification connexion bdd : Echec -- CConnexionMysql.CConnexionMysql:self.verifierConnexionBdd()
2018-05-03 17:37:21,813 -- DEBUG -- *** Essai reconnexion à la bdd : host=192.168.0.20, port=3306, user=user_sav, password=password, database=dbsav -- CConnexionMysql.CConnexionMysql:self.__seConnecter()
2018-05-03 17:37:22,691 -- DEBUG -- PROG PRINCIPAL. Demande mise en bdd action 'R' -- CGestionSavThread, main
2018-05-03 17:37:22,693 -- DEBUG -- Création d'un objet 'CThreadMemBdd' avec lien à bdd et logger -- CGestionSavThread.CThreadMemBdd:self.__init__()
2018-05-03 17:37:22,696 -- DEBUG -- Thread-8 lancé pour mémoriser l'action en bdd -- CGestionSavThread.CGestionSav:mettreEnBddActionThread()
2018-05-03 17:37:22,819 -- ERROR -- code 3 
2003: Can't connect to MySQL server on '192.168.0.20:3306' (10061 Aucune connexion n’a pu être établie car l’ordinateur cible l’a expressément refusée) -- CConnexionMysql.CConnexionMysql:self.__seConnecter()
2018-05-03 17:37:22,820 -- ERROR -- code 102, échec mise en bdd codeAction 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:22,821 -- ERROR -- Thread-7. Echec mise en bdd action 'R'. Reste 4 essai(s). Prochaine tentative dans 3 secondes -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:22,821 -- DEBUG -- Thread-8. Essai 1/5 : demande mise en bdd action 'R' -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:22,822 -- DEBUG --   *** Mise en bdd de l'action 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:22,823 -- DEBUG -- Vérification connexion bdd : Echec -- CConnexionMysql.CConnexionMysql:self.verifierConnexionBdd()
2018-05-03 17:37:22,825 -- DEBUG -- *** Essai reconnexion à la bdd : host=192.168.0.20, port=3306, user=user_sav, password=password, database=dbsav -- CConnexionMysql.CConnexionMysql:self.__seConnecter()
2018-05-03 17:37:23,698 -- DEBUG -- PROG PRINCIPAL. Demande mise en bdd action 'R' -- CGestionSavThread, main
2018-05-03 17:37:23,699 -- DEBUG -- Création d'un objet 'CThreadMemBdd' avec lien à bdd et logger -- CGestionSavThread.CThreadMemBdd:self.__init__()
2018-05-03 17:37:23,701 -- DEBUG -- Thread-9 lancé pour mémoriser l'action en bdd -- CGestionSavThread.CGestionSav:mettreEnBddActionThread()
2018-05-03 17:37:23,829 -- ERROR -- code 3 
2003: Can't connect to MySQL server on '192.168.0.20:3306' (10061 Aucune connexion n’a pu être établie car l’ordinateur cible l’a expressément refusée) -- CConnexionMysql.CConnexionMysql:self.__seConnecter()
2018-05-03 17:37:23,831 -- ERROR -- code 102, échec mise en bdd codeAction 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:23,832 -- ERROR -- Thread-8. Echec mise en bdd action 'R'. Reste 4 essai(s). Prochaine tentative dans 3 secondes -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:23,833 -- DEBUG -- Thread-9. Essai 1/5 : demande mise en bdd action 'R' -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:23,835 -- DEBUG --   *** Mise en bdd de l'action 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:23,836 -- DEBUG -- Vérification connexion bdd : Echec -- CConnexionMysql.CConnexionMysql:self.verifierConnexionBdd()
2018-05-03 17:37:23,838 -- DEBUG -- *** Essai reconnexion à la bdd : host=192.168.0.20, port=3306, user=user_sav, password=password, database=dbsav -- CConnexionMysql.CConnexionMysql:self.__seConnecter()
2018-05-03 17:37:24,703 -- DEBUG -- PROG PRINCIPAL. Demande mise en bdd action 'R' -- CGestionSavThread, main
2018-05-03 17:37:24,704 -- DEBUG -- Création d'un objet 'CThreadMemBdd' avec lien à bdd et logger -- CGestionSavThread.CThreadMemBdd:self.__init__()
2018-05-03 17:37:24,706 -- DEBUG -- Thread-10 lancé pour mémoriser l'action en bdd -- CGestionSavThread.CGestionSav:mettreEnBddActionThread()
2018-05-03 17:37:24,855 -- DEBUG -- * Succès connexion à la bdd * -- CConnexionMysql.CConnexionMysql:self.__seConnecter()
2018-05-03 17:37:24,868 -- DEBUG -- * Succès exécution requête :
SELECT code FROM action 
-- CConnexionMysql.CConnexionMysql:self.executerReqSelect()
2018-05-03 17:37:24,872 -- DEBUG -- * Succès exécution requête :
SELECT id FROM action WHERE code LIKE 'R' 
-- CConnexionMysql.CConnexionMysql:self.executerReqSelect()
2018-05-03 17:37:24,883 -- DEBUG -- * Succès exécution requête :
INSERT INTO journal (date_heure, id_action) VALUES ('2018-05-03 17:37:23.699816', 1) 
-- CConnexionMysql.CConnexionMysql:self.executerReqInsUpdDel()
2018-05-03 17:37:24,884 -- DEBUG --   * Succès mise en base de codeAction 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:24,884 -- DEBUG -- Thread-9. Succès mise en bdd action 'R' -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:24,885 -- DEBUG -- Thread-10. Essai 1/5 : demande mise en bdd action 'R' -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:24,885 -- DEBUG -- Thread-9. Fin thread. -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:24,886 -- DEBUG --   *** Mise en bdd de l'action 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:24,887 -- DEBUG -- Vérification connexion bdd : Succès -- CConnexionMysql.CConnexionMysql:self.verifierConnexionBdd()
2018-05-03 17:37:24,890 -- DEBUG -- * Succès exécution requête :
SELECT code FROM action 
-- CConnexionMysql.CConnexionMysql:self.executerReqSelect()
2018-05-03 17:37:24,892 -- DEBUG -- * Succès exécution requête :
SELECT id FROM action WHERE code LIKE 'R' 
-- CConnexionMysql.CConnexionMysql:self.executerReqSelect()
2018-05-03 17:37:24,900 -- DEBUG -- * Succès exécution requête :
INSERT INTO journal (date_heure, id_action) VALUES ('2018-05-03 17:37:24.704979', 1) 
-- CConnexionMysql.CConnexionMysql:self.executerReqInsUpdDel()
2018-05-03 17:37:24,901 -- DEBUG --   * Succès mise en base de codeAction 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:24,901 -- DEBUG -- Thread-10. Succès mise en bdd action 'R' -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:24,902 -- DEBUG -- Thread-6. Essai 2/5 : demande mise en bdd action 'R' -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:24,902 -- DEBUG -- Thread-10. Fin thread. -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:24,903 -- DEBUG --   *** Mise en bdd de l'action 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:24,905 -- DEBUG -- Vérification connexion bdd : Succès -- CConnexionMysql.CConnexionMysql:self.verifierConnexionBdd()
2018-05-03 17:37:24,908 -- DEBUG -- * Succès exécution requête :
SELECT code FROM action 
-- CConnexionMysql.CConnexionMysql:self.executerReqSelect()
2018-05-03 17:37:24,910 -- DEBUG -- * Succès exécution requête :
SELECT id FROM action WHERE code LIKE 'R' 
-- CConnexionMysql.CConnexionMysql:self.executerReqSelect()
2018-05-03 17:37:24,918 -- DEBUG -- * Succès exécution requête :
INSERT INTO journal (date_heure, id_action) VALUES ('2018-05-03 17:37:20.680248', 1) 
-- CConnexionMysql.CConnexionMysql:self.executerReqInsUpdDel()
2018-05-03 17:37:24,919 -- DEBUG --   * Succès mise en base de codeAction 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:24,919 -- DEBUG -- Thread-6. Succès mise en bdd action 'R' -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:24,920 -- DEBUG -- Thread-6. Fin thread. -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:25,822 -- DEBUG -- Thread-7. Essai 2/5 : demande mise en bdd action 'R' -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:25,823 -- DEBUG --   *** Mise en bdd de l'action 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:25,825 -- DEBUG -- Vérification connexion bdd : Succès -- CConnexionMysql.CConnexionMysql:self.verifierConnexionBdd()
2018-05-03 17:37:25,829 -- DEBUG -- * Succès exécution requête :
SELECT code FROM action 
-- CConnexionMysql.CConnexionMysql:self.executerReqSelect()
2018-05-03 17:37:25,832 -- DEBUG -- * Succès exécution requête :
SELECT id FROM action WHERE code LIKE 'R' 
-- CConnexionMysql.CConnexionMysql:self.executerReqSelect()
2018-05-03 17:37:25,839 -- DEBUG -- * Succès exécution requête :
INSERT INTO journal (date_heure, id_action) VALUES ('2018-05-03 17:37:21.686773', 1) 
-- CConnexionMysql.CConnexionMysql:self.executerReqInsUpdDel()
2018-05-03 17:37:25,841 -- DEBUG --   * Succès mise en base de codeAction 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:25,842 -- DEBUG -- Thread-7. Succès mise en bdd action 'R' -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:25,843 -- DEBUG -- Thread-7. Fin thread. -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:26,834 -- DEBUG -- Thread-8. Essai 2/5 : demande mise en bdd action 'R' -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:26,835 -- DEBUG --   *** Mise en bdd de l'action 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:26,837 -- DEBUG -- Vérification connexion bdd : Succès -- CConnexionMysql.CConnexionMysql:self.verifierConnexionBdd()
2018-05-03 17:37:26,841 -- DEBUG -- * Succès exécution requête :
SELECT code FROM action 
-- CConnexionMysql.CConnexionMysql:self.executerReqSelect()
2018-05-03 17:37:26,845 -- DEBUG -- * Succès exécution requête :
SELECT id FROM action WHERE code LIKE 'R' 
-- CConnexionMysql.CConnexionMysql:self.executerReqSelect()
2018-05-03 17:37:26,854 -- DEBUG -- * Succès exécution requête :
INSERT INTO journal (date_heure, id_action) VALUES ('2018-05-03 17:37:22.693362', 1) 
-- CConnexionMysql.CConnexionMysql:self.executerReqInsUpdDel()
2018-05-03 17:37:26,855 -- DEBUG --   * Succès mise en base de codeAction 'R' -- CGestionSavThread.CGestionSav:mettreEnBddAction()
2018-05-03 17:37:26,856 -- DEBUG -- Thread-8. Succès mise en bdd action 'R' -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:26,858 -- DEBUG -- Thread-8. Fin thread. -- CGestionSavThread.CThreadMemBdd:run()
2018-05-03 17:37:28,707 -- DEBUG -- 
----- Affichage des actions mémorisées dans la bdd dbsav ----- -- CGestionSavThread.CGestionSav:afficherActionMemBdd()
2018-05-03 17:37:28,710 -- DEBUG -- Vérification connexion bdd : Succès -- CConnexionMysql.CConnexionMysql:self.verifierConnexionBdd()
2018-05-03 17:37:28,716 -- DEBUG -- * Succès exécution requête :
 SELECT j.id, j.date_heure, a.code, a.nom FROM journal j INNER JOIN action a ON j.id_action = a.id ORDER BY j.id 
-- CConnexionMysql.CConnexionMysql:self.executerReqSelect()
----------------------------------------------------------------------------------------------------
"""
from CConnexionMysql import CConnexionMysql
from datetime import datetime
# classe gérant les loggers et les handlers
from CLogger import CLogger
import time
import sys
import threading

# Mise en place d'un verrou pour que la connexion à la bdd ne soit utilisée que par un seul client
# à la fois
verrou = threading.RLock()

class CGestionSav:
   """ Gère les retours de matériel en panne. Mémorise le type d'intervention effectué parmi :
       'R', 'E' ou 'D' dans une base de donnée MySQL de façon à faire des statistiques.
       'R' : Réparation du matériel    'E' : Echange     'D' : Devis, dommages hors garantie 
   """
   
   def __init__(self, bdd, logger, isHeritage=False, nbEssaiBdd=5, dureeEntreEssaiBdd=300):
      """ Constructeur
          bdd : référence à un objet "connexion bdd"
          logger : référence à un objet "logger console et fichier rotatif"
          isHeritage : boolean, différencie un objet créé par la classe mère de la classe fille, 
                       utile pour le debug (affichage création objet)
                       False : objet classe mère          True : objet classe fille (héritage)
          nbEssaiBdd : int, nombre d'essais de mise en bdd en cas d'échec
          dureeEntreEssaiBdd : int, durée (en s) entre chaque essai de mise en bdd en cas d'échec
      """
      fonction = "CGestionSavThread.CGestionSav:self.__init__()"
      self.__bdd = bdd
      self.logger = logger
      self._nbEssaiBdd = nbEssaiBdd
      self._dureeEntreEssaiBdd = dureeEntreEssaiBdd
      # _codeResult = 0 -> succès opération        _codeResult > 0 -> échec opération
      self._codeResult = 0
      # journalisation uniquement si objet classe mère 
      if not isHeritage:
         message = "Création d'un objet 'CGestionSav' avec lien à bdd et logger -- {}" \
            .format(fonction)
         self.logger.debug(message)
      
   def mettreEnBddActionThread(self, codeAction='0'):
      """ Mémorise une action en bdd à l'aide d'un thread. En cas d'échec, plusieurs autres essais
          seront tentés à un intervalle de temps défini.
          Retour int : codeResult = 0 -> succès     codeResult > 0 -> Echec
      """
      fonction ="CGestionSavThread.CGestionSav:mettreEnBddActionThread()"
      # préparation date_heure,format str   (exemple : '2018-03-30 17:45:21')
      #dateHeure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      dateHeure = datetime.now()
      thBdd = CThreadMemBdd(self.__bdd, self.logger, True, codeAction, self._nbEssaiBdd, \
                            self._dureeEntreEssaiBdd, dateHeure)
      thBdd.start()
      nomThread = thBdd.getName()
      message = "{} lancé pour mémoriser l'action en bdd -- {}" \
         .format(nomThread, fonction)
      self.logger.debug(message)
      
   def mettreEnBddAction(self, codeAction='0', dateHeure='2000-01-01 00:00:00'):
      """ Mémorise une action en bdd 
          Retour int : codeResult = 0 -> succès     codeResult > 0 -> Echec
      """
      fonction ="CGestionSavThread.CGestionSav:mettreEnBddAction()"
      message = "  *** Mise en bdd de l'action '{}'".format(codeAction)
      print(message)
      self.logger.debug("{} -- {}".format(message, fonction))
      try:
         # ----- Vérification validité du code action à mémoriser dans la bdd -----
         # vérifie la connexion de la bdd et en cas d'échec essaie de se reconnecter
         if self.__bdd.verifierConnexionBdd() == False:
            self.__bdd.refaireConnexionBdd()
         # vérifie, en cas d'essai de reconnexion, que celle-ci a réussi
         if self.__bdd.get_codeResult() != 0:
            raise ValueError  # lève exception si échec connexion
         # récupération des actions mémorisées dans la bdd (actions possibles)
         sqlQuery = "SELECT code FROM action"
         self._codeResult = self.__bdd.executerReqSelect(sqlQuery)
         if self._codeResult != 0:
            raise ValueError  # lève exception si échec exécution requête
         codeActionListTemp = self.__bdd.get_resultReqSelect()
         # codeActionListTemp est une liste contenant une autre liste (ex: [('R',),('E',),('D',)]
         # transformation de codeActionListTemp en une liste simple (ex. ['R','E','D'])
         codeActionList = []
         for code in codeActionListTemp:
            codeActionList.append(code[0])
         # vérification validitité de code action à mémoriser dans la bdd.
         if codeAction != '0' and codeAction not in codeActionList:
            # Echec, code à mémoriser non valide
            self._codeResult = 100
            raise ValueError
         else:
            # codeAction = '0' -> Demande de saisie d'une action jusqu'à ce qu'elle soit valide
            while codeAction not in codeActionList:
               codeAction = input("Saisir un code action parmi {} ? ".format(codeActionList))
               if codeAction not in codeActionList:
                  print("Erreur ! Code action '{}' non valide !".format(codeAction))
      
         # ----- mise en base de données de l'action -----
         # récupération valeur du champ id de l'action à mémoriser
         idAction = self.__bdd.recupererValeurId('action', codeAction)
         if self.__bdd.get_codeResult() != 0:
            raise ValueError  # lève exception si échec requête  
         if idAction != -1:
            # la valeur de idAction est valide
            sqlQuery = "INSERT INTO journal (date_heure, id_action) VALUES ('{}', {})" \
               .format(dateHeure, idAction)
            self._codeResult = self.__bdd.executerReqInsUpdDel(sqlQuery)
         else:
            raise ValueError  # erreur lors récupération id
         message = "  * Succès mise en base de codeAction '{}'".format(codeAction)
         print(message)
         self.logger.debug("{} -- {}".format(message, fonction))
      except ValueError as erreur:
         # ----- gestion des éventuelles erreurs survenues -----
         if self._codeResult == 100:
            message = "code {}, échec mise en bdd, codeAction '{}' non valide ! -- {}" \
               .format(self._codeResult, codeAction, fonction)
            self.logger.error(message)
         else:
            self._codeResult = 102
            message = "code {}, échec mise en bdd codeAction '{}' -- {}" \
               .format(self._codeResult, codeAction, fonction)
            self.logger.error(message)
      except:
         self._codeResult = 103
         message = "code {}, échec mise en bdd codeAction '{}'\n{} -- {}" \
            .format(self._codeResult, codeAction, sys.exc_info(), fonction)
         self.logger.error(message)
      return self._codeResult
      
   def afficherActionMemBddBrut(self, debug=False):
      """ Affiche les actions mémorisées dans la table journal de la bdd, résultats bruts
      """
      fonction ="CGestionSavThread.CGestionSav:afficherActionMemBddBrut()"
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
            message = "0 action mémorisée dans la bdd"
            print(message)
            self.logger.debug("{} -- {}".format(message, fonction))
      except:
         message = "{}\n-- {}".format(sys.exc_info(), fonction)
         self.logger.error(message)

   def afficherActionMemBdd(self, debug=False):
      """ Affiche les actions mémorisées dans la table journal de la bdd
      """
      fonction ="CGestionSavThread.CGestionSav:afficherActionMemBdd()"
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
            message = "0 action mémorisée dans la bdd"
            print(message)
            self.logger.debug("{} -- {}".format(message, fonction))
      except:
         message = "{}\n-- {}".format(sys.exc_info(), fonction)
         self.logger.error(message)
            
   def effacerActionMemBdd(self):
      """ Efface toutes les actions enregistrées dans la bdd. 
          Autrement dit efface toutes les données de la table journal
      """
      fonction ="CGestionSavThread.CGestionSav:effacerActionMemBdd()"
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
         message = "{}\n-- {}".format(sys.exc_info(), fonction)
         self.logger.error(message)
      
class CThreadMemBdd(threading.Thread, CGestionSav):
   """ Thread permettant de mettre en base un enregistrement.
       En cas d'échec, le thread essaiera le nombre de fois défini cette opération avec une durée
       d'attente définie entre chaque essai.
   """
   
   def __init__(self, bdd, logger, isHeritage=True, codeAction='0', nbEssaiBdd=5, \
                dureeEntreEssaiBdd=5, dateHeure='2000-01-01 00:00:00'):
      """ constructeur
          bdd : référence à un objet "connexion bdd"
          logger : référence à un objet "logger console et fichier rotatif"
          isHeritage : boolean, différencie un objet créé par la classe mère de la classe fille, 
                       utile pour le debug (affichage création objet)
                       False : objet classe mère          True : objet classe fille (héritage)
          codeAction : str[1], lettre correspondant à l'action à mémoriser dans la bdd
          nbEssaiBdd : int, nombre d'essais de mise en bdd en cas d'échec
          dureeEntreEssaiBdd : int, durée (en s) entre chaque essai de mise en bdd en cas d'échec
          dateHeure : datetime, date et heure de la demande d'enregistrement du codeAction
      """
      # exécution constructeur classe mère
      CGestionSav.__init__(self, bdd, logger, isHeritage, nbEssaiBdd, dureeEntreEssaiBdd)
      fonction = "CGestionSavThread.CThreadMemBdd:self.__init__()"
      self.__codeAction = codeAction
      self.__dateHeure = dateHeure
      # préparation du thread
      threading.Thread.__init__(self)
      message = "Création d'un objet 'CThreadMemBdd' avec lien à bdd et logger -- {}" \
         .format(fonction)
      self.logger.debug(message)
      
   def run(self):
      """ Méthode exécutée lors du lancement du thread. Gère la mise en bbd du codeAction.
          En cas d'échec, le thread essaiera le nombre de fois défini cette opération avec une durée
          d'attente définie entre chaque essai.
          Un verrou est mis en place pour être sûr que la connexion à la bdd ne soit utlisée que par
          un seul thread à la fois.
      """
      fonction = "CGestionSavThread.CThreadMemBdd:run()"
      nomThread = self.getName()	    # Chaque thread possède un nom
      time.sleep(0.1)
      nbEssaiBdd = 1
      while nbEssaiBdd <= self._nbEssaiBdd:
         with verrou:
            # empêche un autre client (thread) d'utiliser la connexion à la bdd en même temps
            print("{} {}".format(nomThread, datetime.now()))
            message = "{}. Essai {}/{} : demande mise en bdd action '{}' -- {}" \
               .format(nomThread, nbEssaiBdd, self._nbEssaiBdd, self.__codeAction, fonction)
            self.logger.debug(message)
            self.mettreEnBddAction(self.__codeAction, self.__dateHeure)

         if self._codeResult == 0:
            # succès opération
            message = "{}. Succès mise en bdd action '{}' -- {}" \
               .format(nomThread, self.__codeAction, fonction)
            self.logger.debug(message)
            break
         else:
            # échec opération, nouvelle tentative dans x secondes
            message = "{}. Echec mise en bdd action '{}'" \
               .format(nomThread, self.__codeAction)
            nbEssaiBdd += 1
            if nbEssaiBdd <= self._nbEssaiBdd:
               # prochaine tentative dans x secondes
               message2 = "{}. Reste {} essai(s). Prochaine tentative dans {} secondes -- {}" \
                  .format(message, self._nbEssaiBdd-nbEssaiBdd+1, self._dureeEntreEssaiBdd, \
                          fonction)
               self.logger.error(message2)
               time.sleep(self._dureeEntreEssaiBdd)
            else:
               # c'était le dernier essai
               message2 = "{}. Fin des essais. -- {}".format(message, fonction)
               self.logger.error(message2)
               
      message = "{}. Fin thread. -- {}".format(nomThread, fonction)
      self.logger.debug(message)            
       
     
if __name__ == "__main__":
   # Nb d'essais effectués pour mettre en base de données si échec
   NB_ESSAI_BDD = 5
   # Durée d'attente en secondes entre 2 essais de mise en bdd
   DUREE_ENTRE_ESSAI_BDD = 3
   
   fonction = "CGestionSavThread, main"
   CLogger.effacerFichierLog("debugSav.log")
   # ----- Mise en place du logger qui va gérer les handlers console et fichier rotatif
   logger = CLogger(loggerName="debugSav", loggerLevel="DEBUG", \
                    consoleLevel="INFO", fileName="debugSav.log", fileLevel="DEBUG")      
   # ---- Création d'un objet 'connexion bdd', cela teste aussi l'accès à la bdd -------
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
      sav = CGestionSav(bdd, logger, False, NB_ESSAI_BDD, DUREE_ENTRE_ESSAI_BDD)
      sav.effacerActionMemBdd()
      codeAction = 'R'
      for seq in range(10):
         message = "PROG PRINCIPAL. Demande mise en bdd action '{}' -- {}" \
            .format(codeAction, fonction)
         sav.logger.debug(message)
         sav.mettreEnBddActionThread(codeAction)
         time.sleep(1)
      time.sleep(3)
      sav.afficherActionMemBdd()
      print("\nFin programme CGestionSav.py")
   
