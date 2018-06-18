/*------------------------------------------------------------------------------------------------
Programme : zbReception.ino      Version : 1.0           Version arduino : 1.6.12
Auteur : H. Dugast               Date : 06-04-2017

Matériel utilisé : Arduino Mega 2560, carte Mega shield grove, modules grove Bee socket
Connexions réalisées sur carte Mega : XBee -> UART1 megashield

Fonctionnement du programme :
Affiche les données réceptionnées par le module xbee connecté à la carte arduino dans un
terminal (115200 bauds)

Test de ce programme :
•  Utiliser le programme python xbeeTestEmission.py
https://github.com/HerveDugast/public_btssn_lasalle_nantes/tree/master/python/_prog_HD/zigbee
ou
•  Utiliser le PC et connecter un module xbee sur le port USB à l'aide d'un adaptateur USB-xbee
Paramétrer le module XBee XB24-ZB "arduino" avec XCTU (exemple):
   Name : coord1998_API    Product family : XB24-ZB
   Firmware : Zigbee Coordinateur API version 21A7
   PAN ID : 1998        SH : 0013A200        BD : 115200
   SC : FFFF            SL : 40E96396        NB : No Parity
   NI : coord1998_API   DH : 0013A200        SB : One stop bit
   CH : 1A              DL : 40D967BC        AP : 2
Utiliser XCTU avec l'outil "Frames generator" et créer une trame API avec
   Protocol : ZigBee    Frame type : 0x10 - Transmit Request   Frame ID : 01
   64-bit dest. address : 00 13 A2 00 40 D9 67 BC
   16-bit dest. address : FF FE     Broadcast radius : 00      Options : 00
   RF Data (ASCII) : Hello routeur
   Trame générée avec ces paramètres :
   7E 00 1B 10 01 00 7D 33 A2 00 40 D9 67 BC FF FE 00 00 48 65 6C 6C 6F 20 72 6F 75 74 65 75 72 D6

Dans le moniteur de XCTU "PC", envoyer la trame API créée
Voici ce qui devrait s'afficher dans le moniteur arduino avec cet exemple
********** Variables programme principal *****************************
payload (hexa) : 48 65 6C 6C 6F 20 72 6F 75 74 65 75 72
payload (decimal) : 72 101 108 108 111 32 114 111 117 116 101 117 114
payload (ascii) : Hello routeur
********** Fin variables programme principal *************************

--- Trame reponse ZBRxResponse (0x90) en hexa ------------------------
7E 0 19 90 0 13 A2 0 40 E9 63 96 0 0 1 48 65 6C 6C 6F 20 72 6F 75 74 65 75 72 6D
Start delimiter : 7E
Length : 0 19
Frame type : 90   (Receive Packet = 0x90)
64-bit dest address : 0 13 A2 0 40 E9 63 96
16-bit dest address : 0 0
Receive options : 1
RF Data : 48 65 6C 6C 6F 20 72 6F 75 74 65 75 72
Ckecksum : 6D
--- FIN trame reponse ZBRxResponse -----------------------------------

***** Configuration Module XBee XB24-ZB "arduino" avec XCTU (exemple) **********
Name : rout1998_API
Product family : XB24-ZB
Firmware : Zigbee Router API version 23A7
PAN ID : 1998        SH : 0013A200        BD : 115200
SC : FFFF            SL : 40D967BC        NB : No Parity
OI : 4E2D            MY : -               SB : One stop bit
CH : 0C              DH : 00000000        AP : 2
JV : 01              DL : 00000000        D7 : Disable
JN : 01              NI : rout1998_API    D6 : disable
---------------------------------------------------------------------------------------------- */
#include <PString.h>
#include <Xbee.h>
#include <Printers.h>
#include <XbeeGestion.h>

const int DUREE_DEBUG_EN_MS = 2000;

// ------------- objets XBee et variables liées au protocole ZigBee -------------------------------
const int DUREE_MAX_SANS_RECEPTION = 3000;
const uint8_t NB_DATA_MAX = 100; // nombre max de données utiles à réceptionner

uint8_t payload[NB_DATA_MAX];  // octets de données
uint8_t nbData = NB_DATA_MAX;   // nombre de données réceptionnées
// Définit le port série à utiliser et sa vitesse de transmission en bauds
// • si carte Arduino UNO, seul le port 0 existe -> Serial(...)
//     ATTENTION, il faut déconnecter le module Xbee pour programmer
//        En effet, le port 0 est utilisé pour la programmation et la communication UNO-XBee
// • si arduino MEGA, on peut utiliser le port 1 -> Serial1(...)
//     Pas besoin de déconnecter Xbee pour programmer, car celle-ci utilise le port 0
#define PORT_SERIE_NUM  1
#define VITESSE_PORT    115200
#define PIN_LED_SEND    10
#define PIN_LED_RECEIVE 12
#define PIN_LED_ERROR   14

                                // Adresse 64 bits xbeeR1 à joindre,  XBeeAddress64(SH XBee destinataire, SL XBee destinataire)
XBeeAddress64 adrXbeeC = XBeeAddress64(0, 0);  // SH coordi = SL coordi = 0
                                               // *** Objet permettant de communiquer avec la radio du module XBee
XbeeGestion xbeeR1 = XbeeGestion(adrXbeeC, payload, sizeof(payload), PORT_SERIE_NUM, VITESSE_PORT,
   PIN_LED_SEND, PIN_LED_RECEIVE, PIN_LED_ERROR);

// ------------------------------------------------------------------------------------------------
// PROGRAMME PRINCIPAL
// ------------------------------------------------------------------------------------------------
void setup()
{
   Serial.begin(115200);  //  debug pour affichage dans un terminal (moniteur)
   Serial.println("Demarrage puis initialisation module XBee... Patientez quelques secondes");
   delay(2000);
   Serial.println("Initialisation terminee");
}

void loop()
{
   xbeeR1.recevoirAvecZBRxResponseEtEnvoyerAR(); // récupère trame pour commander clignotement LED
   if (xbeeR1.m_rx.isAvailable())
   {
      // une trame est réceptionnée
      xbee_lire_payload(); // lit et traite les données transmises dans la trame reçue
      afficherVariableProgramme();
      debugImmediat();
      xbeeR1.m_rx.init();  // efface le drapeau isAvailable
   }

   // Détection des erreurs de réception dans la liaison xbee
   xbeeR1.signalerProblemeReceptionPaquet(DUREE_MAX_SANS_RECEPTION);
}

//-------------------------------------------------------------------------------------------------
// Lit et mémorise les données utiles (payload) de la trame reçue 
//-------------------------------------------------------------------------------------------------
void xbee_lire_payload()
{
   nbData = xbeeR1.m_rx.getDataLength();
   if (nbData > NB_DATA_MAX)
      nbData = NB_DATA_MAX;
   for (int i = 0; i < nbData; i++)
      payload[i] = xbeeR1.m_rx.getData(i);
}

//-------------------------------------------------------------------------------------------------
// DEBUG : Affiche les valeurs des variables dans un terminal
//-------------------------------------------------------------------------------------------------
void afficherVariableProgramme()
{
   Serial.println("");
   Serial.println("********** Variables programme principal *****************************");
   Serial.print("payload (hexa) : ");
   for (int i = 0; i < nbData; i++)
   {
      Serial.print(payload[i], HEX); Serial.print(" ");
   }
   Serial.println("");
   Serial.print("payload (decimal) : ");
   for (int i = 0; i < nbData; i++)
   {
      Serial.print(payload[i]); Serial.print(" ");
   }
   Serial.println("");
   Serial.print("payload (ascii) : ");
   for (int i = 0; i < nbData; i++)
   {
      if (payload[i] >= 32 && payload[i] < 127)
         Serial.write(payload[i]);
      else
         Serial.print('?');
      Serial.print(' ');
   }
   Serial.println("");
   Serial.println("********** Fin variables programme principal *************************");
   Serial.println("");
}

//-------------------------------------------------------------------------------------------------
// DEBUG IMMEDIAT : appelle un programme pour afficher dans le terminal toutes les nb baseTemps
//-------------------------------------------------------------------------------------------------
void debugImmediat()
{
   //afficherVariableProgramme();
   //xbeeR1.afficherTrameZBRxResponse();
   //xbeeR1.afficherVariableMembre();
   //xbeeR1.afficherInfoXbee();
}
