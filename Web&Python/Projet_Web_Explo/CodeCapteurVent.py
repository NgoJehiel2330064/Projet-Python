# Rui Santos & Sara Santos - Random Nerd Tutorials
# Projet complet : https://RandomNerdTutorials.com/raspberry-pi-pico-anemometer-micropython/

from machine import ADC, Pin
from time import sleep

# --- Constantes ---
ANEMOMETER_PIN = 26     # GPIO relié à la sortie de l’anémomètre
MIN_VOLTAGE = 0.033     # Tension minimale correspondant à 0 m/s
MAX_VOLTAGE = 3.3       # Tension maximale correspondant à 32.4 m/s
MAX_WIND_SPEED = 32.4   # Vitesse maximale en m/s pour ce modèle

# Facteurs de conversion
MPS_TO_KMH = 3.6        # 1 m/s = 3.6 km/h
MPS_TO_MPH = 2.23694    # 1 m/s = 2.23694 mph

# --- Configuration du capteur ---
adc = ADC(Pin(ANEMOMETER_PIN))

# --- Boucle principale ---
while True:
    # Lecture de la valeur analogique (0 à 65535)
    adc_value = adc.read_u16()

    # Conversion en tension (0 à 3.3V)
    voltage = (adc_value / 65535.0) * 3.3

    # Limiter la tension à la plage valide
    if voltage < MIN_VOLTAGE:
        voltage = MIN_VOLTAGE
    elif voltage > MAX_VOLTAGE:
        voltage = MAX_VOLTAGE

    # Conversion tension → vitesse du vent (m/s)
    wind_speed_mps = ((voltage - MIN_VOLTAGE) / (MAX_VOLTAGE - MIN_VOLTAGE)) * MAX_WIND_SPEED

    # Conversion en km/h et mph
    wind_speed_kmh = wind_speed_mps * MPS_TO_KMH
    wind_speed_mph = wind_speed_mps * MPS_TO_MPH

    # Affichage des résultats
    print("Vitesse du vent :")
    print("{:.2f} m/s".format(wind_speed_mps))
    print("{:.2f} km/h".format(wind_speed_kmh))
    print("{:.2f} mph".format(wind_speed_mph))
    print("---------------------------")

    # Délai avant la prochaine lecture
    sleep(1)
