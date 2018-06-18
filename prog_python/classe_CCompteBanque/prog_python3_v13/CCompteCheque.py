#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : CCompteCheque.py       version 1.3
Date : 11-03-2018
Auteur : Hervé Dugast

------- affichage console ------------------------------------------------------
*** Création de comptes chèques
... type compte : CHEQ
Découvert autorisé ? 100
solde du compte ? -200
Erreur ! Le solde (-200.00 €) doit être supérieur ou égal à -100.00 € ! 
Saisir un solde valide ? 0
   * Récapitulatif *
   - Compte CHEQ n° 100-1
     solde compte = 0.00, découvert autorisé = 100.00

... type compte : CHEQ
Découvert autorisé ? 200
solde compte = 100.00
   * Récapitulatif *
   - Compte CHEQ n° 100-2
     solde compte = 100.00, découvert autorisé = 200.00

... type compte : CHEQ
découvert autorisé = 500.00
solde compte = -10.00
   * Récapitulatif *
   - Compte CHEQ n° 100-3
     solde compte = -10.00, découvert autorisé = 500.00

... type compte : CHEQ
découvert autorisé = 0.00
solde compte = -10.00
Erreur ! Le solde (-10.00 €) doit être supérieur ou égal à 0.00 € ! 
Saisir un solde valide ? 50.25
   * Récapitulatif *
   - Compte CHEQ n° 100-4
     solde compte = 50.25, découvert autorisé = 0.00

***Affichage compte
Compte n° 100-1 : solde = 0.0, découvert autorisé = 100.0
compte1.__dict__ = {'_CCompteCheque__decouvertAutorise': 100.0, '_numero': '100-1',
'_CCompteCheque__type': 'CHEQ', '_CCompteBanque__solde': 0.0}

   - Compte CHEQ n° 100-1
     solde compte = 0.00, découvert autorisé = 100.00
   - Compte CHEQ n° 100-2
     solde compte = 100.00, découvert autorisé = 200.00
   - Compte CHEQ n° 100-3
     solde compte = -10.00, découvert autorisé = 500.00
   - Compte CHEQ n° 100-4
     solde compte = 50.25, découvert autorisé = 0.00

Nombre total de comptes bancaires : 4
--------------------------------------------------------------------------------
"""

from CCompteBanque import CCompteBanque

class CCompteCheque(CCompteBanque):
   """ gère les opérations courantes d'un compte chèque
   """
   
   TYPE = "CHEQ"
   
   def __init__(self, solde=-1, decouvertAutorise=-1):
      """ constructeur 
      """
      print("... type compte : {}".format(CCompteCheque.TYPE))
      self.__type = CCompteCheque.TYPE
      self.set_decouvertAutorise(decouvertAutorise)
      # il faut connaître le découvert autorisé avant de donner une valeur au solde
      CCompteBanque.__init__(self, solde, self.__decouvertAutorise*-1, self.__type)
      print("   * Récapitulatif *")
      self.afficherInformations()
      
   def __str__(self):
      """ affichage par défaut de l'objet
      """
      return "Compte n° {} : solde = {}, découvert autorisé = {}" \
             .format(self._numero, self.get_solde(), self.__decouvertAutorise)
   
   def afficherInformations(self):
      """ Affiche les informations du compte bancaire
      """
      print("   - Compte {} n° {}".format(self.__type, self._numero))
      print("     solde compte = {:.02f}, découvert autorisé = {:.02f}" \
            .format(self.get_solde(), self.__decouvertAutorise))
      
   def set_decouvertAutorise(self, decouvertAutorise):
      """ Renseigne le découvert autorisé à partir du clavier ou de la valeur passée par paramètre
      """
      if decouvertAutorise >= 0:
         # affiche découvert autorisé si valeur passée par paramètre est valide
         print("découvert autorisé = {:.02f}".format(decouvertAutorise))
      else:
         # découvert autorisé non valide ou pas encore saisi
         while decouvertAutorise < 0:
            if decouvertAutorise != -1:
               print("Erreur ! Le découvert autorisé ({:.02f} €) doit être supérieur ou égal à 0 !"\
                     .format(decouvertAutorise))
            decouvertAutorise = float(input("Découvert autorisé ? "))
      self.__decouvertAutorise = decouvertAutorise
      
   def get_type(self):
      return self.__type
   
# Test de la classe
if __name__ == "__main__":
   print("*** Création de comptes chèques")
   # crée un compte chèque avec demande saisie découvert et solde
   compte1 = CCompteCheque() ; print("")
   # crée un compte chèque avec demande saisie découvert
   compte2 = CCompteCheque(100) ; print("")
   # crée un compte chèque sans demande de saisie 
   compte3 = CCompteCheque(-10, 500) ; print("")
   # crée un compte chèque sans demande de saisie, mais avec une incohérence solde < découvert
   # demande une valeur de solde valide
   compte4 = CCompteCheque(-10, 0)
    
   print("\n***Affichage compte")
   print(compte1)
   print("compte1.__dict__ = {}".format(compte1.__dict__)) ; print("")
   compte1.afficherInformations()
   compte2.afficherInformations()
   compte3.afficherInformations()
   compte4.afficherInformations() ; print("")
   
   CCompteBanque.afficherNombreComptesExistant()

   