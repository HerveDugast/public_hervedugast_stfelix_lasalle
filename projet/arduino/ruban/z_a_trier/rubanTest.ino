/**************************************************************************************************
Programme : rubanTest.ino      Version : 1.0           Version arduino : 1.6.12
Auteur : H. Dugast                  Date : 04-05-2017

Matériel utilisé : Arduino Mega 2560, carte Mega shield grove, module grove Potentiometer
ruban lumineux bus SPI type LPD8806 (nombre de LED paramétrable)
Connexions réalisées sur carte Mega : Potentiometer -> A0-A1 megashield, LED -> D2-D3 megashield

Fonctionnement du programme :
Test de ruban lumineux de qques cm jusqu'à 5 mètres de LED strip adressables (1 à 160 LED)
Commande du ruban de LED basé sur le LPD8806
**************************************************************************************************/
#include <LPD8806.h>	// pour ruban à LED strip adressable
#include <SPI.h>		// pour bus SPI

// ------------- paramètres base de temps ---------------------------------------------------------
#define BASE_TEMPS   1000            // base de temps en millisecondes
const uint16_t DUREE_DEBUG_EN_MS = 2000;

// ------------- module potentiomètre -------------------------------------------------------------
const uint8_t POT_PIN = 0;   // numéro entrée analogique connectée au potentiomètre
uint16_t potCode;      // code numérique (0 à 1023) correspondant à position curseur potentiomètre

// ------------- ruban à LED ----------------------------------------------------------------------
const uint8_t SEQUENCE_A_TESTER = 9;  // choix entre séquence num 0 à 6      9 -> toutes les seq
const uint16_t NB_LED_RUBAN = 26;	// nombre de LED dans le ruban
const uint8_t SPI_MOSI_PIN = 51;    // signal DATA du bus SPI		(Mega -> 51, Uno -> 11)
const uint8_t SPI_CLOCK_PIN = 52;   // signal CLOCK du bus SPI		(Mega -> 52, Uno -> 13)
LPD8806 ruban = LPD8806(NB_LED_RUBAN, SPI_MOSI_PIN, SPI_CLOCK_PIN); // création objet ruban
uint16_t nbLedOn = 0;         // nombre de LED à allumer dans le ruban
                              // Définit les couleurs de LED que peut prendre le ruban
const uint8_t NB_COULEUR = 5;     // nombre de couleurs programmées
                                  // ATTENTION, les couleurs sont codées sur 7 bits donc de 0 à 127
uint8_t couleurRuban[NB_COULEUR][3] = { 0,   0,   0,  // éteint : R = 0   G = 0   B = 0
0,   0, 127,  // bleu :  (R, G, B)= (0, 0, 127)
0, 127,   0,  // vert
127,   0,   0,  // rouge
127, 127, 127   // blanc
};
const uint8_t COULEUR_BLEU = 1;   // élément RGB correspondant à couleur dans liste couleurRuban
const uint8_t  COULEUR_VERT = 2;  // élément RGB correspondant à couleur dans liste couleurRuban
const uint8_t  COULEUR_ROUGE = 3; // élément RGB correspondant à couleur dans liste couleurRuban
const uint8_t  COULEUR_BLANC = 4; // élément RGB correspondant à couleur dans liste couleurRuban

                                  // ------------- autres ---------------------------------------------------------------------------
const unsigned char LED_PIN = 2;   // LED pour vérifier plantage

void setup()
{
   // Initialise la connexion SPI : MSB first, mode 0, clock 2 MHz, RAZ registres LED
   ruban.begin();	ruban.show(); // éteint toutes les LED
   pinMode(LED_PIN, OUTPUT);    // configure le port commandant la LED en sortie
   pinMode(POT_PIN, INPUT);   // configure la broche connectée au potentiomètre en ENTREE
   Serial.begin(115200);		// démarre la liaison serie
}

void loop()
{
   static uint16_t millisPrec = millis();// mémorise nb de millisecondes écoulées à un instant
   uint16_t millisNow;  // nb de millisecondes écoulées à cet instant
   static uint8_t numSequence = 0;  // numéro séquence pour tester les fonctions du ruban

   millisNow = millis(); // lit nb de millisecondes écoulées à cet instant
   
   if (SEQUENCE_A_TESTER != 9)   numSequence = SEQUENCE_A_TESTER;

   if (millisNow - millisPrec >= BASE_TEMPS)
   {
      led_changerEtat();   // clignotement LED pour vérifier que programme n'est pas planté
      switch (numSequence)
      {
      case 0:  // allumer tout le ruban en rouge
         ruban_eteindre();
         ruban_preparerCouleurIntensite(1, NB_LED_RUBAN, COULEUR_ROUGE, 100);
         ruban_allumer(); break;
      case 1:  // éteindre les LED n°3 à n°6
         ruban_eteindreLedxALedy(3, 6); break;
      case 2:  // allumer une seule LED du ruban en blanc   
         ruban_eteindre();
         ruban_preparerCouleurIntensite(1, 1, COULEUR_BLANC, 100);
         ruban_allumer(); break;
      case 3:  // allumer les LED de la 4è à la 10è en vert
         ruban_eteindre();
         ruban_preparerCouleurIntensite(4, 10, COULEUR_VERT, 100);
         ruban_allumer(); break;
      case 4:  // allumer les LED proportionnellement à la position du curseur du potentiomètre
         pot_mesurerPositionCurseur();
         // Calcule le nombre de LED à allumer en fonction de la position du curseur du potentiomètre
         // map(value, fromLow, fromHigh, toLow, toHigh), change d'échelle : 0 à 1023 -> 0 à NB_LED
         nbLedOn = (unsigned char)map((long)potCode, 0, 1023, 0, NB_LED_RUBAN);
         ruban_eteindre();
         ruban_preparerCouleurIntensite(0, nbLedOn, COULEUR_BLEU, 100);
         ruban_allumer(); break;
      case 5:  // allumer les LED avec un dégradé d'une couleur vers une autre couleur
         ruban_eteindre();
         ruban_preparerCouleurDegrade(COULEUR_VERT, COULEUR_ROUGE, 15, NB_LED_RUBAN);
         ruban_allumer(); break;
      case 6:  // allumer les LED avec un dégradé d'une couleur vers une autre couleur 
               // proportionnellement à la position du curseur du potentiomètre
         ruban_eteindre();
         ruban_preparerCouleurDegrade(COULEUR_VERT, COULEUR_ROUGE, 15, NB_LED_RUBAN);
         pot_mesurerPositionCurseur();
         // Calcule le nombre de LED à allumer en fonction de la position du curseur du potentiomètre
         // map(value, fromLow, fromHigh, toLow, toHigh), change d'échelle : 0 à 1023 -> 0 à NB_LED
         nbLedOn = (unsigned char)map((long)potCode, 0, 1023, 0, NB_LED_RUBAN);
         if (nbLedOn != NB_LED_RUBAN)
            ruban_eteindreLedxALedy(nbLedOn + 1, NB_LED_RUBAN);
         ruban_allumer(); break;
      case 7:
         ruban_eteindre();
      }

      millisPrec = millisNow;
      numSequence++;    // passage à la séquence suivante
      if (numSequence > 7)   numSequence = 0;   // retour à la première séquence
   }
}

//-------------------------------------------------------------------------------------------------
// Mesure la position du curseur du potentiomètre
// Retour :
//    uint16_t -> valeur proportionnelle à la position du curseur
//                curseur en position mini : 0    curseur en position maxi : 1023
//-------------------------------------------------------------------------------------------------
uint16_t pot_mesurerPositionCurseur()
{
   potCode = (uint16_t)analogRead(POT_PIN);
}

// ------------------------------------------------------------------------------------------------
// Allume le ruban suivant les paramètres enregistrées (valeurs registres)
// Les méthodes ruban_preparerCouleur... permettent de définir les couleurs de chaque point RGB
// ------------------------------------------------------------------------------------------------
void ruban_allumer()
{
   ruban.show(); // allume le ruban de LED en fonction des couleurs définies avant
}

// ------------------------------------------------------------------------------------------------
// Eteint toutes les LED du ruban 
// ------------------------------------------------------------------------------------------------
void ruban_eteindre()
{
   uint16_t ledNum;
   // charge couleur allumage des points dans registre (pas de couleur en fait)
   for (ledNum = 0; ledNum <= NB_LED_RUBAN; ledNum++)
   {
      ruban.setPixelColor(ledNum, 0);
   }
   ruban.show(); // allume le ruban de LED en fonction des couleurs définies avant
}

// ------------------------------------------------------------------------------------------------
// Eteint la plage de LED spécifiée du ruban  
//    numLedDebut -> numéro de la première LED à éteindre dans le ruban
//    numLedFin -> numéro de la dernière LED à éteindre dans le ruban
// ------------------------------------------------------------------------------------------------
void ruban_eteindreLedxALedy(uint8_t numLedDebut, uint8_t numLedFin)
{
   uint16_t ledNum;

   // vérification cohérence paramètres
   if (numLedDebut > NB_LED_RUBAN)   numLedDebut = NB_LED_RUBAN;
   if (numLedFin < numLedDebut)   numLedFin = numLedDebut;
   // Si demande allumage d'au moins une LED, numLedDebut doit être supérieur ou égal à 1
   if (numLedDebut == 0 && numLedFin != 0)   numLedDebut = 1;

   // charge couleur allumage des points dans registre (ici, RGB = 0 -> point éteint)
   for (ledNum = numLedDebut - 1; ledNum <= numLedFin - 1; ledNum++)
   {
      ruban.setPixelColor(ledNum, 0);
   }
   ruban.show(); // allume le ruban de LED en fonction des couleurs définies avant
}

// ------------------------------------------------------------------------------------------------
// Charge dans les registres la couleur de chaque point RGB à allumer. Les points s'allumeront 
// suivant les valeurs mémorisées dans les registres avec la méthode ruban.show() 
// paramètres : 
//    numLedDebut -> numéro de la première LED (1 à NB_LED), 0 -> aucun allumage
//    numLedFin ->   numéro de la dernière LED (1 à NB_LED et numLedFin >= numLedDebut)    0 -> OFF
//    couleurNum -> numéro de la couleur RGB (numéro élément RGB de la liste couleurRuban)
//    intensite -> intensite lumineuse des points en pourcentage (0 à 100%)    0 -> éteint
// ------------------------------------------------------------------------------------------------
void ruban_preparerCouleurIntensite(uint8_t numLedDebut, uint8_t numLedFin, uint8_t couleurNum,
   uint8_t intensite)
{
   uint16_t ledNum;
   uint16_t couleurTemp;
   uint8_t couleurNew[3];
   // vérification cohérence paramètres
   if (numLedDebut > NB_LED_RUBAN)   numLedDebut = NB_LED_RUBAN;
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
         couleurTemp = (uint16_t)couleurRuban[couleurNum][i] * (uint16_t)intensite / 100;
         couleurNew[i] = (uint8_t)couleurTemp;
      }

      // charge couleurNum allumage des points dans registre
      for (ledNum = numLedDebut - 1; ledNum <= numLedFin - 1; ledNum++)
      {
         ruban.setPixelColor(ledNum, couleurNew[0], couleurNew[1], couleurNew[2]);
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
void ruban_preparerCouleurDegrade(uint8_t coulDepart, uint8_t coulArrivee, uint8_t nbLedDegrad,
   uint8_t nbLedTotal)
{
   uint8_t couleurNow[3];

   // 

   for (int ledNum = 0; ledNum < nbLedDegrad; ledNum++)
   {
      for (int j = 0; j < 3; j++)
      {
         couleurNow[j] = couleurRuban[coulDepart][j];
         if (couleurRuban[coulArrivee][j] >= couleurRuban[coulDepart][j])
            couleurNow[j] = couleurRuban[coulDepart][j] +
            (couleurRuban[coulArrivee][j] - couleurRuban[coulDepart][j]) / (nbLedDegrad - 1) * ledNum;
         else
            couleurNow[j] = couleurRuban[coulDepart][j] -
            (couleurRuban[coulDepart][j] - couleurRuban[coulArrivee][j]) / (nbLedDegrad - 1) * ledNum;
      }
      ruban.setPixelColor(ledNum, couleurNow[0], couleurNow[1], couleurNow[2]);
   }
   // Définit la couleur 
   for (int ledNum = nbLedDegrad; ledNum < nbLedTotal; ledNum++)
      ruban.setPixelColor(ledNum, couleurRuban[coulArrivee][0], couleurRuban[coulArrivee][1],
         couleurRuban[coulArrivee][2]);
}

// -------------------------------------------------------------------------------------------
// Change l'etat de la LED (basculement)
// -------------------------------------------------------------------------------------------
void led_changerEtat()
{
   digitalWrite(LED_PIN, !digitalRead(LED_PIN));
}

//-------------------------------------------------------------------------------------------------
// DEBUG : Affiche les valeurs des variables dans un terminal
//-------------------------------------------------------------------------------------------------
void afficherVariableDebug()
{
   Serial.println("");
   Serial.print("potCode : "); Serial.println(potCode);
   Serial.print("nbLedOn : "); Serial.println(nbLedOn);
}

//-------------------------------------------------------------------------------------------------
// DEBUG : Affiche les valeurs des variables dans un terminal
//-------------------------------------------------------------------------------------------------
void afficherTableCouleur(uint8_t couleurNum)
{
   Serial.print("-- Couleur : "); Serial.println(couleurNum);
   Serial.print(couleurRuban[couleurNum][0]); Serial.print(" ");
   Serial.print(couleurRuban[couleurNum][1]); Serial.print(" ");
   Serial.print(couleurRuban[couleurNum][2]);
   Serial.println("");

   // affiche le contenu du tableau des couleurs mémorisées (couleurRuban)
   for(int i = 0; i < 3; i++)
      for (int j = 0; j < 3; j++)
      {
         Serial.print(i); Serial.print(" "); Serial.print(j); Serial.print(" : ");
         Serial.println(couleurRuban[i][j]);
      }
}