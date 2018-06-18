#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : CGestionBanque.py       version 1.4
Date : 13-04-2018
Auteur : Hervé Dugast

------- affichage console ------------------------------------------------------
*** Clients habitant à Nantes :
Aucun client enregistré actuellement !

*** Création nouveau client
Nom client ? philou
Prénom client ? marc
Année de naissance client (saisir 0 si inconnue) ? 1993
Ville client ? lorient
   * Récapitulatif *
Client n°1 : PHILOU Marc, né 1993, ville LORIENT
Succès opération

*** Création nouveau client
   * Récapitulatif *
Client n°2 : BARROT Lise, né 1995, ville NANTES
Succès opération

*** Création nouveau client
   * Récapitulatif *
Client n°3 : LELOUP Phil, né 2000, ville NANTES
Succès opération

*** Création nouveau client
   * Récapitulatif *
Client n°4 : BIBA Lise, né 1990, ville BREST
Succès opération

*** Clients habitant à Nantes :
Client n°2 : BARROT Lise, né 1995, ville NANTES
Client n°3 : LELOUP Phil, né 2000, ville NANTES

*** Clients se prénommant Lise :
Client n°2 : BARROT Lise, né 1995, ville NANTES
Client n°4 : BIBA Lise, né 1990, ville BREST

*** Création compte bancaire
... client n°2 (BARROT Lise)
... type compte : EPAR
Solde minimal = 10.00
solde compte = 200.00
   * Récapitulatif *
   - Compte EPAR n° 200-1
     solde compte = 200.00, solde minimal = 10.00, intérêts = 0.00
Succès opération

*** Création compte bancaire
Numéro client ? 1
... client n°1 (PHILOU Marc)
Choisir type compte bancaire parmi ['CHEQ', 'EPAR'] ? CHEQ
... type compte : CHEQ
Découvert autorisé ? 100
solde du compte ? 200
   * Récapitulatif *
   - Compte CHEQ n° 100-2
     solde compte = 200.00, découvert autorisé = 100.00
Succès opération

*** Création compte bancaire
... client n°3 (LELOUP Phil)
! Erreur n°21 classe CClient : client n°3
! ECHEC creerCompteBancaire(), type compte inexistant (CHEK) !

*** Création compte bancaire
! Erreur n°11 classe CGestionBanque :
! ECHEC creerCompteBancaire(), client n°5 inexistant !

*** Création compte bancaire
... client n°2 (BARROT Lise)
... type compte : CHEQ
découvert autorisé = 500.00
solde compte = -78.90
   * Récapitulatif *
   - Compte CHEQ n° 100-3
     solde compte = -78.90, découvert autorisé = 500.00
Succès opération

*** Création compte bancaire
... client n°2 (BARROT Lise)
... type compte : EPAR
Solde minimal = 10.00
solde compte = 10.25
   * Récapitulatif *
   - Compte EPAR n° 200-4
     solde compte = 10.25, solde minimal = 10.00, intérêts = 0.00
Succès opération

*** Affichage informations clients
Client n°2 : BARROT Lise, né 1995, ville NANTES
   - Compte CHEQ n° 100-3
     solde compte = -78.90, découvert autorisé = 500.00
   - Compte EPAR n° 200-1
     solde compte = 200.00, solde minimal = 10.00, intérêts = 0.00
   - Compte EPAR n° 200-4
     solde compte = 10.25, solde minimal = 10.00, intérêts = 0.00

Client n°1 : PHILOU Marc, né 1993, ville LORIENT
   - Compte CHEQ n° 100-2
     solde compte = 200.00, découvert autorisé = 100.00
Client n°2 : BARROT Lise, né 1995, ville NANTES
   - Compte CHEQ n° 100-3
     solde compte = -78.90, découvert autorisé = 500.00
   - Compte EPAR n° 200-1
     solde compte = 200.00, solde minimal = 10.00, intérêts = 0.00
   - Compte EPAR n° 200-4
     solde compte = 10.25, solde minimal = 10.00, intérêts = 0.00
Client n°3 : LELOUP Phil, né 2000, ville NANTES
Client n°4 : BIBA Lise, né 1990, ville BREST

*** Dépôts argent
Numéro client ? 1
Choisir un compte parmi :
   - compte CHEQ n°100-2 : solde = 200.0
Numéro de compte pour le dépôt ? 100-2
Somme à déposer sur le compte (nombre positif) ? 120.75
*** Dépot de 120.75 € sur le compte suivant :
   - Compte CHEQ n° 100-2
     solde compte = 320.75, découvert autorisé = 100.00
Succès opération

! Erreur n°12 classe CGestionBanque :
! ECHEC deposerArgent(), client n°25 inexistant !

! Erreur n°22 classe CClient : client n°2
! ECHEC deposerArgent(), n° compte inexistant (200-11) !

*** Dépot de 100.00 € sur le compte suivant :
   - Compte EPAR n° 200-1
     solde compte = 300.00, solde minimal = 10.00, intérêts = 0.00
Succès opération
Fin programme
--------------------------------------------------------------------------------
"""
from CClient import CClient
from CCompteBanque import CCompteBanque

class CGestionBanque:
   """ gère les comptes bancaires de client
   """
   def __init__(self):
      """ constructeur """
      self.__clients = {}
      
   def creerNouveauClient(self, nom="0", prenom="0", anNaiss=-1, ville="0"):
      """ Crée un nouveau client puis affiche les informations créées
          -1, "0" -> valeur par défaut, signifie que la valeur de l'attribut n'a pas été renseignée
                     la valeur de l'objet sera renseignée à l'aide d'une saisie clavier
          Retour : code résultat opération (int)     0 : succès     1 ou plus : échec
      """
      print("*** Création nouveau client")
      client = CClient(nom, prenom, anNaiss, ville)
      # mémorisation du client dans un dictionnaire {numClient : objetClient}
      self.__clients[client.get_numero()] = client
      # affiche le succès de l'opération
      self.__afficherResultatOperation(0)

   def chercherClients(self, numClient=-1, nom="0", prenom="0", anNaiss=-1, ville="0"):
      """ Cherche et retourne les numéros des clients qui répondent aux critères transmis 
          Rappel, les clients sont stockés dans un dictionn. : clients{numeroClient : objetClient}
          -1, "0" -> valeur par défaut, critère non pris en compte dans la recherche
          Retour : liste contenant numéros des clients répondant aux critères
                   liste vide -> aucun client ne correspond aux critères
      """
      numClientsTrouves = []  # contiendra numéros des clients répondant aux critères
      # parcourt tous les clients existants
      for client in self.__clients.values():
         if numClient == -1 or client.get_numero() == numClient:
            # pas de recherche sur le n° client ou n° client existe
            if nom == "0" or client.get_nom() == nom.upper():
               if prenom == "0" or client.get_prenom() == prenom.capitalize():
                  if anNaiss == -1 or client.get_anNaiss() == anNaiss:
                     if ville == "0" or client.get_ville() == ville.upper():
                        # client répondant aux critères demandés a été trouvé
                        numClientsTrouves.append(client.get_numero())
      return numClientsTrouves
   
   def afficherInfosClientsCriteres(self, numClient=-1, nom="0", prenom="0", anNaiss=-1, ville="0"):
      """ Cherche et affiche les informations des clients qui répondent aux critères transmis 
          Rappel, les clients sont stockés dans un dictionn. : clients{numeroClient : objetClient}
          -1, "0" -> valeur par défaut, critère non pris en compte dans la recherche
      """
      listeClientsTrouves = self.chercherClients(numClient, nom, prenom, anNaiss, ville)
      if listeClientsTrouves:
         # affiche les clients répondant aux critères
         self.afficherInfosClients(listeClientsTrouves)
      else:
         # aucun client répondant aux critères n'a été trouvé
         print("Aucun client ne correspond aux critères de recherche !")

   def afficherInfosClients(self, listeNumClient=[]):
      """ Affiche les informations des clients indiqués dans la liste 
      """
      # pour info, self.__clients retourne False si aucun client (dictionnaire vide)
      if not self.__clients:
         # aucun client existe
         print("Aucun client enregistré actuellement !")
      else:
         # au moins 1 client existe
         if listeNumClient:
            # affichage des informations de certains clients
            clientTrouve = False # True -> client demandé existe
            for numClientAff in listeNumClient:
               # parcourt les numéros de clients demandés pour affichage informations
               for numClient in self.__clients.keys():
                  # parcourt tous les clients existants
                  if numClient == numClientAff:
                     # client demandé a été trouvé, affichage de ses informations
                     self.__clients[numClient].afficherInformations()
                     clientTrouve = True
            if not clientTrouve:
               print("Client(s) demandé(s) non trouvé(s)\n"           )
         else:
            # affichage des informations de tous les clients, pas de liste recue en paramètre
            for numClient in self.__clients.keys():   # parcours de tous les clients existants
               self.__clients[numClient].afficherInformations()
         
   def creerCompteBancaire(self, numClient=-1, typeCompteBanque="0", solde=-1, soldeMin=-1):
      """ Crée un compte bancaire pour un client. 
          Affiche les informations du compte créé, ou un message d'erreur en cas d'échec lors de la 
          création
          Retour : code résultat opération (int)     0 : succès     1 ou plus : échec
      """
      print("*** Création compte bancaire")
      # renseigne numéro client
      numClient = self.__renseignerNumeroClient(numClient)
      # vérifie l'existence du client à qui l'on souhaite créer un compte bancaire
      if self.verifierExistenceNumClient(numClient):  
         # le client existe, demande de création d'un compte bancaire
         codeResult = \
            self.__clients[numClient].creerCompteBancaire(typeCompteBanque, solde, soldeMin)
         if codeResult == 0:
            # affiche succès opération
            self.__afficherResultatOperation(codeResult)
      else:
         # client n'existe pas, création compte bancaire impossible
         codeResult = 11 
         # affiche message indiquant le problème rencontré
         self.__afficherResultatOperation(codeResult, numClient)
      return codeResult 
   
   def __renseignerNumeroClient(self, numClient):
      """ Retourne un numéro de client à partir d'une saisie utilisateur ou de la valeur passée
          en paramètre
          Retour : numéro du client (int)
      """
      if numClient == -1: 
         numClient = int(input("Numéro client ? "))
      return numClient
         
   def verifierExistenceNumClient(self, numClient):
      """ vérifie si numéro de client passé par paramètre existe, donc vérifie si le client existe
          Retour : booléen    True -> client existe       False -> client n'existe pas
      """
      if numClient in self.__clients:    
         return True    # Le client existe
      else:   
         return False   # numéro de client est introuvable

   def deposerArgent(self, somme=-1, numClient=-1, numCompte="0"):
      """ Dépose une somme d'argent sur le compte du client indiqué
          -1, "0" -> valeur par défaut, signifie que la valeur de l'attribut n'a pas été renseignée
                     la valeur de l'objet sera renseignée à l'aide d'une saisie clavier
          Retour : code résultat opération (int)     0 : succès     1 ou plus : échec
      """
      # renseigne numéro client
      numClient = self.__renseignerNumeroClient(numClient)
      # vérifie l'existence du client qui souhaite déposer de l'argent
      if self.verifierExistenceNumClient(numClient):  
         # le client existe, demande de dépôt d'argent sur un compte bancaire
         codeResult = self.__clients[numClient].deposerArgent(somme, numCompte)
         if codeResult == 0:
            # succès opération
            self.__afficherResultatOperation(codeResult)
      else:
         # client n'existe pas, opération bancaire impossible
         codeResult = 12
         self.__afficherResultatOperation(codeResult, numClient)
      
   def retirerArgent(self, somme=-1, numClient=-1, numCompte="0"):
      """ Retire une somme d'argent sur le compte du client indiqué
          -1, "0" -> valeur par défaut, signifie que la valeur de l'attribut n'a pas été renseignée
                     la valeur de l'objet sera renseignée à l'aide d'une saisie clavier
          Retour : code résultat opération (int)     0 : succès     1 ou plus : échec
      """
      # renseigne numéro client
      numClient = self.__renseignerNumeroClient(numClient)
      # vérifie l'existence du client qui souhaite retirer de l'argent
      if self.verifierExistenceNumClient(numClient):  
         # le client existe, demande de retrait d'argent sur un compte bancaire
         codeResult = self.__clients[numClient].retirerArgent(somme, numCompte)
         if codeResult == 0:
            # succès opération
            self.__afficherResultatOperation(codeResult)
      else:
         # client n'existe pas, opération bancaire impossible
         codeResult = 13
      self.__afficherResultatOperation(codeResult, numClient)

   def __afficherResultatOperation(self, codeResult, *args):
      """ Affiche un message en fonction du résultat de l'opération demandé
          Le message affiché est de type "succès" ou "échec". Dans ce dernier cas, on affiche
          le code d'erreur avec une courte description du problème rencontré
          *args : liste contenant les éventuels arguments (n° client...) envoyés à la fonction
      """
      if codeResult == 0:   
         # Opération demandée a réussi
         print("Succès opération")
      else:
         print("! Erreur n°{} classe CGestionBanque :".format(codeResult))

      # ----- erreur 1x ----- : erreurs liés au module CGestionBanque
      # erreur 11 : args[0] -> numClient
      if codeResult == 11:
         print("! ECHEC creerCompteBancaire(), client n°{} inexistant !".format(args[0]))

      # erreur 12 : args[0] -> numClient
      elif codeResult == 12:
         print("! ECHEC deposerArgent(), client n°{} inexistant !".format(args[0]))
   
      # erreur 13 : args[0] -> numClient
      elif codeResult == 12:
         print("! ECHEC retirerArgent(), client n°{} inexistant !".format(args[0]))

if __name__ == "__main__":
   banque = CGestionBanque()
   
   # Recherche des clients habitant à Nantes
   listeNumClient = banque.chercherClients(ville="Nantes")
   print("*** Clients habitant à Nantes :")
   banque.afficherInfosClients(listeNumClient) ; print("")
   
   # Création de nouveaux clients
   #banque.creerNouveauClient()  ; print("")  # "philou", "marc", 0, "lorient"
   banque.creerNouveauClient("Barrot", "Lise", 1995, "Nantes") ; print("")
   banque.creerNouveauClient("LELOUP", "Phil", 2000, "Nantes") ; print("")
   banque.creerNouveauClient("BIBA", "Lise", 1990, "Brest")
   
   # Recherche des clients habitant à Nantes
   print("\n*** Clients habitant à Nantes :")
   banque.afficherInfosClientsCriteres(ville="Nantes")
   
   # Recherche des clients habitant à Nantes
   print("\n*** Clients se prénommant Lise :")
   banque.afficherInfosClientsCriteres(prenom="lise") ; print("")

   # Création d'un compte bancaire
   banque.creerCompteBancaire(2, "EPAR", 200, 10) ; print("")
   #banque.creerCompteBancaire() ; print("")
   #banque.creerCompteBancaire(3, "CHEK") ; print("")
   banque.creerCompteBancaire(5, "CHEQ", 123.45, 0) ; print("")
   banque.creerCompteBancaire(2, "CHEQ", -78.9, -500) ; print("")
   banque.creerCompteBancaire(2, "EPAR", 10.25, 10)

   # affichage informations clients
   print("\n*** Affichage informations clients")
   banque.afficherInfosClients([2])
   print("")
   banque.afficherInfosClients()
   
   # Déposer de l'argent
   print("\n*** Dépôts argent")
   #banque.deposerArgent() ; print("")
   banque.deposerArgent(100, 25, "100-1") ; print("")
   banque.deposerArgent(100, 2, "200-11") ; print("")
   banque.deposerArgent(100, 2, "200-1")
   
   # Retirer de l'argent
   print("\n*** Retrait argent")
   banque.retirerArgent(100, 2, "100-1") ; print("")
   banque.retirerArgent(1000, 2, "100-1") ; print("")

   print("Fin programme")