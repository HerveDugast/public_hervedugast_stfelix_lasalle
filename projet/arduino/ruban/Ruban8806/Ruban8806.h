#pragma once
/*-------------------------------------------------------------------------------------------------
Classe : Ruban8806.h       Version : 1.0           Version arduino : 1.6.12
Auteur : H. Dugast         Date : 05-05-2017
Fonction résumée : 
Test de ruban lumineux de qques cm jusqu'à 5 mètres de LED strip adressables (1 à 160 LED)
Commande du ruban de LED basé sur le composant LPD8806
------------------------------------------------------------------------------------------------ */
#include <Arduino.h>
#include <LPD8806.h>

class Ruban8806 : public LPD8806
{
public:
   // Constructeur
   Ruban8806(uint16_t nbLedRuban, uint8_t pinSpiMosiData, uint8_t pinSpiClock);
   ~Ruban8806();

   // Allume le ruban suivant les paramètres enregistrées (valeurs registres)
   // Les méthodes ruban_preparerCouleur... permettent de définir les couleurs de chaque point RGB
   void allumer();

   // Eteint toutes les LED du ruban 
   void eteindre();

   // Eteint la plage de LED spécifiée du ruban  
   //    numLedDebut -> numéro de la première LED à éteindre dans le ruban
   //    numLedFin -> numéro de la dernière LED à éteindre dans le ruban
   void eteindreLedxALedy(uint8_t numLedDebut, uint8_t numLedFin);

   // Charge dans les registres la couleur de chaque point RGB à allumer. Les points s'allumeront 
   // suivant les valeurs mémorisées dans les registres avec la méthode ruban.show() 
   // paramètres : 
   //    numLedDebut -> numéro de la première LED (1 à NB_LED), 0 -> aucun allumage
   //    numLedFin ->   numéro de la dernière LED (1 à NB_LED et numLedFin >= numLedDebut)    0 -> OFF
   //    couleurNum -> numéro de la couleur RGB (numéro élément RGB de la liste couleurRuban)
   //    intensite -> intensite lumineuse des points en pourcentage (0 à 100%)    0 -> éteint
   void preparerCouleurIntensite(uint8_t numLedDebut, uint8_t numLedFin, uint8_t couleurNum,
      uint8_t intensite);

   // Charge dans les registres un dégradé de 2 couleurs. Le dégradé (couleur Départ vers couleur 
   // arrivée) est calculé en fonction d'un nombre de LED donné. Possibilité de mettre les LED 
   // restantes à la couleur d'arrivée. 
   // L'évolution des teintes est calculée en fonction du nombre de LED concernées par le dégradé
   // Exemple : coulDepart = (0,100,0) -> vert, coulArrivee = (100,0,0) -> rouge,
   //           nbLedDegrad = 6, nbLedTotal = 10
   //    légende     cd : LED couleur départ    cg : LED couleur dégradé     ca : LED couleur arrivée
   //      ruban LED :           cd   cg   cg   cg   cg   ca   ca   ca   ca   ca
   //      évolution rouge R :    0   20   40   60   80  100  100  100  100  100
   //      évolution rouge G :  100   80   60   40   20    0    0    0    0    0
   //      évolution rouge B :    0    0    0    0    0    0    0    0    0    0
   // paramètres : 
   //    coulDepart -> numéro couleur RGB départ (numéro élément RGB de la liste couleurRuban)
   //    coulArrivee -> numéro couleur RGB arrivée (numéro élément RGB de la liste couleurRuban)
   //    nbLedDegrad -> nombre de LED où est appliqué le dégradé (en partant de la 1è LED)
   //    nbLedTotal ->  nombre de LED total, les LED de fin de ruban prennent la couleur d'arrivée
   void preparerCouleurDegrade(uint8_t coulDepart, uint8_t coulArrivee, uint8_t nbLedDegrad,
      uint8_t nbLedTotal);

   // DEBUG : Affiche les valeurs des variables dans un terminal
   void afficherVariableMembre();
   
   uint16_t get_nbLedRuban() { return m_nbLedRuban; }
//   const uint8_t* get_couleurPointRGB(uint8_t couleurPoint) { return s_COUL_POINT_RGB[couleurPoint]; }
   uint16_t get_nbLedOn() { return m_nbLedOn; }

   void set_nbLedOn(uint16_t nbLedOn) { m_nbLedOn = nbLedOn; };

   // constantes statiques

   // pour pointer une couleur RGB de la liste m_couleurPointRGB
   static const uint8_t s_COUL_ETEINT = 0;
   // pour pointer une couleur RGB de la liste m_couleurPointRGB
   static const uint8_t s_COUL_BLEU = 1;
   // pour pointer une couleur RGB de la liste m_couleurPointRGB
   static const uint8_t s_COUL_VERT = 2;
   // pour pointer une couleur RGB de la liste m_couleurPointRGB
   static const uint8_t s_COUL_ROUGE = 3;
   // pour pointer une couleur RGB de la liste m_couleurPointRGB
   static const uint8_t s_COUL_BLANC = 4;

   // pour pointer une couleur RGB de la liste m_couleurPointRGB
   static const uint8_t s_NB_COULEUR_MEM = 5;
   // Définit dans une liste certaines couleurs de LED que peut prendre le ruban
   // ATTENTION, les couleurs sont codées sur 7 bits donc R, G, B varie entre 0 à 127
   static const uint8_t s_COUL_POINT_RGB[s_NB_COULEUR_MEM][3];

protected:
   uint16_t m_nbLedRuban;	// nombre de LED dans le ruban
   uint8_t m_pinSpiMosiData = 51;    // signal DATA du bus SPI		(Mega -> 51, Uno -> 11)
   uint8_t m_pinSpiClock = 52;   // signal CLOCK du bus SPI		(Mega -> 52, Uno -> 13)
   uint16_t m_nbLedOn = 0;         // nombre de LED à commander dans le ruban
   
};

