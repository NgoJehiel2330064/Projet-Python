"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import spidev
import time
import RPi.GPIO as GPIO
# --- Connexions matérielles ---
# MCP3008 :
# VDD → 3.3V
# VREF → 3.3V
# AGND/DGND → GND
# CLK → GPIO11 (SCLK)
# DOUT → GPIO9  (MISO)
# DIN → GPIO10  (MOSI)
# CS/SHDN → GPIO8 (CE0)
# CH0 → sortie analogique de l’anémomètre
# --- Configuration SPI ---
spi = spidev.SpiDev()
spi.open(0, 0)      # bus 0, device CE0
spi.max_speed_hz = 1350000
# --- Constantes ---
CHANNEL = 0         # canal MCP3008 relié à l’anémomètre
MIN_VOLTAGE = 0.033 # Vitesse 0 m/s
MAX_VOLTAGE = 3.3   # Vitesse max 32.4 m/s
MAX_WIND_SPEED = 32.4
MPS_TO_KMH = 3.6
MPS_TO_MPH = 2.23694
# --- Fonction de lecture SPI ---
def read_adc(channel):
   if channel < 0 or channel > 7:
       return -1
   r = spi.xfer2([1, (8 + channel) << 4, 0])
   data = ((r[1] & 3) << 8) + r[2]
   return data
# --- Boucle principale ---
try:
   while True:
       # Lecture brute (0–1023)
       adc_value = read_adc(CHANNEL)
       # Conversion en tension (0–3.3 V)
       voltage = (adc_value / 1023.0) * 3.3
       # Clamp
       if voltage < MIN_VOLTAGE:
           voltage = MIN_VOLTAGE
       elif voltage > MAX_VOLTAGE:
           voltage = MAX_VOLTAGE
       # Calcul des vitesses
       wind_mps = ((voltage - MIN_VOLTAGE) / (MAX_VOLTAGE - MIN_VOLTAGE)) * MAX_WIND_SPEED
       wind_kmh = wind_mps * MPS_TO_KMH
       wind_mph = wind_mps * MPS_TO_MPH
       # Affichage
       print(f"Vitesse du vent : {wind_mps:.2f} m/s | {wind_kmh:.2f} km/h | {wind_mph:.2f} mph")
       print("---------------------------")
       time.sleep(1)
except KeyboardInterrupt:
   print("Arrêt du programme.")
finally:
   spi.close()
   GPIO.cleanup()
---

import RPi.GPIO as GPIO
import time
import math
ANEMO_PIN = 26        # signal noir
RADIUS = 0.09         # m
PULSES_PER_REV = 1    # 1 impulsion / tour
GPIO.setmode(GPIO.BCM)
GPIO.setup(ANEMO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
count = 0
def pulse(channel):
   global count
   count += 1
GPIO.add_event_detect(ANEMO_PIN, GPIO.FALLING, callback=pulse)
try:
   while True:
       count = 0
       start = time.time()
       time.sleep(5)
       duration = time.time() - start
       rotations = count / PULSES_PER_REV
       distance = 2 * math.pi * RADIUS * rotations
       wind_speed = distance / duration
       print(f"Vitesse du vent : {wind_speed:.2f} m/s  ({wind_speed*3.6:.2f} km/h)")
except KeyboardInterrupt:
   GPIO.cleanup()
"""

import RPi.GPIO as GPIO
import time
PIN = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
try:
   while True:
       print(GPIO.input(PIN))
       time.sleep(0.01)
except KeyboardInterrupt:
   GPIO.cleanup()