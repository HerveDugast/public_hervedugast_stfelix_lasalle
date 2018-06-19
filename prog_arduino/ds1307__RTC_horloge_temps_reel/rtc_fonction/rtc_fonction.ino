/*-------------------------------------------------------------------------------------------------
Programme : rtc_fonction.ino      Version : 1.1           Version arduino : 1.6.12
Auteur : http://wiki.seeed.cc/Grove-RTC/   (modifié Hervé Dugast)
Date : 13-12-2016

Matériel utilisé : Arduino Mega 2560, carte Mega shield grove, module grove RTC v1.1 (DS1307)
Connexions : module RTC -> 1 des connecteurs i2c de la carte mega shield

Fonctionnement du programme :
Initialise la date et l'heure puis l'affiche au format anglais dans un moniteur série.

Remarque : le programme est décomposé en fonctions
---------------------------------------------------------------------------------------------- */
#include <Wire.h>
#include "DS1307.h"

DS1307 clock;//define a object of DS1307 class
void setup()
{
	Serial.begin(9600);
	clock.begin();
	//rtc_configurer_date_heure();
}
void loop()
{
	clock.getTime();
	rtc_printTime();
}

/*Function: Display time on the serial monitor*/
void rtc_printTime()
{
    Serial.print(clock.hour, DEC);
    Serial.print(":");
    Serial.print(clock.minute, DEC);
    Serial.print(":");
    Serial.print(clock.second, DEC);
    Serial.print("	");
    Serial.print(clock.month, DEC);
    Serial.print("/");
    Serial.print(clock.dayOfMonth, DEC);
    Serial.print("/");
    Serial.print(clock.year + 2000, DEC);
    Serial.print(" ");
    Serial.print(clock.dayOfMonth);
    Serial.print("*");
    switch (clock.dayOfWeek)		// Friendly printout the weekday
    {
    case MON:
        Serial.print("MON");
        break;
    case TUE:
        Serial.print("TUE");
        break;
    case WED:
        Serial.print("WED");
        break;
    case THU:
        Serial.print("THU");
        break;
    case FRI:
        Serial.print("FRI");
        break;
    case SAT:
        Serial.print("SAT");
        break;
    case SUN:
        Serial.print("SUN");
        break;
    }
    Serial.println(" ");
}

/* Function: initialise la date et l'heure aux valeurs indiquées */
void rtc_configurer_date_heure()
{
    clock.fillByYMD(2016, 12, 14);	// Year, Month, Date
    clock.fillByHMS(11, 34, 00);		// HH, MM, SS
    clock.fillDayOfWeek(TUE);		// MON, TUE, WED, THU, FRI, SAT, SUN
    clock.setTime();				// write time to the RTC chip
}