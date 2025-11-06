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
    cursor.execute("SELECT TOP 5 * FROM Utilisateur;")

    for row in cursor.fetchall():
        print(row)

except Exception as e:
    print(" Erreur de connexion ou d'exécution :", e)

finally:
    if 'conn' in locals():
        conn.close()
        print(" Connexion fermée.")


