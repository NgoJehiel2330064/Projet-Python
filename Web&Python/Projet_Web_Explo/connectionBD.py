import pymssql


# Informations de connexion
server = 'dicjwin01.cegepjonquiere.ca'   # ton vrai serveur SQL
database = 'Prog3a25MaStation'
username = 'prog3e07'
password = 'fenetre98'

conn = pymssql.connect(
    server= server,
    user=username,
    password=password,
    database=database
)


try:

    cursor = conn.cursor()
    
    cursor.execute("""INSERT INTO DonneeCapteur (IdUtilisateur,DateMesure,Temperature, Humidite, Pression, Lumiere, Pluie, VentDirection, VentVitesse)
                    VALUES
                    (10,GETDATE(), 22.5, 45.0, 1013.25, 300.0, 0.0, 180.0, 5.2),
                    (10,GETDATE(), 22.7, 44.5, 1013.10, 320.0, 0.0, 185.0, 4.8),
                    (10,GETDATE(), 23.0, 43.8, 1012.95, 340.0, 0.0, 190.0, 4.5),
                    (10,GETDATE(), 23.3, 43.0, 1012.70, 360.0, 0.0, 200.0, 4.2)
                    """)

    conn.commit()
    print("Insertion réussie.")

except Exception as e:
    print("Erreur :", e)

finally:
    if 'conn' in locals():
        conn.close()
        print(" Connexion fermée.")



