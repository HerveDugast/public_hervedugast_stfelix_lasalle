#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : CCompteEpargne.py  (partiel)     version 1.3
   ***** PARTIES créer nouveau client et nouveau compte bancaire uniquement *****
Date : 11-03-2018
Auteur : Hervé Dugast
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
