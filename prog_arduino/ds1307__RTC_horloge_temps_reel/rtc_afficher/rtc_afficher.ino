/*-------------------------------------------------------------------------------------------------
Programme : rtc_afficher.ino      Version : 1.0           Version arduino : 1.6.12
Auteur : http://wiki.seeed.cc/Grove-RTC/   (modifié Hervé Dugast)
Date : 29-11-2016

Matériel utilisé : Arduino Mega 2560, carte Mega shield grove, module grove RTC v1.1 (DS1307)
Connexions : module RTC -> 1 des connecteurs i2c de la carte mega shield

Fonctionnement du programme :
Initialise la date et l'heure puis l'affiche au format français dans un moniteur série
---------------------------------------------------------------------------------------------- */
#include <Wire.h>
#include "DS1307.h"

#define JOUR_SEMAINE_NOM        TUE     // à choisir parmi MON, TUE, WED, THU, FRI, SAT, SUN
#define JOUR_SEMAINE_NOMBRE     29      // jour de la semaine en nombre 
#define MOIS                    11
#define ANNEE                   2016
#define HEURE                   19
#define MINUTE                  8
#define SECONDE                 45

DS1307 clock;//define a object of DS1307 class
void setup()
{
    Serial.begin(9600);
    clock.begin();      // démarre l'horloge temps réel
    //rtc_initialiser(); // mise à l'heure
    delay(500);
}

void loop()
{
    static uint8_t secondePrec = 0;
    clock.getTime();
    if (clock.second != secondePrec)
    {
        rtc_afficher_heure();
        secondePrec = clock.second; // mémorise le nb de secondes courant
    }
    delay(100);
}

/*Function: Display time on the serial monitor*/
void rtc_afficher_heure()
{
    char date[8];  // chaîne de caractères contenant la date (jour/mois/année)
    char heure[8]; // chaîne de caractères contenant l'heure (heures:minutes:secondes)

    switch (clock.dayOfWeek)  // affiche le nom du jour de la semaine
    {
    case MON:
        Serial.print("Lundi");
        break;
    case TUE:
        Serial.print("Mardi ");
        break;
    case WED:
        Serial.print("Mercredi ");
        break;
    case THU:
        Serial.print("Jeudi ");
        break;
    case FRI:
        Serial.print("Vendredi ");
        break;
    case SAT:
        Serial.print("Samedi ");
        break;
    case SUN:
        Serial.print("Dimanche ");
        break;
    }
    // Mise en forme de la date, jour et mois sur 2 chiffres
    sprintf(date, "%02d/%02d/%i ", clock.dayOfMonth, clock.month, clock.year + 2000);
    Serial.print(date);
    // Mise en forme de l'heure, heures, minutes et secondes sur 2 chiffres
    sprintf(heure, "%02d:%02d:%02d", clock.hour, clock.minute, clock.second);
    Serial.print(heure);
    Serial.println(" ");
}

/* Function: initialise la date et l'heure aux valeurs indiquées */
void rtc_initialiser()
{
    clock.fillByYMD(ANNEE, MOIS, JOUR_SEMAINE_NOMBRE);
    clock.fillByHMS(HEURE, MINUTE, SECONDE);
    clock.fillDayOfWeek(JOUR_SEMAINE_NOM);
    clock.setTime();    // écrit la date et l'heure dans la puce DS1307
}