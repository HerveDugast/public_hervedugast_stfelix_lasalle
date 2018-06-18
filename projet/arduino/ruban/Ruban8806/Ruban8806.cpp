/*-------------------------------------------------------------------------------------------------
Classe : Ruban8806.cpp     Version : 1.0           Version arduino : 1.6.12
Auteur : H. Dugast         Date : 05-05-2017
Fonction résumée :
Test de ruban lumineux de qques cm jusqu'à 5 mètres de LED strip adressables (1 à 160 LED)
Commande du ruban de LED basé sur le composant LPD8806
------------------------------------------------------------------------------------------------ */
#include "Ruban8806.h"

// Définit dans une liste certaines couleurs de LED que peut prendre le ruban
// ATTENTION, les couleurs sont codées sur 7 bits donc R, G, B varie entre 0 à 127
const uint8_t Ruban8806::s_COUL_POINT_RGB[5][3] =
   { 0,   0,   0,  // éteint : R = 0   G = 0   B = 0
   0,   0, 127,  // bleu :  (R, G, B)= (0, 0, 127)
   0, 127,   0,  // vert
   127,   0,   0,  // rouge
   127, 127, 127   // blanc
   };

// pour pointer une couleur RGB de la liste m_couleurPointRGB
//s_COUL_ETEINT = 0;
//// pour pointer une couleur RGB de la liste m_couleurPointRGB
//static const uint8_t s_COUL_BLEU = 1;
//// pour pointer une couleur RGB de la liste m_couleurPointRGB
//static const uint8_t s_COUL_VERT = 2;
//// pour pointer une couleur RGB de la liste m_couleurPointRGB
//static const uint8_t s_COUL_ROUGE = 3;
//// pour pointer une couleur RGB de la liste m_couleurPointRGB
//static const uint8_t s_COUL_BLANC = 4;

// ------------------------------------------------------------------------------------------------
// Public : Constructeur, paramètres :
//    pinSpiMosiData -> numéro de broche bus SPI MOSI Data   (Mega -> 51, Uno -> 11)
//    pinSpiClock    -> numéro de broche bus SPI CLOCK       (Mega -> 52, Uno -> 13)
//    nbLedRuban     -> nombre de LED dans le ruban
// ------------------------------------------------------------------------------------------------
Ruban8806::Ruban8806(uint16_t nbLedRuban, uint8_t pinSpiMosiData, uint8_t pinSpiClock) : LPD8806(nbLedRuban, pinSpiMosiData, pinSpiClock)
{
   m_pinSpiMosiData = pinSpiMosiData;
   m_pinSpiClock = pinSpiClock;
   m_nbLedRuban = nbLedRuban;
   m_nbLedOn = 0;         // nombre de LED à commander dans le ruban
}

Ruban8806::~Ruban8806()
{
}

// ------------------------------------------------------------------------------------------------
// Allume le ruban suivant les paramètres enregistrées (valeurs registres)
// Les méthodes preparerCouleur... permettent de définir les couleurs de chaque point RGB
// ------------------------------------------------------------------------------------------------
void Ruban8806::allumer()
{
   show(); // allume le ruban de LED en fonction des couleurs définies avant
}

// ------------------------------------------------------------------------------------------------
// Eteint toutes les LED du ruban 
// ------------------------------------------------------------------------------------------------
void Ruban8806::eteindre()
{
   uint16_t ledNum;
   // charge couleur allumage des points dans registre (pas de couleur en fait)
   for (ledNum = 0; ledNum <= m_nbLedRuban; ledNum++)
   {
      setPixelColor(ledNum, 0);
   }
   show(); // allume le ruban de LED en fonction des couleurs définies avant
}

// ------------------------------------------------------------------------------------------------
// Eteint la plage de LED spécifiée du ruban  
//    numLedDebut -> numéro de la première LED à éteindre dans le ruban
//    numLedFin -> numéro de la dernière LED à éteindre dans le ruban
// ------------------------------------------------------------------------------------------------
void Ruban8806::eteindreLedxALedy(uint8_t numLedDebut, uint8_t numLedFin)
{
   uint16_t ledNum;

   // vérification cohérence paramètres
   if (numLedDebut > m_nbLedRuban)   numLedDebut = m_nbLedRuban;
   if (numLedFin < numLedDebut)   numLedFin = numLedDebut;
   // Si demande allumage d'au moins une LED, numLedDebut doit être supérieur ou égal à 1
   if (numLedDebut == 0 && numLedFin != 0)   numLedDebut = 1;

   // charge couleur allumage des points dans registre (ici, RGB = 0 -> point éteint)
   for (ledNum = numLedDebut - 1; ledNum <= numLedFin - 1; ledNum++)
   {
      setPixelColor(ledNum, 0);
   }
   show(); // allume le ruban de LED en fonction des couleurs définies avant
}

// ------------------------------------------------------------------------------------------------
// Charge dans les registres la couleur de chaque point RGB à allumer. Les points s'allumeront 
// suivant les valeurs mémorisées dans les registres avec la méthode show() 
// paramètres : 
//    numLedDebut -> numéro de la première LED (1 à NB_LED), 0 -> aucun allumage
//    numLedFin ->   numéro de la dernière LED (1 à NB_LED et numLedFin >= numLedDebut)    0 -> OFF
//    couleurNum -> numéro de la couleur RGB (numéro élément RGB de la liste couleurRuban)
//    intensite -> intensite lumineuse des points en pourcentage (0 à 100%)    0 -> éteint
// ------------------------------------------------------------------------------------------------
void Ruban8806::preparerCouleurIntensite(uint8_t numLedDebut, uint8_t numLedFin, uint8_t couleurNum,
   uint8_t intensite)
{
   uint16_t ledNum;
   uint16_t couleurTemp;
   uint8_t couleurNew[3];
   // vérification cohérence paramètres
   if (numLedDebut > m_nbLedRuban)   numLedDebut = m_nbLedRuban;
   if (numLedFin < numLedDebut)   numLedFin = numLedDebut;
   // Si demande allumage d'au moins une LED, numLedDebut doit être supérieur ou égal à 1
   if (numLedDebut == 0 && numLedFin != 0)   numLedDebut = 1;
   if (intensite > 100)   intensite = 100;

   // prépare les couleurs des LED du ruban si demande d'allumage d'au moins une LED
   if (numLedFin != 0)
   {
      // Ajuste l'intensité lumineuse des points (0 à 100%)
      for (int i = 0; i < 3; i++)
      {
         couleurTemp = (uint16_t)s_COUL_POINT_RGB[couleurNum][i] * (uint16_t)intensite / 100;
         couleurNew[i] = (uint8_t)couleurTemp;
      }

      // charge couleurNum allumage des points dans registre
      for (ledNum = numLedDebut - 1; ledNum <= numLedFin - 1; ledNum++)
      {
         setPixelColor(ledNum, couleurNew[0], couleurNew[1], couleurNew[2]);
      }
   }
}

// ------------------------------------------------------------------------------------------------
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
// ------------------------------------------------------------------------------------------------
void Ruban8806::preparerCouleurDegrade(uint8_t coulDepart, uint8_t coulArrivee, uint8_t nbLedDegrad,
   uint8_t nbLedTotal)
{
   uint8_t couleurNow[3];

   // 

   for (int ledNum = 0; ledNum < nbLedDegrad; ledNum++)
   {
      for (int j = 0; j < 3; j++)
      {
         couleurNow[j] = s_COUL_POINT_RGB[coulDepart][j];
         if (s_COUL_POINT_RGB[coulArrivee][j] >= s_COUL_POINT_RGB[coulDepart][j])
            couleurNow[j] = s_COUL_POINT_RGB[coulDepart][j] +
            (s_COUL_POINT_RGB[coulArrivee][j] - s_COUL_POINT_RGB[coulDepart][j]) / (nbLedDegrad - 1) * ledNum;
         else
            couleurNow[j] = s_COUL_POINT_RGB[coulDepart][j] -
            (s_COUL_POINT_RGB[coulDepart][j] - s_COUL_POINT_RGB[coulArrivee][j]) / (nbLedDegrad - 1) * ledNum;
      }
      setPixelColor(ledNum, couleurNow[0], couleurNow[1], couleurNow[2]);
   }
   // Définit la couleur 
   for (int ledNum = nbLedDegrad; ledNum < nbLedTotal; ledNum++)
      setPixelColor(ledNum, s_COUL_POINT_RGB[coulArrivee][0], s_COUL_POINT_RGB[coulArrivee][1],
         s_COUL_POINT_RGB[coulArrivee][2]);
}

//-------------------------------------------------------------------------------------------------
// DEBUG : Affiche les valeurs des variables dans un terminal
//-------------------------------------------------------------------------------------------------
void Ruban8806::afficherVariableMembre()
{
   Serial.println("--- Variables objet Ruban8806 ---");
   Serial.print("m_nbLedRuban : "); Serial.println(m_nbLedRuban);
   Serial.print("m_pinSpiMosiData : "); Serial.println(m_pinSpiMosiData);
   Serial.print("m_pinSpiClock : "); Serial.println(m_pinSpiClock);
   Serial.print("m_nbLedOn : "); Serial.println(m_nbLedOn);

   // affiche le contenu du tableau des couleurs mémorisées (couleurRuban)
   Serial.println("Contenu liste s_COUL_POINT_RGB[nbCouleur] : ");
   Serial.println("indiceCouleur  R  G  B");
   for (int i = 0; i < s_NB_COULEUR_MEM; i++)
   {
      Serial.print(i); Serial.print("\t"); 
      for (int j = 0; j < 3; j++)
      {
         Serial.print(s_COUL_POINT_RGB[i][j]);
         Serial.print("\t");
      }
      Serial.println("");
   }
   Serial.println("--- Fin objet Ruban8806 ---");
}