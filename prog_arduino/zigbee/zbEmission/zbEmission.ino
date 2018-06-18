/*------------------------------------------------------------------------------------------------
Programme : zbEmission.ino      Version : 1.0           Version arduino : 1.6.12
Auteur : H. Dugast               Date : 24-04-2017

Matériel utilisé : Arduino Mega 2560, carte Mega shield grove, modules grove Bee socket
Connexions réalisées sur carte Mega : XBee -> UART1 megashield

Fonctionnement du programme :
Envoie des données, chaine de caractères ou octets, vers un ordinateur, par une
liaison zigbee. Les modules XBee utilisés sont des séries 2, fonctionnant en API mode 2.
Le module xbee connecté au PC est configuré en routeur API.
https://github.com/HerveDugast/public_btssn_lasalle_nantes/tree/master/arduino/_prog_HD/zigbee

Pour tester ce programme, on peut utiliser le programme xbeeTestReceptionPlus.py sur un PC sur lequel
est connecté un module XBee configuré en routeur API.
https://github.com/HerveDugast/public_btssn_lasalle_nantes/tree/master/python/_prog_HD/zigbee

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

// ------------- paramètres base de temps ---------------------------------------------------------
#define BASE_TEMPS   2000            // base de temps
const int DUREE_DEBUG_EN_MS = 2000;

// ------------- objets XBee et variables liées au protocole ZigBee -------------------------------
const int DUREE_MAX_SANS_RECEPTION = 3000;
const uint8_t NB_DATA_MAX = 100; // nombre max de données utiles à réceptionner
uint8_t nbDataPayload;  // nombre d'octets à transmettre (nb octets réel du payload)

const uint8_t NB_DATAHEX = 5;
uint8_t dataHex[NB_DATAHEX] = { 0x10, 0x00, 0xFE, 0x13, 0x4A };
const uint8_t NB_DATATXT = 6;
char dataTxt[NB_DATATXT] = "Hello";

uint8_t payload[NB_DATA_MAX];  // octets de données
uint8_t nbData = NB_DATA_MAX;   // nombre de données envoyées
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
XBeeAddress64 adrXbeeR1 = XBeeAddress64(0x0013A200, 0x40D967BC);
// *** Objet permettant de communiquer avec la radio du module XBee
XbeeGestion xbeeC = XbeeGestion(adrXbeeR1, payload, sizeof(payload), PORT_SERIE_NUM, VITESSE_PORT,
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
   static uint16_t numeroTrame = 0;   // pour compter le nombre d'envoi
   static unsigned long millisPrec = millis();// mémorise nb de millisecondes écoulées à un instant
   unsigned long millisNow;   // contient nb de millisecondes écoulées à cet instant

   millisNow = millis(); // lit nb de millisecondes écoulées à cet instant

   if (millisNow - millisPrec >= BASE_TEMPS)
   {
      // entre dans cette boucle tous les multiples de BASE_TEMPS (en ms)
      // exemple : avec BASE_TEMPS = 20 ms, on entre dans dans cette boucle toutes les 20 ms
      numeroTrame++;  // numérote la trame à envoyer sur 16 bits
      millisPrec = millisNow; // mémorise nb de millisecondes écoulées à un instant
      xbeePreparerPayload(numeroTrame); // prépare le message utile à transmettre par liaison xbee
      // Envoie trame commande LED vers carte zbLedRouteur, signale erreur
      xbeeC.envoyerZBTxRequestEtReceptionnerAR();
      afficherVariableProgramme();
   }
}

//-------------------------------------------------------------------------------------------------
// Prépare le message utile à envoyer (payload)
// Dans notre exemple, payload : concaténation du numéro de trame, d'une suite d'octets et 
// d'un message texte
//   Exemple avec numéro trame = 1500, dataHexStr = "0x1000FE134A" et dataTxtStr = "Hello" 
//   Payload envoyé(hexa) : 0f 27 1b 10 00 fe 13 4a 48 65 6c 6c 6f
//   Payload envoyé(dec) : 15 39 27 16 0 254 19 74 72 101 108 108 111
//   Payload envoyé(ascii) :  '   \000 ?  J H e l l o
//-------------------------------------------------------------------------------------------------
void xbeePreparerPayload(uint16_t numeroTrame)
{
   uint8_t i, j;
   payload[0] = (uint8_t)(numeroTrame >> 8);
   payload[1] = (uint8_t)(numeroTrame & 0x00FF);
   for(i = 0; i < NB_DATAHEX; i++)
      payload[2 + i] = dataHex[i];
   for (j = 0; j < NB_DATATXT; j++)
      payload[2 + i + j] = dataTxt[j];
   nbDataPayload = 1 + i + j;
}

//-------------------------------------------------------------------------------------------------
// DEBUG : Affiche les valeurs des variables dans un terminal
//-------------------------------------------------------------------------------------------------
void afficherVariableProgramme()
{
   Serial.println("");
   Serial.println("********** Variables programme principal *****************************");
   Serial.print("payload envoye (hexa) : ");
   for (int i = 0; i < nbDataPayload; i++)
   {
      Serial.print(payload[i], HEX); Serial.print(" ");
   }
   Serial.println("");
   Serial.print("payload envoye (decimal) : ");
   for (int i = 0; i < nbDataPayload; i++)
   {
      Serial.print(payload[i]); Serial.print(" ");
   }
   Serial.println("");
   Serial.print("payload envoye (ascii) : ");
   for (int i = 0; i < nbDataPayload; i++)
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
