#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : CCompteEpargne.py       version 1.3
Date : 11-03-2018
Auteur : Hervé Dugast

------- affichage console -----------------------------------------------------------------
*** Création de comptes épargnes
... type compte : EPAR
Saisir le solde minimal (supérieur ou égal à 0) ? 10
solde du compte ? 0
Erreur ! Le solde (0.00 €) doit être supérieur ou égal à 10.00 € ! 
Saisir un solde valide ? 150
   * Récapitulatif *
   - Compte EPAR n° 200-1
     solde compte = 150.00, solde minimal = 10.00, intérêts = 0.00

... type compte : EPAR
Saisir le solde minimal (supérieur ou égal à 0) ? 10
solde compte = 150.63
   * Récapitulatif *
   - Compte EPAR n° 200-2
     solde compte = 150.63, solde minimal = 10.00, intérêts = 0.00

... type compte : EPAR
Solde minimal = 10.00
solde compte = 0.00
Erreur ! Le solde (0.00 €) doit être supérieur ou égal à 10.00 € ! 
Saisir un solde valide ? 111.27
   * Récapitulatif *
   - Compte EPAR n° 200-3
     solde compte = 111.27, solde minimal = 10.00, intérêts = 0.00

... type compte : EPAR
Solde minimal = 10.00
solde compte = 1251.24
   * Récapitulatif *
   - Compte EPAR n° 200-4
     solde compte = 1251.24, solde minimal = 10.00, intérêts = 0.00

***Affichage compte
Compte n° 200-1 : solde compte = 150.0, solde minimal = 10.0, intérêts = 0
compte1.__dict__ = {'_numero': '200-1', '_CCompteBanque__solde': 150.0, 
'_CCompteEpargne__soldeMinimal': 10.0, '_CCompteEpargne__interets': 0,
'_CCompteEpargne__type': 'EPAR'}

   - Compte EPAR n° 200-1
     solde compte = 150.00, solde minimal = 10.00, intérêts = 0.00
   - Compte EPAR n° 200-2
     solde compte = 150.63, solde minimal = 10.00, intérêts = 0.00
   - Compte EPAR n° 200-3
     solde compte = 111.27, solde minimal = 10.00, intérêts = 0.00
   - Compte EPAR n° 200-4
     solde compte = 1251.24, solde minimal = 10.00, intérêts = 0.00

Nombre total de comptes bancaires : 4
-------------------------------------------------------------------------------------------
"""
from CCompteBanque import CCompteBanque  


class CCompteEpargne(CCompteBanque):
   """ gère les opérations courantes d'un compte épargne
   """
   
   TYPE = "EPAR"

   def __init__(self, solde=-1, soldeMinimal=-1):
      """ constructeur
      """
      print("... type compte : {}".format(CCompteEpargne.TYPE))
      self.__type = CCompteEpargne.TYPE
      self.set_soldeMinimal(soldeMinimal)  
      self.__interets = 0
      # il faut connaître le solde minimal autorisé du compte avant de donner une valeur au solde
      CCompteBanque.__init__(self, solde, self.__soldeMinimal, self.__type)
      print("   * Récapitulatif *")
      self.afficherInformations()
      
   def __str__(self):
      """ affichage par défaut de l'objet
      """
      return "Compte n° {} : solde compte = {}, solde minimal = {}, intérêts = {}" \
             .format(self._numero, self.get_solde(), self.__soldeMinimal, self.__interets)

   def afficherInformations(self):
      """ Affiche les informations du compte bancaire
      """
      print("   - Compte {} n° {}".format(self.__type, self._numero))
      print("     solde compte = {:.02f}, solde minimal = {:.02f}, intérêts = {:.02f}" \
            .format(self.get_solde(), self.__soldeMinimal, self.__interets))

   def set_soldeMinimal(self, soldeMinimal):
      """ Renseigne le solde minimal autorisé pour ce compte à partir du clavier ou de la valeur
          passée par paramètre.
          Le solde minimal d'un compte épargne ne peut pas être négatif
      """
      if soldeMinimal >= 0:
         # affiche solde minimal si valeur passée par paramètre est valide
         print("Solde minimal = {:.02f}".format(soldeMinimal))
      else:
         # solde minimal non valide ou pas encore saisi
         while soldeMinimal < 0:
            if soldeMinimal != -1:
               print("Erreur ! Le solde minimal ne peut pas être négatif ({:.02f} €) ! " \
                     .format(soldeMinimal))
            soldeMinimal = float(input("Saisir le solde minimal (supérieur ou égal à 0) ? "))
      self.__soldeMinimal = soldeMinimal
      
   def get_type(self):
      return self.__type
   

if __name__ == "__main__":
   print("*** Création de comptes épargnes")
   # crée un compte épargne avec demande saisie solde minimal et solde compte
   compte1 = CCompteEpargne() ; print("")
   # crée un compte épargne avec demande saisie solde minimal
   compte2 = CCompteEpargne(150.63) ; print("")
   # crée un compte épargne sans demande de saisie
   compte3 = CCompteEpargne(0, 10) ; print("")
   # crée un compte épargne sans demande de saisie mais avec une incohérence solde < solde minimal
   # demande une valeur de solde valide
   compte4 = CCompteEpargne(1251.24, 10)

   print("\n***Affichage compte")
   print(compte1)
   print("compte1.__dict__ = {}".format(compte1.__dict__)) ; print("")
   compte1.afficherInformations()
   compte2.afficherInformations()
   compte3.afficherInformations()
   compte4.afficherInformations() ; print("")
   
   CCompteBanque.afficherNombreComptesExistant()
