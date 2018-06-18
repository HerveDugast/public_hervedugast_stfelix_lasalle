/*-------------------------------------------------------------------------------------------------
Programme : test_signalLed.ino        Version : 1.0           Version arduino : 1.6.12
Auteur : H. Dugast                    Date : 22-03-2017

Matériel utilisé : Arduino Mega 2560, carte interfaceCapteur
Connexions réalisées : carte interfaceCapteur connectée sur la Méga 2560

Fonctionnement du programme :
Fait clignoter la LED rouge L2
------------------------------------------------------------------------------------------------ */

const uint8_t PIN_L2 = 14;  // broche LED L2

void setup() {
   // initialize digital pin PIN_L2 as an output.
   pinMode(PIN_L2, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
   digitalWrite(PIN_L2, HIGH);   // turn the LED on (HIGH is the voltage level)
   delay(1000);                       // wait for a second
   digitalWrite(PIN_L2, LOW);    // turn the LED off by making the voltage LOW
   delay(1000);                       // wait for a second
}