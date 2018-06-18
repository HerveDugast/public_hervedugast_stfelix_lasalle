/**************************************************************************************************
Programme : rubanTest.ino      Version : 1.0           Version arduino : 1.6.12
Auteur : H. Dugast                  Date : 04-05-2017

Mat�riel utilis� : Arduino Mega 2560, carte Mega shield grove, module grove Potentiometer
ruban lumineux bus SPI type LPD8806 (nombre de LED param�trable)
Connexions r�alis�es sur carte Mega�: Potentiometer -> A0-A1 megashield, LED -> D2-D3 megashield

Fonctionnement du programme :
Test de ruban lumineux de qques cm jusqu'� 5 m�tres de LED strip adressables (1 � 160 LED)
Commande du ruban de LED bas� sur le LPD8806
**************************************************************************************************/
#include <Ruban8806.h>
//#include <LPD8806.h>	// pour ruban � LED strip adressable
#include <SPI.h>		// pour bus SPI

// ------------- param�tres base de temps ---------------------------------------------------------
#define BASE_TEMPS   1000            // base de temps en millisecondes
const uint16_t DUREE_DEBUG_EN_MS = 2000;

// ------------- module potentiom�tre -------------------------------------------------------------
const uint8_t POT_PIN = 0;   // num�ro entr�e analogique connect�e au potentiom�tre
uint16_t potCode;      // code num�rique (0 � 1023) correspondant � position curseur potentiom�tre

// ------------- ruban � LED ----------------------------------------------------------------------
const uint8_t SEQUENCE_A_TESTER = 9;  // choix entre s�quence num 0 � 6      9 -> toutes les seq
const uint16_t NB_LED_RUBAN = 26;	// nombre de LED dans le ruban
const uint8_t SPI_MOSI_PIN = 51;    // signal DATA du bus SPI		(Mega -> 51, Uno -> 11)
const uint8_t SPI_CLOCK_PIN = 52;   // signal CLOCK du bus SPI		(Mega -> 52, Uno -> 13)
Ruban8806 ruban = Ruban8806(NB_LED_RUBAN, SPI_MOSI_PIN, SPI_CLOCK_PIN); // cr�ation objet ruban

// ------------- autres ---------------------------------------------------------------------------
const unsigned char LED_PIN = 2;   // LED pour v�rifier plantage

void setup()
{
   // Initialise la connexion SPI : MSB first, mode 0, clock 2 MHz, RAZ registres LED
   ruban.begin();	ruban.show(); // �teint toutes les LED
   pinMode(LED_PIN, OUTPUT);    // configure le port commandant la LED en sortie
   pinMode(POT_PIN, INPUT);   // configure la broche connect�e au potentiom�tre en ENTREE
   Serial.begin(115200);		// d�marre la liaison serie
}

void loop()
{
   //static uint16_t millisPrec = millis();// m�morise nb de millisecondes �coul�es � un instant
   //uint16_t millisNow;  // nb de millisecondes �coul�es � cet instant
   //static uint8_t numSequence = 0;  // num�ro s�quence pour tester les fonctions du ruban

   //millisNow = millis(); // lit nb de millisecondes �coul�es � cet instant

   //if (SEQUENCE_A_TESTER != 9)   numSequence = SEQUENCE_A_TESTER;

   //if (millisNow - millisPrec >= BASE_TEMPS)
   //{
   //   led_changerEtat();   // clignotement LED pour v�rifier que programme n'est pas plant�
   //   switch (numSequence)
   //   {
   //   case 0:  // allumer tout le ruban en rouge
   //      ruban.eteindre();
   //      ruban.preparerCouleurIntensite(1, NB_LED_RUBAN, ruban::s_COUL_BLEU, 100);
   //      ruban.allumer(); break;
   //   case 1:  // �teindre les LED n�3 � n�6
   //      ruban.eteindreLedxALedy(3, 6); break;
   //   case 2:  // allumer une seule LED du ruban en blanc   
   //      ruban.eteindre();
   //      ruban.preparerCouleurIntensite(1, 1, ruban.s_COUL_ROUGE, 100);
   //      ruban.allumer(); break;
   //   case 3:  // allumer les LED de la 4� � la 10� en vert
   //      ruban.eteindre();
   //      ruban.preparerCouleurIntensite(4, 10, ruban.s_COUL_VERT, 100);
   //      ruban.allumer(); break;
   //   case 4:  // allumer les LED proportionnellement � la position du curseur du potentiom�tre
   //      pot_mesurerPositionCurseur();
   //      // Calcule le nombre de LED � allumer en fonction de la position du curseur du potentiom�tre
   //      // map(value, fromLow, fromHigh, toLow, toHigh), change d'�chelle : 0 � 1023 -> 0 � NB_LED
   //      ruban.set_nbLedOn( (unsigned char)map((long)potCode, 0, 1023, 0, NB_LED_RUBAN));
   //      ruban.eteindre();
   //      ruban.preparerCouleurIntensite(0, ruban.get_nbLedOn(), ruban.s_COUL_BLEU, 100);
   //      ruban.allumer(); break;
   //   case 5:  // allumer les LED avec un d�grad� d'une couleur vers une autre couleur
   //      ruban.eteindre();
   //      ruban.preparerCouleurDegrade(ruban.s_COUL_VERT, ruban.s_COUL_ROUGE, 15, NB_LED_RUBAN);
   //      ruban.allumer(); break;
   //   case 6:  // allumer les LED avec un d�grad� d'une couleur vers une autre couleur 
   //            // proportionnellement � la position du curseur du potentiom�tre
   //      ruban.eteindre();
   //      ruban.preparerCouleurDegrade(ruban.s_COUL_VERT, ruban.s_COUL_ROUGE, 15, NB_LED_RUBAN);
   //      pot_mesurerPositionCurseur();
   //      // Calcule le nombre de LED � allumer en fonction de la position du curseur du potentiom�tre
   //      // map(value, fromLow, fromHigh, toLow, toHigh), change d'�chelle : 0 � 1023 -> 0 � NB_LED
   //      ruban.set_nbLedOn((unsigned char)map((long)potCode, 0, 1023, 0, NB_LED_RUBAN));
   //      if (ruban.get_nbLedOn() != NB_LED_RUBAN)
   //         ruban.eteindreLedxALedy(ruban.get_nbLedOn() + 1, NB_LED_RUBAN);
   //      ruban.allumer(); break;
   //   case 7:
   //      ruban.eteindre();
   //   }

   //   millisPrec = millisNow;
   //   numSequence++;    // passage � la s�quence suivante
   //   if (numSequence > 7)   numSequence = 0;   // retour � la premi�re s�quence
   //}
}

//-------------------------------------------------------------------------------------------------
// Mesure la position du curseur du potentiom�tre
// Retour :
//    uint16_t -> valeur proportionnelle � la position du curseur
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

//-------------------------------------------------------------------------------------------------
// DEBUG : Affiche les valeurs des variables dans un terminal
//-------------------------------------------------------------------------------------------------
void afficherVariableDebug()
{
   Serial.println("");
   Serial.print("potCode : "); Serial.println(potCode);
}
