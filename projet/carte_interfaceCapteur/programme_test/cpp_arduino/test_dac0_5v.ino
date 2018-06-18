/*-------------------------------------------------------------------------------------------------
Programme : test_dac0_5v.ino         Version : 1.0           Version arduino : 1.6.12
Auteur : H. Dugast                   Date : 22-03-2017

Matériel utilisé : Arduino Mega 2560, carte interfaceCapteur
Connexions réalisées : carte interfaceCapteur connectée sur la Méga 2560

Fonctionnement du programme :
- Génère en sortie une tension continue analogique comprise entre 0 et 5V
proportionnelle à la valeur de la pwm d'entrée
- Génère un signal pwm sur l'autre sortie

Mesures ci-dessous effectuée avec Fpwm = 3,92KHz soit Tpwm = 255µs
| valPwm0	 |    pwm     | vs10f  |
| 0 - 255 |  théorique | mesuré |
|         |     %      |   V    |
|     0   |	    0      |   0,01 |
|    63   |    25      |   1,25 |
|   127   |    50      |   2,50 |
|   190   |    75      |   3,74 |
|   255   |   100      |   5,00 |
------------------------------------------------------------------------------------------------ */

// ------------- paramètres base de temps ---------------------------------------------------------
const int DUREE_DEBUG_EN_MS = 1000;

const uint8_t PIN_VE_DAC5 = 6;   // broche signal pwm0 pour générer tension analogique sortie 0-5V
// La connexion VePwm1-D7 n'a pas été routé avec protéus...   v1.2 : OK
const uint8_t PIN_VE_PWM1 = 7;   // broche signal pwm1 pour générer signal PWM sortie 0-5V
uint8_t valPwm0 = 127;             // valeur pwm : 0 à 255  correspondant 0 à 100%
uint8_t valPwm1 = 190;             // valeur pwm : 0 à 255  correspondant 0 à 100%

// ------------------------------------------------------------------------------------------------
// PROGRAMME PRINCIPAL
// ------------------------------------------------------------------------------------------------
void setup()
{
   // set timer 4 divisor to 1 for PWM frequency of 31372.55 Hz
   //TCCR4B = TCCR4B & B11111000 | B00000001; 
   // set timer 4 divisor to 8 for PWM frequency of 3921.16 Hz
   TCCR4B = TCCR4B & B11111000 | B00000010; 
   // set timer 4 divisor to 64 for PWM frequency of 490.20 Hz
   //TCCR4B = TCCR4B & B11111000 | B00000011; 
   analogWrite(PIN_VE_DAC5, valPwm0);
   analogWrite(PIN_VE_PWM1, valPwm1);

   Serial.begin(115200);  //  debug
}

void loop()
{
   //debug();
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
      Serial.print("valPwm0 = ");
      Serial.println(valPwm0);
      Serial.println("----------------------------");
   }
}

//-------------------------------------------------------------------------------------------------
// DEBUG IMMEDIAT : appelle un programme pour afficher dans le terminal toutes les nb baseTemps
//-------------------------------------------------------------------------------------------------
void debugImmediat()
{

}
