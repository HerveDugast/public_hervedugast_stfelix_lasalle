#!/usr/bin/python3.4
# coding: utf-8

import sys 
sys.path.append("/home/pi/prog/j518-supervisor/BMP280")
sys.path.append("/home/pi/prog/j518-supervisor/Classe_projet")
import time
from datetime import datetime
import threading 
import BMP280
import mysql.connector
from raspiomix import Raspiomix
import ActionneurPy3
import CaptNumPy3
import RPi.GPIO as GPIO
import locale

locale.setlocale(locale.LC_TIME,'')

global CAPTEUR_ID_TEMP_BMP280
global CAPTEUR_ID_PRES_BMP280
CAPTEUR_ID_TEMP_BMP280 = 1
CAPTEUR_ID_PRES_BMP280 = 3
INTERVALLE_MESURE_I2C_TEMPERATURE = 15  # en minutes
INTERVALLE_MESURE_I2C_PRESSION = 60  # en minutes


GPIO.setmode(GPIO.BOARD) # mode de fonctionnement GPIO
GPIO.setup(Raspiomix.IO0, GPIO.OUT) # configure port en sortie

def bddConnect():
    """ Connexion à une base de données MySQL """
    try:
        cnx = mysql.connector.connect(host="10.6.0.1",
                                      user="supervisor",
                                      password="Btssn44",
                                      database="dbsn")

##        cnx = mysql.connector.connect(host="10.16.3.232",
##                                             user="root",
##                                             password="",
##                                             database="dbsn")
##        if cnx.is_connected():
##            print("Connectée à une base de données MySQL")
    except mysql.connector.Error as err:
        print("Error", err)
    finally:
        return cnx

def bddClose(cnx):
    """ Déconnexion de la base de données MySQL """
    cnx.close()
    
def sqlSelectFetchall(sqlQuery):
    """ Exécute et affiche une requête SQL de type SELECT """
    try:
        cnx = bddConnect()
        cur = cnx.cursor()
        cur.execute(sqlQuery)
        #Iterate
        for row in cur.fetchall() :
            print(row)
    except mysql.connector.Error as err:
        print("Error", err) 
    finally:
        # close the cursor
        cur.close()
        bddClose(cnx)

def sqlInsert3Data(sqlQuery, champ1, champ2, champ3):
    """ Exécute une requête SQL de type INSERT, insère 2 données dans la base de données MySQL"""
    args = [champ1, champ2, champ3]
    try:
        cnx = bddConnect()
        cur = cnx.cursor()
        cur.execute(sqlQuery, args)
        if cur.lastrowid:
            print('last insert id', cur.lastrowid)
        else:
            print('ERROR !!! Last insert id not found')
        cnx.commit()
    except mysql.connector.Error as err:
        print("Error", err) 
    finally:
        cur.close()
        bddClose(cnx)

def t1mnLed(tempo): 
    threading.Timer(tempo, t1mnLed, [tempo]).start() 
    ## Reste du traitement
    GPIO.output(Raspiomix.IO0, not GPIO.input(Raspiomix.IO0))

def t100msDetectPorte1(tempo): 
    threading.Timer(tempo / 10, t100msDetectPorte1, [tempo]).start() 
    ## Reste du traitement
    GPIO.output(Raspiomix.IO0, not GPIO.input(Raspiomix.IO0))
    
def t1mnTemperature(tempo): 
#    threading.Timer(tempo * 60, t1mnTemperature, [tempo]).start() 
    threading.Timer(tempo * 60, t1mnTemperature, [tempo]).start() 
    ## Reste du traitement 
    timeCourant = time.strftime('%A %d/%m/%Y %H:%M:%S')
    mesTemperature = int(sensor.read_temperature() * 10)
    print(timeCourant + '  T = ' + str(mesTemperature / 10) + "°C")
    ts = time.time()
    timeReleve = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    sqlQuery = "INSERT INTO releve_capteur (date_heure, valeur, capteur_id) VALUES (%s, '%s', '%s')"
    sqlInsert3Data(sqlQuery, timeReleve, mesTemperature, CAPTEUR_ID_TEMP_BMP280)

#    sqlSelectFetchall("SELECT date_heure, valeur FROM releve_capteur")


def t1mnPression(tempo): 
    threading.Timer(tempo * 60, t1mnPression, [tempo]).start() 
    ## Reste du traitement 
    timeCourant = time.strftime('%A %d/%m/%Y %H:%M:%S')
    mesPression = int(sensor.read_pressure() / 100)
    print(timeCourant + '  T = ' + str(mesPression) + " mb")
    ts = time.time()
    timeReleve = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    sqlQuery = "INSERT INTO releve_capteur (date_heure, valeur, capteur_id) VALUES (%s, '%s', '%s')"
    sqlInsert3Data(sqlQuery, timeReleve, mesPression, CAPTEUR_ID_PRES_BMP280)
    

sensor = BMP280.BMP280()
t1mnTemperature(15)
t1mnPression(60)
t1mnLed(0.5)
#t100msDetectPorte1(1)
