#!/usr/bin/env python3
# SPDX-License-Identifier: MIT

import time
import smbus2
import bme280
import RPi.GPIO as GPIO
import board
import pyodbc
import adafruit_pcf8591.pcf8591 as PCF8591
from adafruit_pcf8591.analog_in import AnalogIn

# ========== CONFIG CAPTEURS ==========
DO_PIN = 17  # capteur de pluie digital
GPIO.setmode(GPIO.BCM)
GPIO.setup(DO_PIN, GPIO.IN)

# I2C commun
i2c = board.I2C()

# PCF8591 (luminosité / analog)
pcf = PCF8591.PCF8591(i2c)
lumiere_channel = AnalogIn(pcf, PCF8591.A0)

# BME280 (temp, humidité, pression)
bus = smbus2.SMBus(1)
bme_addr = 0x76
calib = bme280.load_calibration_params(bus, bme_addr)

# ========== CONFIG SQL ==========
server = 'dicjwin01.cegepjonquiere.ca'
database = 'Prog3a25MaStation'
username = 'prog3e07'
password = 'fenetre98'

connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    f"TrustServerCertificate=yes;"
)

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# ========== FONCTION INSERT ==========
def enregistrer_donnees(id_user, temp, hum, press, lumiere, pluie):
    cursor.execute("""
        INSERT INTO DonneeCapteur
        (IdUtilisateur, Temperature, Humidite, Pression, Lumiere, Pluie)
        VALUES (?, ?, ?, ?, ?, ?)
    """, id_user, temp, hum, press, lumiere, pluie)

    conn.commit()
    print(">> Données insérées avec succès.")


# ========== BOUCLE PRINCIPALE ==========
try:
    while True:
        # BME280
        data = bme280.sample(bus, bme_addr, calib)
        temp = float(data.temperature)
        hum = float(data.humidity)
        press = float(data.pressure)

        # Lumière via PCF8591
        lumiere = int(lumiere_channel.value)     # 0 - 65535

        # Pluie (0 = pluie, 1 = sec selon ton module)
        pluie = 0 if GPIO.input(DO_PIN) == 0 else 1

        print("===== MESURE =====")
        print(f"Température : {temp:.2f} °C")
        print(f"Humidité    : {hum:.2f} %")
        print(f"Pression    : {press:.2f} hPa")
        print(f"Lumière     : {lumiere}")
        print(f"Pluie       : {pluie}")
        print("===================")

        # INSERTION SQL (IdUtilisateur = 10)
        enregistrer_donnees(10, temp, hum, press, lumiere, pluie)

        time.sleep(3)

except KeyboardInterrupt:
    print("Arrêt du programme.")
except Exception as e:
    print("Erreur :", e)

finally:
    GPIO.cleanup()
    conn.close()
