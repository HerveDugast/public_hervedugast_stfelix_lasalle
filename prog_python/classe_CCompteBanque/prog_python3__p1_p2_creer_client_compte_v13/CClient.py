#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : CClient.py (partiel)      version 1.3
   ***** PARTIES créer nouveau client et nouveau compte bancaire uniquement *****
Date : 11-03-2018
Auteur : Hervé Dugast
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
         # Echec, args[0] -> numClient
         print("! Erreur n°{} classe CClient : client n°{}".format(codeResult, args[0]))

      # ----- erreur 2x ----- : erreurs liés au module CClient
      # erreur 21 : args[1] -> typeCompte
      if codeResult == 21:
         print("! ECHEC creerCompteBancaire(), type compte inexistant ({}) !".format(args[1]))
   