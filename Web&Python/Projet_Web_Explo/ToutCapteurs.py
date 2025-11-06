# SPDX-License-Identifier: MIT

# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries

import time

import board

import busio

from adafruit_pcf8591.analog_in import AnalogIn

import adafruit_pcf8591.pcf8591 as PCF8591

# Création de la communication I2C

i2c = busio.I2C(board.SCL, board.SDA)

# i2c = board.STEMMA_I2C()  # alternative si tu utilises le connecteur STEMMA QT

# Initialisation du module PCF8591

pcf = PCF8591.PCF8591(i2c)

# Création d’un objet pour le capteur branché sur A0 (ex: photoresistor)

photoresistor = AnalogIn(pcf, PCF8591.A0)

# Boucle de lecture continue

while True:

    print(f"Valeur du photoresistor : {photoresistor.value}")

    time.sleep(1)




#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
import time
import smbus2
import bme280
import RPi.GPIO as GPIO
import board
import adafruit_pcf8591.pcf8591 as PCF8591
from adafruit_pcf8591.analog_in import AnalogIn
# --- Configuration GPIO ---
DO_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(DO_PIN, GPIO.IN)
# --- Initialisation du bus I2C ---
i2c = board.I2C()  # utilise SCL/SDA par défaut
# --- Initialisation du module PCF8591 ---
pcf = PCF8591.PCF8591(i2c)
adc_channel = AnalogIn(pcf, PCF8591.A0)
# --- Initialisation du capteur BME280 ---
bus = smbus2.SMBus(1)
bme280_address = 0x76
calibration_params = bme280.load_calibration_params(bus, bme280_address)
# --- Fonction de conversion ---
def celsius_to_fahrenheit(celsius):
   return (celsius * 9 / 5) + 32
# --- Boucle principale ---
try:
   while True:
       # Lecture du BME280
       data = bme280.sample(bus, bme280_address, calibration_params)
       temp_c = data.temperature
       temp_f = celsius_to_fahrenheit(temp_c)
       pressure = data.pressure
       humidity = data.humidity
       # Lecture du PCF8591 (valeur analogique)
       analog_value = adc_channel.value
       # Affichage des valeurs
       print(f"Température : {temp_c:.2f} °C / {temp_f:.2f} °F")
       print(f"Pression    : {pressure:.2f} hPa")
       print(f"Humidité    : {humidity:.2f} %")
       print(f"Valeur ADC  : {analog_value}")
       print("-" * 40)
       time.sleep(2)
except KeyboardInterrupt:
   print("Programme arrêté proprement.")
   GPIO.cleanup()
except Exception as e:
   print("Erreur :", e)
   GPIO.cleanup()
 