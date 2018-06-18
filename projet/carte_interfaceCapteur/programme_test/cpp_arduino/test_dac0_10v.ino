/*-------------------------------------------------------------------------------------------------
Programme : test_dac0_10v.ino         Version : 1.0           Version arduino : 1.6.12
Auteur : H. Dugast                    Date : 22-03-2017

Matériel utilisé : Arduino Mega 2560, carte interfaceCapteur
Connexions réalisées : carte interfaceCapteur connectée sur la Méga 2560

Fonctionnement du programme :
Génère en sortie une tension continue analogique comprise entre 0 et 10V
proportionnelle à la valeur de la pwm d'entrée
La tension de sortie de l'amplificateur opérationnel de la fonction DAC 0-10V
sature à 9,8V. C'est normal avec la gamme de composant utilisé.

Mesures ci-dessous effectuée avec Fpwm = 31,37KHz soit Tpwm = 31,88µs
| valPwm	 |   T    |	 Thaut |   pwm     |  pwm   |   vs10f   | vs10f  |
| 0 - 255 | mesuré | mesuré | théorique | mesuré | théorique | mesuré |
|         |   µs   |   µs   |    %      |   %    |    V      |    V   |
|     0   |	  0    |   0    |	     0    |    0   |    0,000  |  0,000 |
|     4   |  31,88 |   0,5  |      2    |    2   |    0,157  |  0,112 | 
|     5   |  31,88 |   0,62 |      2    |    2   |    0,196  |  0,151 |
|    10   |  31,88 |   1,24 |      4    |    4   |    0,392  |  0,350 |
|    63   |  31,88 |   7,87 |     25    |   25   |    2,471  |  2,456 |
|    64   |  31,88 |   8,00 |     25    |   25   |    2,510  |  2,497 |
|   127   |  31,88 |  15,88 |     50    |   50   |    4,98   |  5,00  |
|   190   |  31,88 |  23,76 |     75    |   75   |    7,45   |  7,50  |
|   249   |  31,88 |  31,15 |     98    |   98   |    9,76   |  9,83  |
|   250   |  31,88 |  31,26 |     98    |   98   |    9,80   |  9,84  |
|   255   |  31,88 |  31,88 |	   100    |  100   |   10,00   |  9,84  |
------------------------------------------------------------------------------------------------ */

// ------------- paramètres base de temps ---------------------------------------------------------
const int DUREE_DEBUG_EN_MS = 1000;

const uint8_t PIN_VE_DAC10 = 12;  // broche signal PWM pour générer tension analogique sortie 0-10V
uint8_t valPwm = 127;             // valeur pwm : 0 à 255  correspondant 0 à 100%

// ------------------------------------------------------------------------------------------------
// PROGRAMME PRINCIPAL
// ------------------------------------------------------------------------------------------------
void setup()
{
   // set timer 1 divisor to 64 for PWM frequency of 490.20 Hz
   //TCCR1B = TCCR1B & B11111000 | B00000011; 
   // set timer 1 divisor to 8 for PWM frequency of 3921.16 Hz
   //TCCR1B = TCCR1B & B11111000 | B00000010; // set timer 1 divisor to 8 for PWM frequency of 3921.16 Hz

   // set timer 1 divisor to 1 for PWM frequency of 31372.55 Hz
   TCCR1B = TCCR1B & B11111000 | B00000001; 
   analogWrite(PIN_VE_DAC10, valPwm);

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
      Serial.print("valPwm = ");
      Serial.println(valPwm);
      Serial.println("----------------------------");
   }
}

//-------------------------------------------------------------------------------------------------
// DEBUG IMMEDIAT : appelle un programme pour afficher dans le terminal toutes les nb baseTemps
//-------------------------------------------------------------------------------------------------
void debugImmediat()
{

}
