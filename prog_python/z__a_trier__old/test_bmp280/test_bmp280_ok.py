#!/usr/bin/python3.4
# coding: utf-8

import sys 
sys.path.append("/home/pi/prog/j518-supervisor/BMP280")
import time
import BMP280
import locale
locale.setlocale(locale.LC_TIME,'')

#setting timeout for 7 hours
#timeout = time.time() + 60*60*7
sensor = BMP280.BMP280()

while True:
    mesureTime = time.strftime('%A %d/%m/%Y %H:%M:%S')
    mesureTemperature = str(sensor.read_temperature())
    mesurePression = str(int(sensor.read_pressure()))
    print(mesureTime + ',' + mesureTemperature + ',' + mesurePression)
    time.sleep(900)

