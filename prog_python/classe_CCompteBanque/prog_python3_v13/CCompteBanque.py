#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : CCompteBanque.py       version 1.3
Date : 11-03-2018
Auteur : Hervé Dugast

------- affichage console ------------------------------------------------------
La classe CCompteBanque est une classe abstraite (non instanciable),
l'implémentation doit se faire dans les classes filles
Nombre total de comptes bancaires : 0

Exécution de :   dir(CCompteBanque)
['_CCompteBanque__genererNouveauNumeroCompte', '_CCompteBanque__get_solde', 
'_CCompteBanque__nbComptes', '_CCompteBanque__set_solde', '_CCompteBanque__typeCompteBanque', 
'__abstractmethods__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', 
'__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__le__', '__lt__',
'__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
'__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_abc_cache', '_abc_negative_cache',
'_abc_negative_cache_version', '_abc_registry', 'afficherInformations', 
'afficherNombreComptesExistant', 'afficherSolde', 'afficherTypesComptesBanqueDispo', 
'deposerArgent', 'get_numero', 'get_solde', 'get_typeCompteBanque', 'get_typeCompteBanqueKeys',
'set_solde', 'soldePublic']

Types de compte bancaire disponibles :
   Clé      Nom module/classe 	Préfixe compte
   -------------------------------------------
   CHEQ     CCompteCheque	100-
   EPAR     CCompteEpargne	200-
--------------------------------------------------------------------------------
"""
from abc import ABC, abstractmethod

class CCompteBanque(ABC):
   """ Classe mère abstraite, gère les opérations courantes de différents types de comptes bancaires
   """
   
   # attributs statiques 
   # mémorise le type de compte avec ses 2 informations : nom classe/module et préfixe compte
   # ex. : type compte "CHEQ" -> module CCompteCheque.py / classe CCompteCheque, prefixe : '100-'
   __typeCompteBanque = {"CHEQ":["CCompteCheque", "100-"], "EPAR":["CCompteEpargne", "200-"]}
   # mémorise nombre de comptes bancaires créés et permet de générer numéros de compte unique
   __nbComptes = 0  
   
   def __init__(self, soldePublic=-1, soldeMin=-1, typeCompte="0"):
      """ Constructeur
          soldePublic : attribut public permet d'accéder ou modifier l'attribut privé __solde
          soldeMin : solde en dessous lequel un retrait est impossible
          typeCompte : type de compte bancaire (chèque, épargne...)
          -1, "0" -> valeur par défaut, signifie que la valeur de l'attribut n'a pas été renseignée
                       la valeur de l'objet sera renseignée à l'aide d'une saisie clavier
      """
      # génère un numéro de compte bancaire unique en fonction du type demandé
      self._numero = "0"    # pour indiquer le type à pyreverse
      self._numero = CCompteBanque.__genererNouveauNumeroCompte(typeCompte)
      if soldePublic == -1:
         # valeur non passée en paramètre, donc saisie clavier de cette valeur
         soldePublic = float(input("solde du compte ? "))
      else:
         # valeur du solde passée en paramètre
         print("solde compte = {:.02f}".format(soldePublic))
      # mémorise la valeur du solde dans l'attribut privé __solde
      self.set_solde(soldePublic, soldeMin)
      super().__init__() # appel constructeur classe mère abc.py
      
   def __str__(self):
      """ Affichage par défaut de l'objet
      """
      return "Compte n°{} : solde compte = {}".format(self._numero, self.__solde)
   
   @staticmethod
   def __genererNouveauNumeroCompte(typeCompte):
      """ Génère un nouveau préfixe de compte en fonction du type de compte demandé.
          Pour info, pyreverse ne détecte pas les attributs statiques s'ils sont modifiés DANS le
          constructeur. En clair, ne pas mettre CCompteBanque.__nbComptes += 1 dans le constructeur!
          Retour : nouveau numéro de compte bancaire (int)
      """
      CCompteBanque.__nbComptes += 1
      numero = CCompteBanque.__typeCompteBanque[typeCompte][1] + str(CCompteBanque.__nbComptes)
      return numero
      
   def deposerArgent(self, somme=-1):
      """ Dépose une somme d'argent (nombre positif) sur le compte indiqué
      """
      if somme == -1:
         # demande saisie clavier
         somme = float(input("Somme à déposer sur le compte (nombre positif) ? "))
      print("*** Dépot de {:.02f} € sur le compte suivant :".format(somme))
      # modifie la valeur du solde en fonction de la somme déposée
      self.set_solde(self.get_solde()+somme)
      self.afficherInformations()

   def __get_solde(self):
      """ Méthode appelée quand on souhaite récupérer la valeur de l'attribut privé __solde 
          retourne la valeur de l'attribut privé __solde 
          """
      return self.__solde
   
   def __set_solde(self, soldePublic, soldeMin=0):
      """ Méthode appelée quand on souhaite modifier la valeur de l'attribut privé __solde 
          Modifie le solde d'un compte en tenant compte du type de compte :
          - compte de type 'CHEQ' -> le solde ne peut pas être initialisé à une valeur inférieure au
            découvert autorisé.
          - compte de type 'EPAR' -> le solde ne peut pas être initialisé à une valeur inférieure au
            solde minimal.
      """
      while soldePublic < soldeMin:
         print("Erreur ! Le solde ({:.02f} €) doit être supérieur ou égal à {:.02f} € ! " \
               .format(soldePublic, soldeMin))
         soldePublic = float(input("Saisir un solde valide ? "))
      self.__solde = soldePublic
   
   # Signale à python que les accès en lecture et écriture de l'attribut public soldePublic seront
   # redirigées vers respectivement les méthodes __get_solde et __set_solde, grâce à une propriété 
   # Ce mécanisme permet de "protéger" un peu les accès à un attribut privé (__solde)
   soldePublic = property(__get_solde, __set_solde)

   def get_solde(self):
      return self.__solde

   def set_solde(self, soldePublic, soldeMin=0):
      """ Méthode public permettant de modifier l'attribut privé __solde
          Redirige vers la méthode __set_solde
      """
      self.__set_solde(soldePublic, soldeMin)
      
   def get_numero(self):
      return self._numero
      
   def afficherSolde(self):
      """ affiche le solde du compte bancaire 
      """
      print("solde compte = {:.02f} €".format(self.__solde))

   @abstractmethod
   def afficherInformations(self):
      """ Méthode abstraite, affiche les informations du compte bancaire
          Doit être définie dans les classes filles
      """
      pass
   
   @staticmethod
   def get_typeCompteBanqueKeys():
      """ Retourne les clés correspondant aux types de comptes possibles, exemple
          typeCompteBanque = {"CHEQ":["CCompteCheque", "100-"], "EPAR":["CCompteEpargne", "200-"]}
          Retour : liste     (exemple : ["CHEQ", "EPAR"])
      """
      typeCompteBanqueKeys = []  # liste qui contiendra type compte bancaire : "EPAR", "CHEQ"...
      for key in CCompteBanque.__typeCompteBanque.keys():
         typeCompteBanqueKeys.append(key)
      return typeCompteBanqueKeys
   
   @staticmethod
   def get_typeCompteBanque():
      """ Retourne contenu variable typeCompteBanque
          typeCompteBanque = {"CHEQ":["CCompteCheque", "100-"], "EPAR":["CCompteEpargne", "200-"]}
      """
      return CCompteBanque.__typeCompteBanque

   @staticmethod
   def afficherNombreComptesExistant():
      """ méthode statique, affiche le nombre de comptes bancaires créés
      """
      print("Nombre total de comptes bancaires : {}".format(CCompteBanque.__nbComptes))

   @staticmethod
   def afficherTypesComptesBanqueDispo():
      """ méthode statique, affiche les types de comptes bancaires disponibles
          ----- Exemple affichage console -----
          Types de compte bancaire disponibles :
             Clé      Nom module/classe 	Préfixe compte
             -------------------------------------------
             CHEQ     CCompteCheque	100-
             EPAR     CCompteEpargne	200-
      """
      print("\nTypes de compte bancaire disponibles :")
      print("   Clé      Nom module/classe \tPréfixe compte")
      print("  ", "-"*43)
      for cle, listeAttributCompte in CCompteBanque.__typeCompteBanque.items():
         print("   {}     {}\t{}".format(cle, listeAttributCompte[0], listeAttributCompte[1]))

if __name__ == "__main__":
   print("La classe CCompteBanque est une classe abstraite (non instanciable),")
   print("l'implémentation doit se faire dans les classes filles")
   CCompteBanque.afficherNombreComptesExistant()
   
   print("\nExécution de :   dir(CCompteBanque)")
   print(dir(CCompteBanque))
   
   CCompteBanque.afficherTypesComptesBanqueDispo()