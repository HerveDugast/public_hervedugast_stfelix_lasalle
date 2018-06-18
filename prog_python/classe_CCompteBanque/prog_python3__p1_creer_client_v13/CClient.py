#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : CClient.py (partiel)      version 1.3
   ***** PARTIE créer nouveau client uniquement *****
Date : 11-03-2018
Auteur : Hervé Dugast
"""

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