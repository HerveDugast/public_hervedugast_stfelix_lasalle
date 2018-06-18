#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : CGestionBanque.py (partiel)     version 1.3
   ***** PARTIE créer nouveau client uniquement *****
Date : 11-03-2018
Auteur : Hervé Dugast

------- affichage console ------------------------------------------------------
*** Création nouveau client
Nom client ? philou
Prénom client ? marc
Année de naissance client (saisir 0 si inconnue) ? 3000
  Veuillez saisir une année de naissance valide
Année de naissance client (saisir 0 si inconnue) ? 100
  Veuillez saisir une année de naissance valide
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

if __name__ == "__main__":
   banque = CGestionBanque()
   # Création de nouveaux clients
   banque.creerNouveauClient()  ; print("")  # "philou", "marc", 0, "lorient"
   banque.creerNouveauClient("Barrot", "Lise", 1995, "Nantes") ; print("")
   banque.creerNouveauClient("LELOUP", "Phil", 2000, "Nantes") ; print("")
   banque.creerNouveauClient("BIBA", "Lise", 1990, "Brest")
   print("Fin programme")