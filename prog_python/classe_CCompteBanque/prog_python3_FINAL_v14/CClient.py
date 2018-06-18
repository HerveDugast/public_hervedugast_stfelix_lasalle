#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : CClient.py       version 1.4
Date : 13-04-2018
Auteur : Hervé Dugast

------- affichage console ----------------
*** Création clients
Nom client ? philou
Prénom client ? marc
Année de naissance client (saisir 0 si inconnue) ? 0
Ville client ? lorient
   * Récapitulatif *
Client n°1 : PHILOU Marc, né 0, ville LORIENT

   * Récapitulatif *
Client n°2 : BARROT Lise, né 1995, ville NANTES

*** Affichage informations clients
Client n°1 : PHILOU, Marc, 0, LORIENT, {}

Client n°1 : PHILOU Marc, né 0, ville LORIENT
Client n°2 : BARROT Lise, né 1995, ville NANTES

*** Création compte bancaire
... client n°2 (BARROT Lise)
Choisir type compte bancaire parmi ['CHEQ', 'EPAR'] ? EPA
! Erreur n°21 classe CClient : client n°2
! ECHEC creerCompteBancaire(), type compte inexistant (EPA) !

... client n°2 (BARROT Lise)
Choisir type compte bancaire parmi ['CHEQ', 'EPAR'] ? EPAR
... type compte : EPAR
Saisir le solde minimal (supérieur ou égal à 0) ? 10
solde du compte ? 0
Erreur ! Le solde (0.0 €) doit être supérieur ou égal à 10.0 € ! 
Saisir un solde autorisé ? 220.50
   * Récapitulatif *
   - Compte EPAR n° 200-1
     solde compte = 220.5, solde minimal = 10.0, intérêts = 0

... client n°2 (BARROT Lise)
... type compte : CHEQ
découvert autorisé = 200
solde compte = 100
   * Récapitulatif *
   - Compte CHEQ n° 100-2
     solde compte = 100, découvert autorisé = 200

... client n°2 (BARROT Lise)
... type compte : EPAR
Solde minimal = 10
solde compte = 125.75
   * Récapitulatif *
   - Compte EPAR n° 200-3
     solde compte = 125.75, solde minimal = 10, intérêts = 0

*** Informations client
Client n°1 : PHILOU Marc, né 0, ville LORIENT
Client n°2 : BARROT Lise, né 1995, ville NANTES
   - Compte CHEQ n° 100-2
     solde compte = 100, découvert autorisé = 200
   - Compte EPAR n° 200-1
     solde compte = 220.5, solde minimal = 10.0, intérêts = 0
   - Compte EPAR n° 200-3
     solde compte = 125.75, solde minimal = 10, intérêts = 0

Fin programme
------------------------------------------
"""
from CCompteBanque import CCompteBanque
from CCompteCheque import CCompteCheque
from CCompteEpargne import CCompteEpargne
# permet d'appeler un constructeur à l'aide de variables
import importlib

class CClient:
   """ gère les clients de la banque
   """
   # attributs statiques
   # mémorise nombre de clients créés et permet de générer numéros de client unique
   __nbClients = 0
   
   def __init__(self, nom="0", prenom="0", anNaiss=-1, ville="0"):
      """ constructeur
          -1, "0" -> valeur par défaut, signifie que la valeur de l'attribut n'a pas été renseignée
                     la valeur de l'objet sera renseignée à l'aide d'une saisie clavier
      """
      # génération d'un numéro de client unique
      self.__numero = 0    # pour détection pyreverse
      self.__numero = CClient.__genererNouveauNumeroClient()
      # construit le client à partir des paramètres ou d'une saisie clavier
      self.set_nom(nom)
      self.set_prenom(prenom)
      self.set_anNaiss(anNaiss)
      self.set_ville(ville)
      # pour mémoriser les comptes bancaires du client. Dictionnaire -> {numCompte : objetCompte }
      self.__comptesBanque = {}
      print("   * Récapitulatif *")
      self.afficherInformations()

   def __str__(self):
      """ affichage par défaut de l'objet
      """
      return "Client n°{} : {}, {}, {}, {}, {}".format(self.__numero, self.__nom, \
              self.__prenom, self.__anNaiss, self.__ville, self.__comptesBanque)

   @staticmethod
   def __genererNouveauNumeroClient():
      """ Génère un nouveau numéro de client unique. Cette méthode ne doit être appelée que par 
          le constructeur.
          Pour info, pyreverse ne détecte pas les attributs statiques s'ils sont modifiés DANS le
          constructeur. En clair, ne pas mettre CClient.__nbClients += 1 dans le constructeur !
          Retour : nouveau numéro de client (int)
      """
      CClient.__nbClients += 1
      return CClient.__nbClients
   
   def afficherInformations(self):
      """ Affiche les informations du client
      """
      print("Client n°{} : {} {}, né {}, ville {}" \
            .format(self.__numero, self.__nom, self.__prenom, self.__anNaiss, self.__ville))
      # affichage des comptes bancaires du client triés par ordre alphabétique (tri sur clé)
      # pour info : t[0] -> tri sur clé    t[1] -> tri sur valeur...
      for cle, compte in sorted(self.__comptesBanque.items(), key=lambda t: t[0]):
         compte.afficherInformations()
       
   def set_nom(self, nom="0"):
      """ Renseigne le nom du client. Mets tout le nom en majuscules
      """
      if nom == "0":
         # pas de nom passé en paramètre donc saisie clavier
         nom = input("Nom client ? ")
      self.__nom = nom.upper()
   
   def set_prenom(self, prenom="0"):
      """ Renseigne le nom du client. Mets la première lettre en majuscule du prénom en majuscule.
      """
      if prenom == "0":
         # pas de prénom passé en paramètre donc saisie clavier
         prenom = input("Prénom client ? ")
      self.__prenom = prenom.capitalize()

   def set_anNaiss(self, anNaiss=-1):
      """ Renseigne ou modifie l'année de naissance du client. 
          Vérifie la validité de l'année avant de modifier la valeur.
          Valeurs possibles : 0 (date naiss inconnue) ou comprise entre 1900 et 2100
      """
      while anNaiss == -1:
         try:
            anNaiss = int(input("Année de naissance client (saisir 0 si inconnue) ? "))
            if anNaiss != 0 and (anNaiss < 1900 or anNaiss > 2100):
               raise ValueError  # lève exception si valeur saisie est en dehors de la plage
         except ValueError:
            anNaiss = -1
            print("  Veuillez saisir une année de naissance valide")
      self.__anNaiss = anNaiss
      
   def set_ville(self, ville="0"):
      """ Renseigne la ville du client. Mets tout le nom de la ville en majuscules
      """
      
      if ville == "0":
         # pas de prénom passé en paramètre donc saisie clavier
         ville = input("Ville client ? ")
      self.__ville = ville.upper()   

   def get_numero(self):
      return self.__numero

   def get_nom(self):
      return self.__nom
   
   def get_prenom(self):
      return self.__prenom

   def get_anNaiss(self):
      return self.__anNaiss

   def get_ville(self):
      return self.__ville
   
   def creerCompteBancaire(self, typeCompteBanque="0", solde=-1, soldeMin=-1):
      """ Crée un compte bancaire parmi les types de comptes disponibles
          vérifie que le type de compte bancaire demandé existe. 
          -1, "0" -> valeur par défaut, signifie que la valeur de l'attribut n'a pas été renseignée
                     la valeur de l'objet sera renseignée à l'aide d'une saisie clavier
          Retour : code résultat opération (int)     0 : succès     1 ou plus : échec
      """
      print("... client n°{} ({} {})" \
            .format(self.get_numero(), self.__nom, self.__prenom))
      # renseigne le type de compte à créer
      typeCompteBanque = self.__renseignerTypeCompteACreer(typeCompteBanque)
      # crée un compte avec le type demandé s'il existe, pour le client concerné
      typeCompteExiste = False
      for cle, typeCompteAttribut in CCompteBanque.get_typeCompteBanque().items():
         if cle == typeCompteBanque:
            # récupération nom du module contenant la classe du constructeur à utiliser
            # exemple : myModule = CCompteCheque si module est CCompteCheque.py
            myModule = importlib.import_module(typeCompteAttribut[0])
            # récupération nom de la classe définie dans le module désigné
            # exemple : nomClasse = CCompteCheque si classe est CCompteCheque()
            MyClass = getattr(myModule, typeCompteAttribut[0])
            # 
            compte = MyClass(solde, soldeMin)
            self.__comptesBanque[compte._numero] = compte
            typeCompteExiste = True
      # Vérification du résultat de l'opération
      if typeCompteExiste: 
         codeResult = 0
      else:
         codeResult = 21
         # affiche message lorsque le type de compte n'existe pas
         self.__afficherResultatOperation(codeResult, self.get_numero(), typeCompteBanque)
      return codeResult
         
   def __renseignerTypeCompteACreer(self, typeCompteBanque="0"):
      """ Retourne le type de compte à créer à partir d'une saisie ou de la valeur passée en 
          paramètre
          Retour : type de compte à créer (str)
      """
      if typeCompteBanque == "0":
         # type de compte non renseigné, demande saisie type compte 
         # récupère la liste des types de comptes pouvant être créés (clés var __typeCompteBanque)
         # Exemple de liste : ["CHEQ", "EPAR"]
         typeComptePossible = CCompteBanque.get_typeCompteBanqueKeys()
         # tri de la liste des comptes possibles par ordre alphabétique
         typeComptePossible.sort()
         typeCompteBanque = input("Choisir type compte bancaire parmi {} ? " \
                                           .format(typeComptePossible))
      return typeCompteBanque
      
   def deposerArgent(self, somme=-1, numCompte="0"):
      """ Dépose une somme d'argent sur le compte indiqué
          -1, "0" -> valeur par défaut, signifie que la valeur de l'attribut n'a pas été renseignée
                     la valeur de l'objet sera renseignée à l'aide d'une saisie clavier
          Retour : code résultat opération (int)     0 : succès     1 ou plus : échec
      """
      # renseigne le numéro de compte à traiter
      numCompte = self.__renseignerCompteATraiter(numCompte)
      if self.__verifierExistenceNumCompte(numCompte):
         # numéro compte bancaire existe
         self.__comptesBanque[numCompte].deposerArgent(somme)
         codeResult = 0    # succès opération
      else:
         # numéro compte bancaire n'existe pas
         codeResult = 22
         # affiche message indiquant l'échec de l'opération
         self.__afficherResultatOperation(codeResult, self.get_numero(), numCompte)
      return codeResult
      
   def __renseignerCompteATraiter(self, numCompte):
      """ Retourne le numéro de compte bancaire à traiter à partir d'une saisie utilisateur ou 
          de la valeur passée en paramètre
          Retour : numéro du compte (str)     si "0" -> erreur, aucun compte existant pour ce client
      """
      if numCompte == "0":
         # aucun numéro de compte renseigné
         if self.__comptesBanque:
            # Au moins un compte bancaire existe, affiche les comptes bancaires existant
            print("Choisir un compte parmi :")
            for cle, compte in sorted(self.__comptesBanque.items(), key=lambda t: t[0]):
               print("   - compte {} n°{} : solde = {}" \
                     .format(compte.get_type(), cle, compte.get_solde()))
            numCompte = input("Numéro de compte pour le dépôt ? ")
         else:
            # aucun compte bancaire pour ce client
            numcompte = "0"
      return numCompte
   
   def __verifierExistenceNumCompte(self, numCompte):
      """ Vérifie l'existence du numéro de compte bancaire 
          Retour : booléen    True -> numéro compte existe    False -> n'existe pas
      """
      if numCompte in self.__comptesBanque.keys():
         return True
      else:
         return False
   
   def retirerArgent(self, somme=-1, numCompte="0"):
      """ Retire une somme d'argent sur le compte indiqué
          -1, "0" -> valeur par défaut, signifie que la valeur de l'attribut n'a pas été renseigné
                     la valeur de l'objet sera renseignée à l'aide d'une saisie clavier
          Retour : code résultat opération (int)     0 : succès     1 ou plus : échec
      """
      numCompte = self.__renseignerCompteATraiter(numCompte)
      if self.__verifierExistenceNumCompte(numCompte):
         # numéro compte bancaire existe
         codeResult = self.__comptesBanque[numCompte].retirerArgent(somme)
      else:
         # numéro compte bancaire n'existe pas
         codeResult = 23
      # affiche message indiquant l'échec de l'opération
      self.__afficherResultatOperation(codeResult)
      return codeResult      
      
   def __afficherResultatOperation(self, codeResult, *args):
      """ Affiche un message en fonction du résultat de l'opération demandé
          Le message affiché est de type "succès" ou "échec". Dans ce dernier cas, on affiche
          le code d'erreur avec une courte description du problème rencontré
          *args : liste contenant les éventuels arguments (n° client...) envoyés à la fonction
      """
      if codeResult == 0:   
         # Opération demandée a réussi
         print("  * Succès opération demandée par classe CClient *")
      else:
         print("  ! ECHEC opération demandée par classe CClient !".format(codeResult))

      # ----- erreur 2x ----- : erreurs liés au module CClient
      # erreur 21 : args[1] -> typeCompte
      if codeResult == 21:
         print("! ECHEC creerCompteBancaire(), type compte inexistant ({}) !".format(args[1]))

      # erreur 22 : args[1] -> numCompte
      elif codeResult == 22:
         print("! ECHEC deposerArgent(), n° compte inexistant ({}) !".format(args[1]))
    
      # erreur 23 : args[1] -> numCompte
      elif codeResult == 23:
         print("! ECHEC retirerArgent(), n° compte inexistant ({}) !".format(args[1]))

if __name__ == "__main__":
   print("*** Création clients")
#   client1 = CClient() ; print("")
   client1 = CClient("Philou", "Marc", 0, "Lorient")
   client2 = CClient("Barrot", "Lise", 1995, "Nantes")
   
   print("\n*** Affichage informations clients")
   # affichage informations objet avec méthode __str__
   print(client1) ; print("")
   # affichage informations objet avec méthode afficherInformations
   client1.afficherInformations()
   client2.afficherInformations()
   
   print("\n*** Création compte bancaire")
   #client2.creerCompteBancaire() ; print("")
   #client2.creerCompteBancaire() ; print("")
   client2.creerCompteBancaire("CHEQ", -100, -200) ; print("")
   client2.creerCompteBancaire("EPAR", 125.75, 10)
   
   print("\n*** Informations client")
   client1.afficherInformations()
   client2.afficherInformations()   
   
   print("\n*** Retrait argent compte bancaire")
   #client2.creerCompteBancaire() ; print("")
   #client2.creerCompteBancaire() ; print("")
   client2.retirerArgent(somme=11, numCompte="100-1")
   client2.retirerArgent(somme=1001, numCompte="100-1")

   client2.retirerArgent(somme=11, numCompte="200-2")
   client2.retirerArgent(somme=1001, numCompte="200-2")

   print("\nFin programme")
   
   