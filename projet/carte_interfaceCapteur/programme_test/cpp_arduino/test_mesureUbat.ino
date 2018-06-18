/*-------------------------------------------------------------------------------------------------
Programme : test_mesureUbat.ino     Version : 1.0           Version arduino : 1.6.12
Auteur : H. Dugast                  Date : 22-03-2017

Mat�riel utilis� : Arduino Mega 2560, carte interfaceCapteur
Connexions r�alis�es : carte interfaceCapteur connect�e sur la M�ga 2560 

Fonctionnement du programme :
Mesure la tension batterie (Ubat), retourne la valeur de la tension batterie en dV (entier)
| Ubat (V) | Ubc (V) | code CAN th�or | code CAN mesur | UbatCalcul (dV) |
|          |         |                |sans correctif  |                 |
|    10,0  |  2,50   |     512        |      510       |      100        |
|    12,0  |  3,00   |     614        |      611       |      120        |
|    14,0  |  3,50   |     717        |      712       |      140        |
------------------------------------------------------------------------------------------------ */

// ------------- param�tres base de temps ---------------------------------------------------------
const int DUREE_DEBUG_EN_MS = 1000; 

const uint8_t PIN_UBAT = 4;           // entr�e CAN mesure Ubat
const uint16_t CODE_CAN_UBAT_CORRECTIF = 5; // correctif code apr�s mesure (plage test 9V - 15V)
uint16_t uBatCalcul;                   // tension batterie en dV (entier)
uint16_t codeCan;

// ------------------------------------------------------------------------------------------------
// PROGRAMME PRINCIPAL
// ------------------------------------------------------------------------------------------------
void setup()
{
   Serial.begin(115200);  //  debug
}

void loop()
{
   codeCan = analogRead(PIN_UBAT);  // convertir la tension batterie en code
   uBatCalcul = (codeCan + CODE_CAN_UBAT_CORRECTIF) * 25 / 128;
   debug();
}

//-------------------------------------------------------------------------------------------------
// DEBUG : appelle un programme pour afficher dans le terminal toutes les nb baseTemps
//-------------------------------------------------------------------------------------------------
void debug()
{
   static unsigned long start = millis();
   unsigned long millisNow;   // contient nb de millisecondes �coul�es � cet instant

   millisNow = millis(); // m�morise l'instant pr�sent pour laisser le temps � la r�ponse d'arriver
   if (millisNow - start > DUREE_DEBUG_EN_MS)
   {
      start = millisNow;

      Serial.print("Ubat code = ");
      Serial.println(codeCan);
      Serial.print("Ubat calcul (dV) = ");
      Serial.println(uBatCalcul);
      Serial.print("");

      //uBat.afficherVariableMembre();
   }
}

//-------------------------------------------------------------------------------------------------
// DEBUG IMMEDIAT : appelle un programme pour afficher dans le terminal toutes les nb baseTemps
//-------------------------------------------------------------------------------------------------
void debugImmediat()
{
   
}
