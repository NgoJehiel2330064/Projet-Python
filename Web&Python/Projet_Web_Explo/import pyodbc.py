# ============================================================
#  PAGE DE CONNEXION + DASHBOARD CAPTEURS
#  Python / CustomTkinter / SQL Server
# ============================================================

import pyodbc
import threading
import time

# ------------------------------------------------------------
# 1. Informations de connexion SQL Server
# ------------------------------------------------------------
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

# ------------------------------------------------------------
# 2. CustomTkinter ou Tkinter
# ------------------------------------------------------------
try:
    import customtkinter as ctk
    tk = ctk
    USING_CT = True
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
except ImportError:
    import tkinter as tk
    USING_CT = False

# ------------------------------------------------------------
# 3. Connexion SQL
# ------------------------------------------------------------
def get_connection():
    return pyodbc.connect(connection_string)

# ------------------------------------------------------------
# 4. Authentification via procédure stockée
# ------------------------------------------------------------
def authentifier(email: str, mot_de_passe: str) -> tuple[int, str]:
    if not email or not mot_de_passe:
        return -1, ""

    try:
        with get_connection() as cnx:
            cur = cnx.cursor()

            cur.execute("""
                DECLARE @ret INT, @role NVARCHAR(50);
                EXEC connexionProced
                    @emailUser=?, 
                    @motDePasseUser=?, 
                    @reponse=@ret OUTPUT, 
                    @roleParam=@role OUTPUT;
                SELECT @ret, @role;
            """, (email, mot_de_passe))

            row = cur.fetchone()
            print("DEBUG row =", row)

            if row is None:
                return -99, ""

            code = int(row[0]) if row[0] is not None else -99
            role = row[1] if row[1] is not None else ""

            return code, role

    except Exception as e:
        print("ERREUR PYODBC :", e)
        return -99, ""

# =====================================================================
#  ÉCRAN 2 – Dashboard Capteurs
# =====================================================================
class Dashboard(tk.CTkToplevel if USING_CT else tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Station Météo – Dashboard")
        self.geometry("700x500")

        # Variables internes
        self.running = False
        self.frequency = 1.0
        self.seuil_temperature = 28.0

        # ----- Titre -----
        title = tk.CTkLabel(self, text="Données en temps réel", font=("Arial", 22))
        title.pack(pady=15)

        # ----- Données -----
        frame_data = tk.CTkFrame(self, corner_radius=10)
        frame_data.pack(pady=10, padx=20, fill="x")

        self.label_temp = tk.CTkLabel(frame_data, text="Température : -- °C", font=("Arial", 18))
        self.label_hum  = tk.CTkLabel(frame_data, text="Humidité : -- %", font=("Arial", 18))
        self.label_pres = tk.CTkLabel(frame_data, text="Pression : -- hPa", font=("Arial", 18))
        self.label_rain = tk.CTkLabel(frame_data, text="Pluie : --", font=("Arial", 18))

        self.label_temp.pack(pady=5)
        self.label_hum.pack(pady=5)
        self.label_pres.pack(pady=5)
        self.label_rain.pack(pady=5)

        # ----- Boutons -----
        frame_btn = tk.CTkFrame(self)
        frame_btn.pack(pady=15)

        self.btn_start = tk.CTkButton(frame_btn, text="Démarrer collecte", command=self.start_collecte)
        self.btn_stop  = tk.CTkButton(frame_btn, text="Arrêter collecte", command=self.stop_collecte)
        self.btn_start.grid(row=0, column=0, padx=10)
        self.btn_stop.grid(row=0, column=1, padx=10)

        # ----- Fréquence -----
        frame_freq = tk.CTkFrame(self)
        frame_freq.pack(pady=10)

        tk.CTkLabel(frame_freq, text="Fréquence (secondes)").grid(row=0, column=0, padx=10)
        self.freq_entry = tk.CTkEntry(frame_freq, width=80)
        self.freq_entry.insert(0, "1")
        self.freq_entry.grid(row=0, column=1)
        tk.CTkButton(frame_freq, text="Appliquer", command=self.set_frequency).grid(row=0, column=2, padx=10)

        # ----- Seuil -----
        frame_seuil = tk.CTkFrame(self)
        frame_seuil.pack(pady=10)

        tk.CTkLabel(frame_seuil, text="Seuil température max").grid(row=0, column=0, padx=10)
        self.seuil_entry = tk.CTkEntry(frame_seuil, width=80)
        self.seuil_entry.insert(0, "28")
        self.seuil_entry.grid(row=0, column=1)
        tk.CTkButton(frame_seuil, text="Définir", command=self.set_seuil).grid(row=0, column=2, padx=10)

    # ---------------------------------------------------
    # LOGIQUE DASHBOARD
    # ---------------------------------------------------
    def start_collecte(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self.collecte_loop, daemon=True).start()

    def stop_collecte(self):
        self.running = False

    def set_frequency(self):
        try:
            self.frequency = float(self.freq_entry.get())
        except:
            self.frequency = 1.0

    def set_seuil(self):
        try:
            self.seuil_temperature = float(self.seuil_entry.get())
        except:
            pass

    # ---------------------------------------------------
    # Boucle de collecte (simulateur ou vrai capteur)
    # ---------------------------------------------------
    def collecte_loop(self):
        while self.running:
            # ICI TU METS LES VRAIES DONNÉES CAPTEUR
            # Exemple :
            data = lire_capteurs()

            temp = data["temp"]
            hum  = data["hum"]
            pres = data["pres"]
            rain = data["rain"]

            # Mise à jour UI
            self.label_temp.configure(text=f"Température : {temp:.1f} °C")
            self.label_hum.configure(text=f"Humidité : {hum:.1f} %")
            self.label_pres.configure(text=f"Pression : {pres:.1f} hPa")
            self.label_rain.configure(
                text="Pluie : OUI" if rain == 1 else "Pluie : NON",
                text_color="red" if rain == 1 else "white"
            )

            # Seuil température
            if temp > self.seuil_temperature:
                self.label_temp.configure(text_color="red")
            else:
                self.label_temp.configure(text_color="white")

            time.sleep(self.frequency)

# =====================================================================
# SIMULATEUR DE CAPTEUR (À REMPLACER PAR TES VRAIES LECTURES PI)
# =====================================================================
import random
def lire_capteurs():
    return {
        "temp": random.uniform(22, 32),
        "hum": random.uniform(40, 70),
        "pres": random.uniform(990, 1015),
        "rain": random.choice([0, 1])
    }

# =====================================================================
#  LOGIN WINDOW
# =====================================================================
class LoginWindow(tk.CTk if USING_CT else tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Connexion")
        self.geometry("420x280")
        self.resizable(False, False)

        # Email
        tk.CTkLabel(self, text="Courriel").pack(anchor="w", padx=20, pady=(20, 0))
        self.email_entry = tk.CTkEntry(self, width=260)
        self.email_entry.pack(padx=20)

        # Mot de passe
        tk.CTkLabel(self, text="Mot de passe").pack(anchor="w", padx=20, pady=(15, 0))
        self.pwd_entry = tk.CTkEntry(self, width=260, show="*")
        self.pwd_entry.pack(padx=20)

        # Message d’erreur
        self.error_label = tk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack(pady=10)

        # Boutons
        frame_btn = tk.CTkFrame(self)
        frame_btn.pack(pady=5)

        self.login_btn = tk.CTkButton(frame_btn, text="Se connecter", command=self.on_login)
        self.login_btn.grid(row=0, column=0, padx=5)

        tk.CTkButton(frame_btn, text="Quitter", command=self.destroy).grid(row=0, column=1, padx=5)

        self.bind("<Return>", lambda _: self.on_login())

    def reset_login(self):
        self.pwd_entry.delete(0, "end")
        self.error_label.configure(text="")
        self.login_btn.configure(state="normal")

    def on_login(self):
        email = self.email_entry.get().strip()
        pwd = self.pwd_entry.get()

        self.login_btn.configure(state="disabled")

        code, role = authentifier(email, pwd)

        if code > 0:
            self.error_label.configure(text="")
            self.withdraw()
            Dashboard(self)
        elif code == -1:
            self.error_label.configure(text="Identifiants invalides.")
            self.login_btn.configure(state="normal")
        else:
            self.error_label.configure(text="Erreur interne, réessayez.")
            self.login_btn.configure(state="normal")


# =====================================================================
# DÉMARRAGE APPLICATION
# =====================================================================
def main():
    app = LoginWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
