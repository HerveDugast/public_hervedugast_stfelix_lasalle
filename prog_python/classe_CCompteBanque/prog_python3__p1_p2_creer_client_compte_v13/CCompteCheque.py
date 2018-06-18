#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : CCompteCheque.py   (partiel)    version 1.3
   ***** PARTIES créer nouveau client et nouveau compte bancaire uniquement *****
Date : 11-03-2018
Auteur : Hervé Dugast
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

   