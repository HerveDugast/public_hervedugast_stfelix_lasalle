#!/usr/bin/python3.4
# coding: utf-8
"""
Programme (classe) : CCompteCheque.py       version 1.4
Date : 13-04-2018
Auteur : Hervé Dugast

------- affichage console ------------------------------------------------------
*** Création de comptes chèques
Exécution de compte1 = CCompteCheque()
... type compte : CHEQ
Découvert autorisé ? 200
Erreur ! Le découvert autorisé (200.00 €) doit être inférieur ou égal à 0 !
Découvert autorisé ? -200
solde du compte ? 0
   * Récapitulatif *
   - Compte CHEQ n° 100-1
     solde compte = 0.00, découvert autorisé = -200.00

Exécution de compte2 = CCompteCheque(-100)
... type compte : CHEQ
Découvert autorisé ? 0
solde compte = -100.00
Erreur ! Le solde (-100.00 €) doit être supérieur ou égal à 0.00 € ! 
Saisir un solde valide ? 10
   * Récapitulatif *
   - Compte CHEQ n° 100-2
     solde compte = 10.00, découvert autorisé = 0.00

Exécution de compte3 = CCompteCheque(-10,500)
... type compte : CHEQ
découvert autorisé = -500.00
solde compte = -136.25
   * Récapitulatif *
   - Compte CHEQ n° 100-3
     solde compte = -136.25, découvert autorisé = -500.00

Exécution de compte4 = CCompteCheque(-10, 0)
... type compte : CHEQ
découvert autorisé = 0.00
solde compte = -10.00
Erreur ! Le solde (-10.00 €) doit être supérieur ou égal à 0.00 € ! 
Saisir un solde valide ? 10
   * Récapitulatif *
   - Compte CHEQ n° 100-4
     solde compte = 10.00, découvert autorisé = 0.00

***Affichage compte
Compte n° 100-1 : solde = 0.0, découvert autorisé = -200.0
compte1.__dict__ = {'_CCompteCheque__type': 'CHEQ', '_numero': '100-1', '_CCompteCheque__decouvertAutorise': -200.0, '_CCompteBanque__solde': 0.0}

   - Compte CHEQ n° 100-1
     solde compte = 0.00, découvert autorisé = -200.00
   - Compte CHEQ n° 100-2
     solde compte = 10.00, découvert autorisé = 0.00
   - Compte CHEQ n° 100-3
     solde compte = -136.25, découvert autorisé = -500.00
   - Compte CHEQ n° 100-4
     solde compte = 10.00, découvert autorisé = 0.00

Nombre total de comptes bancaires : 4
--------------------------------------------------------------------------------
"""

from CCompteBanque import CCompteBanque

class CCompteCheque(CCompteBanque):
   """ gère les opérations courantes d'un compte chèque
   """
   
   TYPE = "CHEQ"
   
   def __init__(self, solde=-1, decouvertAutorise=1):
      """ constructeur 
      """
      print("... type compte : {}".format(CCompteCheque.TYPE))
      self.__type = CCompteCheque.TYPE
      self.set_decouvertAutorise(decouvertAutorise)
      # il faut connaître le découvert autorisé avant de donner une valeur au solde
      CCompteBanque.__init__(self, solde, self.__decouvertAutorise, self.__type)
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
      
   def retirerArgent(self, somme=-1):
      """ Retire une somme d'argent (nombre positif) sur le compte indiqué
      """
      CCompteBanque.retirerArgent(self, somme)
      # modifie la valeur du solde en fonction de la somme retirée, si cela est possible
      # recupère solde minimal en fonction du type de compte
      if self.get_solde() - somme >= self.__decouvertAutorise:
         # Le solde du compte doit être supérieur ou égal au découvert autorisé après le retrait
         self.set_solde(self.get_solde()-somme, self.__decouvertAutorise)
         codeResult = 0
      else:
         # pas assez d'argent sur le compte pour retirer la somme demandée
         codeResult = 33
         self.__afficherResultatOperation(codeResult)
      self.afficherInformations()   
      return codeResult
      
   def set_decouvertAutorise(self, decouvertAutorise):
      """ Renseigne le découvert autorisé à partir du clavier ou de la valeur passée par paramètre
      """
      if decouvertAutorise <= 0:
         # affiche découvert autorisé si valeur passée par paramètre est valide
         print("découvert autorisé = {:.02f}".format(decouvertAutorise))
      else:
         # découvert autorisé non valide ou pas encore saisi
         while decouvertAutorise > 0:
            if decouvertAutorise != 1:
               print("Erreur ! Le découvert autorisé ({:.02f} €) doit être inférieur ou égal à 0 !"\
                     .format(decouvertAutorise))
            decouvertAutorise = float(input("Découvert autorisé ? "))
      self.__decouvertAutorise = decouvertAutorise
      
   def get_type(self):
      return self.__type
   
   def get_decouvertAutorise(self):
      return self.__decouvertAutorise
   
   def __afficherResultatOperation(self, codeResult, *args):
      """ Affiche un message en fonction du résultat de l'opération demandé
          Le message affiché est de type "succès" ou "échec". Dans ce dernier cas, on affiche
          le code d'erreur avec une courte description du problème rencontré
          *args : liste contenant les éventuels arguments (n° client...) envoyés à la fonction
      """
      # ----- erreur 3x ----- : erreurs liés au module CCompteCheque
      # erreur 33 : args[1] -> typeCompte
      if codeResult == 33:
         print("ERREUR {}, échec {}.retirerArgent(), solde insuffisant pour retrait demandé !".format(codeResult, __name__))
   
# Test de la classe
if __name__ == "__main__":
   print("*** Création de comptes chèques")
   # crée un compte chèque avec demande saisie découvert et solde
   print("Exécution de {}".format("compte1 = CCompteCheque()"))
   compte1 = CCompteCheque() ; print("")
   # crée un compte chèque avec demande saisie découvert
   print("Exécution de {}".format("compte2 = CCompteCheque(-100)"))
   compte2 = CCompteCheque(-100) ; print("")
   # crée un compte chèque sans demande de saisie 
   print("Exécution de {}".format("compte3 = CCompteCheque(-10,500)"))
   compte3 = CCompteCheque(-136.25, -500) ; print("")
   # crée un compte chèque sans demande de saisie, mais avec une incohérence solde < découvert
   # demande une valeur de solde valide
   print("Exécution de {}".format("compte4 = CCompteCheque(-10, 0)"))
   compte4 = CCompteCheque(-10, 0)
    
   print("\n***Affichage compte")
   print(compte1)
   print("compte1.__dict__ = {}".format(compte1.__dict__)) ; print("")
   compte1.afficherInformations()
   compte2.afficherInformations()
   compte3.afficherInformations()
   compte4.afficherInformations() ; print("")
   
   CCompteBanque.afficherNombreComptesExistant()


