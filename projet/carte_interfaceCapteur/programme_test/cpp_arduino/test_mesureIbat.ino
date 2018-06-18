/*-------------------------------------------------------------------------------------------------
Programme : test_mesureIbat.ino       Version : 1.0           Version arduino : 1.6.12
Auteur : H. Dugast                    Date : 22-03-2017

Matériel utilisé : Arduino Mega 2560, carte interfaceCapteur
Connexions réalisées : carte interfaceCapteur connectée sur la Méga 2560

Fonctionnement du programme :
Mesure le courant continu (Ibat) circulant dans le conducteur qui traverse le capteur LEM. 
Précision +/- 100mA. Attention au sens de circulation du courant. 
Une flèche sue le capteur LEM indique le sens de mesure pour un courant positif.
Plage de mesure du courant : 0 - 25A

|  Ibat  |  Ibch  |  Ibca  | iBatCodeCan | iBatCodeCan | iBatCalcul | iBatCalcul | 
| mesuré | mesuré | mesuré |  théorique  |  mesuré     |  théorique |  calculé   |
|   A    |    V   |    V   |             |             |     dA     |    dA      |
|   0    | 5,978  | 0,0351 |        0    |        0    |      0     |     0      |
|   0,1  | 5,990  | 0,0614 |        4    |        9    |      1     |     2      |
|   1    | 6,084  | 0,2400 |       41    |       46    |     10     |    11      |
|   3    | 6,293  | 0,6371 |      123    |      127    |     30     |    31      |
|   5    | 6,501  | 1,0345 |      205    |      208    |     50     |    50      |
|  10    | 7,019  | 2,0290 |      410    |      412    |    100     |   100      |
|  15    | 7,540  | 3.0245 |      614    |      615    |    150     |   150      |
|  20    | 8,059  | 4,.021 |      819    |      819    |    200     |   199      |
------------------------------------------------------------------------------------------------ */

// ------------- paramètres base de temps ---------------------------------------------------------
const int DUREE_DEBUG_EN_MS = 1000;

const uint8_t PIN_IBAT = 6; // entrée CAN mesure Ibat
uint32_t iBatCodeCan;       // code correspondant courant batterie
uint32_t iBatCalcul;        // courant batterie en dA

// ------------------------------------------------------------------------------------------------
// PROGRAMME PRINCIPAL
// ------------------------------------------------------------------------------------------------
void setup()
{
   Serial.begin(115200);  //  debug
}

void loop()
{
   iBatCodeCan = analogRead(PIN_IBAT);  // convertir le courant batterie en code
   // La structure électronique (montage à AOP) amène une petite erreur d'offset malgré le réglage
   // pour bien afficher 0A quand Ibat = 0, on considère que Ibat = 0 si codeCanIbat < 9 (100 mA)
   if (iBatCodeCan >= 9)
      iBatCalcul = (iBatCodeCan * uint32_t(125)) / 512;
   else
      iBatCalcul = 0;
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
      Serial.print("Ibat code = ");
      Serial.println(iBatCodeCan);
      Serial.print("Ibat calcul (dA) = ");
      Serial.println(iBatCalcul);
      Serial.println("----------------------------");
   }
}

//-------------------------------------------------------------------------------------------------
// DEBUG IMMEDIAT : appelle un programme pour afficher dans le terminal toutes les nb baseTemps
//-------------------------------------------------------------------------------------------------
void debugImmediat()
{

}
