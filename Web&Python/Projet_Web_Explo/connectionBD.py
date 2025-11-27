import pyodbc


# Informations de connexion
server = 'dicjwin01.cegepjonquiere.ca'   # ton vrai serveur SQL
database = 'Prog3a25MaStation'
username = 'prog3e07'
password = 'fenetre98'

# Chaîne de connexion
connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    f"TrustServerCertificate=yes;"
)


try:
    conn = pyodbc.connect(connection_string)
    print(" Connexion réussie à la base de données.")

    cursor = conn.cursor()
    cursor.execute("""INSERT INTO DonneeCapteur (IdUtilisateur, Temperature, Humidite, Pression, Lumiere, Pluie, VentDirection, VentVitesse)
                    VALUES
                    (10, 22.5, 45.0, 1013.25, 300.0, 0.0, 180.0, 5.2),
                    (10, 22.7, 44.5, 1013.10, 320.0, 0.0, 185.0, 4.8),
                    (10, 23.0, 43.8, 1012.95, 340.0, 0.0, 190.0, 4.5),
                    (10, 23.3, 43.0, 1012.70, 360.0, 0.0, 200.0, 4.2)
                    """)

    conn.commit()
    print("Insertion réussie.")

except Exception as e:
    print("Erreur :", e)

finally:
    if 'conn' in locals():
        conn.close()
        print(" Connexion fermée.")



