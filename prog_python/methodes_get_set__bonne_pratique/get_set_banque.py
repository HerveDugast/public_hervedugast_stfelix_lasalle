#!/usr/bin/python3.4
#coding: utf-

"""
Programme (classe) : get_set_banque.py       version 1.0
Date : 12-02-2018
Auteur : Hervé Dugast

Fonctionnement :
   Cette classe permet de créer un compte avec un solde positif ou nul. Elle permet aussi de 
   modifier le solde d'un compte existant, à condition qu'il soit positif ou nul.
   L'entrée d'un solde négatif met le solde à 0 avec un message d'alerte.

------- affichage console --------------------------------------------------------------------------
Création objet compte1 avec :   compte1 = Compte(110)
Exécution __set_solde() ... modifie __solde
compte1.__dict__ = {'_Compte__solde': 110}

Affichage contenu attribut privé avec :   print(compte1._Compte__solde)
Pour montrer que python permet de tout voir !
__solde = 110

Affichage attribut privé en passant par attribut public avec la commande :
   print(compte1.soldeAccesModif)
Exécution __get_solde() ... lit __solde
__solde = 110 

Affichage attribut privé en passant par méthode get_solde : print(compte1.get_solde())
C'est la bonne façon de faire pour afficher un attribut privé
__solde = 110 

On souhaite modifier le contenu de l'attribut privé __solde.
On ne peut pas modifier un attribut privé comme ceci :   compte1.__solde = -24
Cela lève une exception de type AttributeError. C'est une 1ère protection, contournable !

Modification contenu attribut privé avec :   compte1._Compte__solde = -24
Pour montrer que python permet de modifier un attribut privé ! 
          ***** NE JAMAIS FAIRE DE CETTE FACON  ! *****
L'affectation n'est pas passée par la méthode __set_solde... Très embêtant !
__solde = -24

Modification contenu attribut privé avec :   compte1.soldeAccesModif = -24
Pourquoi pas ! L'affectation appelle la méthode __set_solde qui vérifie la maj du solde
Le nouveau solde ne peut pas prendre de valeurs négatives, donc __solde est mis à 0
Exécution __set_solde() ... modifie __solde
ATTENTION ! Solde mis à 0 €, ne peut pas être initialisé à -24 €
Exécution __get_solde() ... lit __solde
__solde = 0 

Modification contenu attribut privé avec :   compte1.set_solde(-24)
C'est la méthode qu'il faut utiliser... elle appelle la méthode __set_solde...
Le nouveau solde ne peut pas prendre de valeurs négatives, donc __solde est mis à 0
Exécution __set_solde() ... modifie __solde
ATTENTION ! Solde mis à 0 €, ne peut pas être initialisé à -24 €
Exécution __get_solde() ... lit __solde
__solde = 0 
----------------------------------------------------------------------------------------------------

Commentaires :
En Python, il n'y a pas vraiment d'attribut privé, TOUT EST ACCESSIBLE, d'une façon ou d'une autre.
On peut toujours accéder ou modifier n'importe quel attribut d'une classe depuis l'extérieur.
Pour faire respecter l'encapsulation, on utilise des conventions :
   - attribut privé : on préfixe l'attribut de 2 underscores (exemple : __solde)
     objet.__solde = 100 lève une exception AttributeError lors d'un appel ,
                         mais il existe d'autres moyens pour contourner cette exception
   - attribut privé : on préfixe l'attribut de 1 underscore (exemple : _solde)
     objet._solde = 100  fonctionne même à l'extérieur de la classe... C'est embêtant
     
   - attribut public : on préfixe l'attribut de 0 underscore (exemple : solde)
     objet.solde = 100  fonctionne, c'est normal
Pour protéger les attributs que l'on souhaite "privés", il faut utiliser des propriétés
sur un attribut public ou protégé qui transfera la valeur sur l'attribut privé.
Cela protège contre les affectations de type :  objet._solde = 100
"""

class Compte:

   def __init__(self, soldeAccesModif=0):
      """ constructeur, on utilise un attribut public pour accéder à un attribut privé : 
          soldeAccesModif -> __solde """
      self.__set_solde(soldeAccesModif)

   def __get_solde(self):
      """ cette méthode est appelée quand on souhaite accéder en lecture à soldeAccesModif,
          retourne la valeur de l'attribut privé __solde """
      print("Exécution __get_solde() ... lit __solde")
      return self.__solde

   def __set_solde(self, soldeAccesModif):
      """ cette méthode est appelée quand on souhaite accéder en écriture à soldeAccesModif,
          modifie l'attribut privé __solde """
      print("Exécution __set_solde() ... modifie __solde")
      if soldeAccesModif < 0:
         print("ATTENTION ! Solde mis à 0 €, ne peut pas être initialisé à {} €" \
                .format(soldeAccesModif))
         self.__solde = 0
      else:
         self.__solde = soldeAccesModif
   
   def get_solde(self):
      """ retourne valeur de __solde """
      return self.__solde

   def set_solde(self, soldeAccesModif):
      """ modifie la valeur de __solde """
      self.__set_solde(soldeAccesModif)

   # signale à python que attribut public soldeAccesModif vers une propriété
   soldeAccesModif = property(__get_solde, __set_solde)
   
if __name__ == "__main__":
   print("Création objet compte1 avec :   compte1 = Compte(110)")
   compte1 = Compte(110)
   print("compte1.__dict__ = {}\n".format(compte1.__dict__))
   
   print("Affichage contenu attribut privé avec :   print(compte1._Compte__solde)")
   print("Pour montrer que python permet de tout voir !")
   print("__solde = {}\n".format(compte1._Compte__solde))
   
   print("Affichage attribut privé en passant par attribut public avec la commande :")
   print("   print(compte1.soldeAccesModif)")
   print("__solde = {} \n".format(compte1.soldeAccesModif))

   print("Affichage attribut privé en passant par méthode get_solde : print(compte1.get_solde())")
   print("C'est la bonne façon de faire pour afficher un attribut privé")
   print("__solde = {} \n".format(compte1.get_solde()))
   
   print("On souhaite modifier le contenu de l'attribut privé __solde.")
   print("On ne peut pas modifier un attribut privé comme ceci :   compte1.__solde = -24")
   print("Cela lève une exception de type AttributeError. C'est une 1ère protection, contournable !\n")

   print("Modification contenu attribut privé avec :   compte1._Compte__solde = -24")
   print("Pour montrer que python permet de modifier un attribut privé ! ")
   print("          ***** NE JAMAIS FAIRE DE CETTE FACON  ! *****")
   print("L'affectation n'est pas passée par la méthode __set_solde... Très embêtant !")
   # compte1.__solde = -24   # génère une erreur, lève une exception AttributeError
      # builtins.AttributeError: 'Compte' object has no attribute '_Compte__soldePrive'
   compte1._Compte__solde = -24 # modifie valeur de l'attribut "privé", NE JAMAIS FAIRE CELA !
   print("__solde = {}\n".format(compte1._Compte__solde))

   print("Modification contenu attribut privé avec :   compte1.soldeAccesModif = -24")
   print("Pourquoi pas ! L'affectation appelle la méthode __set_solde qui vérifie la maj du solde")
   print("Le nouveau solde ne peut pas prendre de valeurs négatives, donc __solde est mis à 0")
   compte1.soldeAccesModif = -24
   print("__solde = {} \n".format(compte1.soldeAccesModif))
   
   print("Modification contenu attribut privé avec :   compte1.set_solde(-24)")
   print("C'est la méthode qu'il faut utiliser... elle appelle la méthode __set_solde...")
   print("Le nouveau solde ne peut pas prendre de valeurs négatives, donc __solde est mis à 0")
   compte1.set_solde(-24)
   print("__solde = {} \n".format(compte1.soldeAccesModif))
