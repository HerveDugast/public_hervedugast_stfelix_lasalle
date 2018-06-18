/*-------------------------------------------------------------------------------------------------
Programme : test_mesureIbat.ino       Version : 1.0           Version arduino : 1.6.12
Auteur : H. Dugast                    Date : 22-03-2017

Mat�riel utilis� : Arduino Mega 2560, carte interfaceCapteur
Connexions r�alis�es : carte interfaceCapteur connect�e sur la M�ga 2560

Fonctionnement du programme :
Mesure le courant continu (Ibat) circulant dans le conducteur qui traverse le capteur LEM. 
Pr�cision +/- 100mA. Attention au sens de circulation du courant. 
Une fl�che sue le capteur LEM indique le sens de mesure pour un courant positif.
Plage de mesure du courant : 0 - 25A

|  Ibat  |  Ibch  |  Ibca  | iBatCodeCan | iBatCodeCan | iBatCalcul | iBatCalcul | 
| mesur� | mesur� | mesur� |  th�orique  |  mesur�     |  th�orique |  calcul�   |
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

// ------------- param�tres base de temps ---------------------------------------------------------
const int DUREE_DEBUG_EN_MS = 1000;

const uint8_t PIN_IBAT = 6; // entr�e CAN mesure Ibat
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
   // La structure �lectronique (montage � AOP) am�ne une petite erreur d'offset malgr� le r�glage
   // pour bien afficher 0A quand Ibat = 0, on consid�re que Ibat = 0 si codeCanIbat < 9 (100 mA)
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
   unsigned long millisNow;   // contient nb de millisecondes �coul�es � cet instant
   static int count = 0;

   millisNow = millis(); // m�morise l'instant pr�sent pour laisser le temps � la r�ponse d'arriver
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
