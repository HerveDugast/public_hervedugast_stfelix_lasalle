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
#include <LPD8806.h>	// pour ruban � LED strip adressable
#include <SPI.h>		// pour bus SPI

// ------------- param�tres base de temps ---------------------------------------------------------
#define BASE_TEMPS   1000            // base de temps en millisecondes
const uint16_t DUREE_DEBUG_EN_MS = 2000;

// ------------- module potentiom�tre -------------------------------------------------------------
const uint8_t POT_PIN = 0;   // num�ro entr�e analogique connect�e au potentiom�tre
uint16_t potCode;      // code num�rique (0 � 1023) correspondant � position curseur potentiom�tre

// ------------- ruban � LED ----------------------------------------------------------------------
const uint8_t SEQUENCE_A_TESTER = 9;  // choix entre s�quence num 0 � 6      9 -> toutes les seq
const uint16_t NB_LED_RUBAN = 160;	// nombre de LED dans le ruban
const uint8_t SPI_MOSI_PIN = 51;    // signal DATA du bus SPI		(Mega -> 51, Uno -> 11)
const uint8_t SPI_CLOCK_PIN = 52;   // signal CLOCK du bus SPI		(Mega -> 52, Uno -> 13)
LPD8806 ruban = LPD8806(NB_LED_RUBAN, SPI_MOSI_PIN, SPI_CLOCK_PIN); // cr�ation objet ruban
uint16_t nbLedOn = 0;         // nombre de LED � allumer dans le ruban
                              // D�finit les couleurs de LED que peut prendre le ruban
const uint8_t NB_COULEUR = 5;     // nombre de couleurs programm�es
                                  // ATTENTION, les couleurs sont cod�es sur 7 bits donc de 0 � 127
uint8_t couleurRuban[NB_COULEUR][3] = { 0,   0,   0,  // �teint : R = 0   G = 0   B = 0
0,   0, 127,  // bleu :  (R, G, B)= (0, 0, 127)
0, 127,   0,  // vert
127,   0,   0,  // rouge
127, 127, 127   // blanc
};
const uint8_t COULEUR_BLEU = 1;   // �l�ment RGB correspondant � couleur dans liste couleurRuban
const uint8_t  COULEUR_VERT = 2;  // �l�ment RGB correspondant � couleur dans liste couleurRuban
const uint8_t  COULEUR_ROUGE = 3; // �l�ment RGB correspondant � couleur dans liste couleurRuban
const uint8_t  COULEUR_BLANC = 4; // �l�ment RGB correspondant � couleur dans liste couleurRuban

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
   static uint16_t millisPrec = millis();// m�morise nb de millisecondes �coul�es � un instant
   uint16_t millisNow;  // nb de millisecondes �coul�es � cet instant
   static uint8_t numSequence = 0;  // num�ro s�quence pour tester les fonctions du ruban

   millisNow = millis(); // lit nb de millisecondes �coul�es � cet instant
   
   if (SEQUENCE_A_TESTER != 9)   numSequence = SEQUENCE_A_TESTER;

   if (millisNow - millisPrec >= BASE_TEMPS)
   {
      led_changerEtat();   // clignotement LED pour v�rifier que programme n'est pas plant�
      switch (numSequence)
      {
      case 0:  // allumer tout le ruban en rouge
         ruban_eteindre();
         ruban_preparerCouleurIntensite(1, NB_LED_RUBAN, COULEUR_ROUGE, 100);
         ruban_allumer(); break;
      case 1:  // �teindre les LED n�3 � n�6
         ruban_eteindreLedxALedy(3, 6); break;
      case 2:  // allumer une seule LED du ruban en blanc   
         ruban_eteindre();
         ruban_preparerCouleurIntensite(1, 1, COULEUR_BLANC, 100);
         ruban_allumer(); break;
      case 3:  // allumer les LED de la 4� � la 10� en vert
         ruban_eteindre();
         ruban_preparerCouleurIntensite(4, 10, COULEUR_VERT, 100);
         ruban_allumer(); break;
      case 4:  // allumer les LED proportionnellement � la position du curseur du potentiom�tre
         pot_mesurerPositionCurseur();
         // Calcule le nombre de LED � allumer en fonction de la position du curseur du potentiom�tre
         // map(value, fromLow, fromHigh, toLow, toHigh), change d'�chelle : 0 � 1023 -> 0 � NB_LED
         nbLedOn = (unsigned char)map((long)potCode, 0, 1023, 0, NB_LED_RUBAN);
         ruban_eteindre();
         ruban_preparerCouleurIntensite(0, nbLedOn, COULEUR_BLEU, 100);
         ruban_allumer(); break;
      case 5:  // allumer les LED avec un d�grad� d'une couleur vers une autre couleur
         ruban_eteindre();
         ruban_preparerCouleurDegrade(COULEUR_VERT, COULEUR_ROUGE, 15, NB_LED_RUBAN);
         ruban_allumer(); break;
      case 6:  // allumer les LED avec un d�grad� d'une couleur vers une autre couleur 
               // proportionnellement � la position du curseur du potentiom�tre
         ruban_eteindre();
         ruban_preparerCouleurDegrade(COULEUR_VERT, COULEUR_ROUGE, 15, NB_LED_RUBAN);
         pot_mesurerPositionCurseur();
         // Calcule le nombre de LED � allumer en fonction de la position du curseur du potentiom�tre
         // map(value, fromLow, fromHigh, toLow, toHigh), change d'�chelle : 0 � 1023 -> 0 � NB_LED
         nbLedOn = (unsigned char)map((long)potCode, 0, 1023, 0, NB_LED_RUBAN);
         if (nbLedOn != NB_LED_RUBAN)
            ruban_eteindreLedxALedy(nbLedOn + 1, NB_LED_RUBAN);
         ruban_allumer(); break;
      case 7:
         ruban_eteindre();
      }

      millisPrec = millisNow;
      numSequence++;    // passage � la s�quence suivante
      if (numSequence > 7)   numSequence = 0;   // retour � la premi�re s�quence
   }
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

// ------------------------------------------------------------------------------------------------
// Allume le ruban suivant les param�tres enregistr�es (valeurs registres)
// Les m�thodes ruban_preparerCouleur... permettent de d�finir les couleurs de chaque point RGB
// ------------------------------------------------------------------------------------------------
void ruban_allumer()
{
   ruban.show(); // allume le ruban de LED en fonction des couleurs d�finies avant
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
   ruban.show(); // allume le ruban de LED en fonction des couleurs d�finies avant
}

// ------------------------------------------------------------------------------------------------
// Eteint la plage de LED sp�cifi�e du ruban  
//    numLedDebut -> num�ro de la premi�re LED � �teindre dans le ruban
//    numLedFin -> num�ro de la derni�re LED � �teindre dans le ruban
// ------------------------------------------------------------------------------------------------
void ruban_eteindreLedxALedy(uint8_t numLedDebut, uint8_t numLedFin)
{
   uint16_t ledNum;

   // v�rification coh�rence param�tres
   if (numLedDebut > NB_LED_RUBAN)   numLedDebut = NB_LED_RUBAN;
   if (numLedFin < numLedDebut)   numLedFin = numLedDebut;
   // Si demande allumage d'au moins une LED, numLedDebut doit �tre sup�rieur ou �gal � 1
   if (numLedDebut == 0 && numLedFin != 0)   numLedDebut = 1;

   // charge couleur allumage des points dans registre (ici, RGB = 0 -> point �teint)
   for (ledNum = numLedDebut - 1; ledNum <= numLedFin - 1; ledNum++)
   {
      ruban.setPixelColor(ledNum, 0);
   }
   ruban.show(); // allume le ruban de LED en fonction des couleurs d�finies avant
}

// ------------------------------------------------------------------------------------------------
// Charge dans les registres la couleur de chaque point RGB � allumer. Les points s'allumeront 
// suivant les valeurs m�moris�es dans les registres avec la m�thode ruban.show() 
// param�tres : 
//    numLedDebut -> num�ro de la premi�re LED (1 � NB_LED), 0 -> aucun allumage
//    numLedFin ->   num�ro de la derni�re LED (1 � NB_LED et numLedFin >= numLedDebut)    0 -> OFF
//    couleurNum -> num�ro de la couleur RGB (num�ro �l�ment RGB de la liste couleurRuban)
//    intensite -> intensite lumineuse des points en pourcentage (0 � 100%)    0 -> �teint
// ------------------------------------------------------------------------------------------------
void ruban_preparerCouleurIntensite(uint8_t numLedDebut, uint8_t numLedFin, uint8_t couleurNum,
   uint8_t intensite)
{
   uint16_t ledNum;
   uint16_t couleurTemp;
   uint8_t couleurNew[3];
   // v�rification coh�rence param�tres
   if (numLedDebut > NB_LED_RUBAN)   numLedDebut = NB_LED_RUBAN;
   if (numLedFin < numLedDebut)   numLedFin = numLedDebut;
   // Si demande allumage d'au moins une LED, numLedDebut doit �tre sup�rieur ou �gal � 1
   if (numLedDebut == 0 && numLedFin != 0)   numLedDebut = 1;
   if (intensite > 100)   intensite = 100;

   // pr�pare les couleurs des LED du ruban si demande d'allumage d'au moins une LED
   if (numLedFin != 0)
   {
      // Ajuste l'intensit� lumineuse des points (0 � 100%)
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
// Charge dans les registres un d�grad� de 2 couleurs. Le d�grad� (couleur D�part vers couleur 
// arriv�e) est calcul� en fonction d'un nombre de LED donn�. Possibilit� de mettre les LED 
// restantes � la couleur d'arriv�e. 
// L'�volution des teintes est calcul�e en fonction du nombre de LED concern�es par le d�grad�
// Exemple : coulDepart = (0,100,0) -> vert, coulArrivee = (100,0,0) -> rouge,
//           nbLedDegrad = 6, nbLedTotal = 10
//    l�gende     cd : LED couleur d�part    cg : LED couleur d�grad�     ca : LED couleur arriv�e
//      ruban LED :           cd   cg   cg   cg   cg   ca   ca   ca   ca   ca
//      �volution rouge R :    0   20   40   60   80  100  100  100  100  100
//      �volution rouge G :  100   80   60   40   20    0    0    0    0    0
//      �volution rouge B :    0    0    0    0    0    0    0    0    0    0
// param�tres : 
//    coulDepart -> num�ro couleur RGB d�part (num�ro �l�ment RGB de la liste couleurRuban)
//    coulArrivee -> num�ro couleur RGB arriv�e (num�ro �l�ment RGB de la liste couleurRuban)
//    nbLedDegrad -> nombre de LED o� est appliqu� le d�grad� (en partant de la 1� LED)
//    nbLedTotal ->  nombre de LED total, les LED de fin de ruban prennent la couleur d'arriv�e
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
   // D�finit la couleur 
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
void afficherCouleur(uint8_t couleurNum)
{
   Serial.print("-- Couleur : "); Serial.println(couleurNum);
   Serial.print(couleurRuban[couleurNum][0]); Serial.print(" ");
   Serial.print(couleurRuban[couleurNum][1]); Serial.print(" ");
   Serial.print(couleurRuban[couleurNum][2]);
   Serial.println("");

   //// affiche le contenu du tableau des couleurs m�moris�es (couleurRuban)
   //for(int i = 0; i < 3; i++)
   //   for (int j = 0; j < 3; j++)
   //   {
   //      Serial.print(i); Serial.print(" "); Serial.print(j); Serial.print(" : ");
   //      Serial.println(couleurRuban[i][j]);
   //   }
}