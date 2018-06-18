/**************************************************************************************************
Programme : ruban8806test.ino       Version : 1.0           Version arduino : 1.6.12
Auteur : H. Dugast                  Date : 04-05-2017

Matériel utilisé : Arduino Mega 2560, carte Mega shield grove, module grove Potentiometer
ruban lumineux bus SPI type LPD8806 (nombre de LED paramétrable)
Connexions réalisées sur carte Mega : Potentiometer -> A0-A1 megashield, LED -> D2-D3 megashield

Fonctionnement du programme :
Test de ruban lumineux de qques cm jusqu'à 5 mètres de LED strip adressables (1 à 160 LED)
Commande du ruban de LED basé sur le LPD8806

• Pour tester une séquence particulière, changer la valeur de la constante : 
  SEQUENCE_A_TESTER = numeroSequence  (entier entre 0 et 6)
• Pour tester toutes les séquences : SEQUENCE_A_TESTER = 9    et définir le temps à passer sur 
  chaque séquence avec : BASE_TEMPS = dureeEnMs  (exemple : 3000 -> 3000 ms -> 3 sec)
**************************************************************************************************/
#include <Ruban8806.h>
#include <SPI.h>		// pour bus SPI

// ------------- paramètres base de temps ---------------------------------------------------------
#define BASE_TEMPS   3000            // base de temps en millisecondes

// ------------- module potentiomètre -------------------------------------------------------------
const uint8_t POT_PIN = 0;   // numéro entrée analogique connectée au potentiomètre
uint16_t potCode;      // code numérique (0 à 1023) correspondant à position curseur potentiomètre

// ------------- ruban à LED ----------------------------------------------------------------------
const uint8_t SEQUENCE_A_TESTER = 9;  // choix entre séquence num 0 à 6      9 -> toutes les seq
const uint16_t NB_LED_RUBAN = 26;	// nombre de LED dans le ruban
const uint8_t SPI_MOSI_PIN = 51;    // signal DATA du bus SPI		(Mega -> 51, Uno -> 11)
const uint8_t SPI_CLOCK_PIN = 52;   // signal CLOCK du bus SPI		(Mega -> 52, Uno -> 13)
Ruban8806 ruban = Ruban8806(NB_LED_RUBAN, SPI_MOSI_PIN, SPI_CLOCK_PIN); // création objet ruban

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
         ruban.eteindre();
         ruban.preparerCouleurIntensite(1, NB_LED_RUBAN, Ruban8806::s_COUL_ROUGE, 100);
         ruban.allumer(); break;
      case 1:  // allumer  tout le ruban en bleu puis éteindre les LED n°3 à n°6
         ruban.preparerCouleurIntensite(1, NB_LED_RUBAN, Ruban8806::s_COUL_BLEU, 100);
         ruban.allumer(); 
         ruban.eteindreLedxALedy(3, 6); break;
      case 2:  // allumer une seule LED du ruban en blanc   
         ruban.eteindre();
         ruban.preparerCouleurIntensite(1, 1, Ruban8806::s_COUL_BLANC, 100);
         ruban.allumer(); break;
      case 3:  // allumer les LED de la 4è à la 10è en vert
         ruban.eteindre();
         ruban.preparerCouleurIntensite(4, 10, Ruban8806::s_COUL_VERT, 100);
         ruban.allumer(); break;
      case 4:  // allumer les LED proportionnellement à la position du curseur du potentiomètre
         pot_mesurerPositionCurseur();
         // Calcule le nombre de LED à allumer en fonction de la position du curseur du potentiomètre
         // map(value, fromLow, fromHigh, toLow, toHigh), change d'échelle : 0 à 1023 -> 0 à NB_LED
         ruban.set_nbLedOn((unsigned char)map((long)potCode, 0, 1023, 0, NB_LED_RUBAN));
         ruban.eteindre();
         ruban.preparerCouleurIntensite(0, ruban.get_nbLedOn(), ruban.s_COUL_BLEU, 100);
         ruban.allumer(); break;
      case 5:  // allumer les LED avec un dégradé d'une couleur vers une autre couleur
         ruban.eteindre();
         ruban.preparerCouleurDegrade(ruban.s_COUL_VERT, ruban.s_COUL_ROUGE, 15, NB_LED_RUBAN);
         ruban.allumer(); break;
      case 6:  // allumer les LED avec un dégradé d'une couleur vers une autre couleur 
               // proportionnellement à la position du curseur du potentiomètre
         ruban.eteindre();
         ruban.preparerCouleurDegrade(ruban.s_COUL_VERT, ruban.s_COUL_ROUGE, 15, NB_LED_RUBAN);
         pot_mesurerPositionCurseur();
         // Calcule le nombre de LED à allumer en fonction de la position du curseur du potentiomètre
         // map(value, fromLow, fromHigh, toLow, toHigh), change d'échelle : 0 à 1023 -> 0 à NB_LED
         ruban.set_nbLedOn((unsigned char)map((long)potCode, 0, 1023, 0, NB_LED_RUBAN));
         if (ruban.get_nbLedOn() != NB_LED_RUBAN)
            ruban.eteindreLedxALedy(ruban.get_nbLedOn() + 1, NB_LED_RUBAN);
         ruban.allumer(); break;
      case 7:
         ruban.eteindre();
      }

      millisPrec = millisNow;
      numSequence++;    // passage à la séquence suivante
      if (numSequence > 7)   numSequence = 0;   // retour à la première séquence
      ruban.afficherVariableMembre();
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

// -------------------------------------------------------------------------------------------
// Change l'etat de la LED (basculement)
// -------------------------------------------------------------------------------------------
void led_changerEtat()
{
   digitalWrite(LED_PIN, !digitalRead(LED_PIN));
}

