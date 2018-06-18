#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : CGestionBanque.py (partiel)     version 1.3
   ***** PARTIES créer nouveau client et nouveau compte bancaire uniquement *****
Date : 11-03-2018
Auteur : Hervé Dugast

------- affichage console ------------------------------------------------------
*** Création nouveau client
Nom client ? philou
Prénom client ? marc
Année de naissance client (saisir 0 si inconnue) ? 0
Ville client ? lorient
   * Récapitulatif *
Client n°1 : PHILOU Marc, né 0, ville LORIENT
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

if __name__ == "__main__":
   banque = CGestionBanque()
   # Création de nouveaux clients
   banque.creerNouveauClient()  ; print("")  # "philou", "marc", 0, "lorient"
   banque.creerNouveauClient("Barrot", "Lise", 1995, "Nantes") ; print("")
   banque.creerNouveauClient("LELOUP", "Phil", 2000, "Nantes") ; print("")
   banque.creerNouveauClient("BIBA", "Lise", 1990, "Brest")
   
   # Création d'un compte bancaire
   banque.creerCompteBancaire(2, "EPAR", 200, 10) ; print("")
   banque.creerCompteBancaire() ; print("") # n°1, 'CHEQ', 100, 200
   banque.creerCompteBancaire(3, "CHEK") ; print("")
   banque.creerCompteBancaire(5, "CHEQ", 123.45, 0) ; print("")
   banque.creerCompteBancaire(2, "CHEQ", -78.9, 500) ; print("")
   banque.creerCompteBancaire(2, "EPAR", 10.25, 10)
   
   print("Fin programme")