/*-------------------------------------------------------------------------------------------------
Programme : test_mesureUshunt.ino     Version : 1.0           Version arduino : 1.6.12
Auteur : H. Dugast                    Date : 22-03-2017

Matériel utilisé : Arduino Mega 2560, carte interfaceCapteur
Connexions réalisées : carte interfaceCapteur connectée sur la Méga 2560

Fonctionnement du programme :
Mesure la consommation de la carte interfaceCapteur et des cartes/capteurs qui y sont connectés
principe : mesure de la tension aux bornes de la résistance de shunt puis application de la
formul Iconso = Urshunt / Rshunt = (Ubat - UbatSh) / Rshunt   avec Rshunt = 0,25 ohm

| Ubat | U Rshunt | UbatCode | UbatShCode | UbatCalcul | UbatShCalcul |Iconso |  Iconso  |Pconso|
|mesuré| mesuré   | mesuré   |  mesuré    | calculé    |  calculé     |théoriq|  mesuré  |mesuré|
|   V  |    mV    |          |            |    mV      |    mV        |   mA  |    mA    |  dW  |
| 12,0 |   16     |    612   |    608     |   12050    |    11972     |   64  |  102/135 | 12/15|
| 12,0 |   50     |    612   |    605     |   12050    |    11914     |  200  |  203/236 | 24/27|
| 12,0 |   123,5  |    612   |    598     |   12050    |    11777     |  494  |  441/474 | 52/56|
------------------------------------------------------------------------------------------------ */

// ------------- paramètres base de temps ---------------------------------------------------------
const int DUREE_DEBUG_EN_MS = 1000;

const uint8_t PIN_UBAT = 4;                  // entrée CAN mesure Ubat avant Rshunt
const uint8_t PIN_UBATSH = 5;                // entrée CAN mesure Ubat après Rshunt
const uint32_t CODE_CAN_UBAT_CORRECTIF = 5;  // correctif code CAN (plage test Ubat : 9V - 15V)
const uint32_t COEFF_ISHUNT_CORRECTIF = 23;  // correctif mesure courant (plage test Ubat : 9V - 15V)
uint32_t uBatCodeCan;      // code correspondant à la tension batterie (entrée Rshunt)
uint32_t uBatShCodeCan;    // code correspondant à la tension en sortie de Rshunt
uint32_t uBatCalcul;       // tension batterie
uint32_t uBatShCalcul;     // tension à la sortie de Rshunt
uint16_t iConso;           // courant consommé (courant traversant le shunt)
uint16_t puissConso;       // courant consommé (courant traversant le shunt)

// ------------------------------------------------------------------------------------------------
// PROGRAMME PRINCIPAL
// ------------------------------------------------------------------------------------------------
void setup()
{
   Serial.begin(115200);  //  debug
}

void loop()
{
   uBatCodeCan = analogRead(PIN_UBAT);  // convertir la tension batterie en code
   uBatCalcul = ((uBatCodeCan + CODE_CAN_UBAT_CORRECTIF) * uint32_t(625)) / 32;
   uBatShCodeCan = analogRead(PIN_UBATSH);  // convertir la tension batterie en code
   uBatShCalcul = ((uBatShCodeCan + CODE_CAN_UBAT_CORRECTIF) * uint32_t(625)) / 32;
   // en théorie uBatCodeCan est toujours supérieur ou égal à uBatShCodeCan
   // mais la mesure des 2 entrées ne sont pas effectuées au même instant
   // donc il faut contrôler cette inégalité pour ne pas obtenir de résultat incohérent
   if (uBatCodeCan >= uBatShCodeCan)
      iConso = uint16_t(((uBatCalcul - uBatShCalcul) * 40 / COEFF_ISHUNT_CORRECTIF));
   // puissConso en dW, uBat en dV et iConso en cA
   else
      iConso = 0;
   puissConso = (uint16_t(uBatCalcul / 100) * uint16_t(iConso / 10)) / 100;
   //Serial.println(puissConso);
   debug();
}

//-------------------------------------------------------------------------------------------------
// DEBUG : appelle un programme pour afficher dans le terminal toutes les nb baseTemps
//-------------------------------------------------------------------------------------------------
void debug()
{
   static unsigned long start = millis();
   unsigned long millisNow;   // contient nb de millisecondes écoulées à cet instant
   static int count = 0;

   millisNow = millis(); // mémorise l'instant présent pour laisser le temps à la réponse d'arriver
   if (millisNow - start > DUREE_DEBUG_EN_MS)
   {
      start = millisNow;
      count++;
      Serial.println(count);
      Serial.print("Ubat code = ");
      Serial.println(uBatCodeCan);
      Serial.print("Ubat calcul (mV) = ");
      Serial.println(uBatCalcul);
      Serial.print("UbatSh code = ");
      Serial.println(uBatShCodeCan);
      Serial.print("UbatSh calcul (mV) = ");
      Serial.println(uBatShCalcul);
      Serial.print("");
      Serial.print("Courant consomme (mA) : ");
      Serial.println(iConso);
      Serial.print("Puissance consommee (dW) : ");
      Serial.println(puissConso, DEC);
      Serial.println("----------------------------");
   }
}

//-------------------------------------------------------------------------------------------------
// DEBUG IMMEDIAT : appelle un programme pour afficher dans le terminal toutes les nb baseTemps
//-------------------------------------------------------------------------------------------------
void debugImmediat()
{

}
