import threading
import time
import random
import tkinter as tk
from tkinter import messagebox

try:
    import mysql.connector  # Optionnel si disponible
except ImportError:  # Sur Raspberry Pi installer via: pip install mysql-connector-python
    mysql = None

# Configuration (adapter selon votre environnement Raspberry Pi / Base de données)
DB_CONFIG = {
    "host": "localhost",
    "user": "pi",
    "password": "raspberry",
    "database": "projet"
}
STORED_PROC_LOGIN = "sp_login"  # Nom de la procédure stockée SQL (à créer côté BD)

class DataCollector(threading.Thread):
    def __init__(self, callback_update, get_frequency, running_flag, stop_event):
        super().__init__(daemon=True)
        self.callback_update = callback_update
        self.get_frequency = get_frequency
        self.running_flag = running_flag
        self.stop_event = stop_event

    def run(self):
        while not self.stop_event.is_set():
            if self.running_flag.is_set():
                # Simulation capteurs (adapter avec vrai capteur)
                data = {
                    'temperature': round(random.uniform(18.0, 30.0), 2),
                    'humidite': round(random.uniform(30.0, 70.0), 2),
                    'distance': round(random.uniform(5.0, 150.0), 2)
                }
                self.callback_update(data)
            time.sleep(max(0.2, self.get_frequency()))

class LoginFrame(tk.Frame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.on_login_success = on_login_success
        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="Connexion", font=("Arial", 18, "bold")).pack(pady=10)
        form = tk.Frame(self)
        form.pack(pady=10)
        tk.Label(form, text="Utilisateur").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        tk.Label(form, text="Mot de passe").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_user = tk.Entry(form)
        self.entry_pass = tk.Entry(form, show="*")
        self.entry_user.grid(row=0, column=1, padx=5, pady=5)
        self.entry_pass.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self, text="Se connecter", command=self.try_login).pack(pady=10)

    def try_login(self):
        user = self.entry_user.get().strip()
        pwd = self.entry_pass.get().strip()
        if not user or not pwd:
            messagebox.showerror("Erreur", "Veuillez entrer utilisateur et mot de passe.")
            return
        ok = self._authenticate_db(user, pwd)
        if ok:
            self.on_login_success(user)
        else:
            messagebox.showerror("Échec", "Identifiants invalides.")

    def _authenticate_db(self, user, pwd):
        # Procédure stockée attendue: sp_login(IN p_user VARCHAR, IN p_pwd VARCHAR)
        # Doit retourner un jeu de résultats indiquant succès (ex: SELECT 1 AS ok)
        if mysql and mysql.connector:  # tentative réelle
            try:
                cnx = mysql.connector.connect(**DB_CONFIG)
                cur = cnx.cursor()
                # Appel de la procédure stockée
                cur.callproc(STORED_PROC_LOGIN, [user, pwd])
                # Récupération des jeux de résultats de la procédure
                for result in cur.stored_results():
                    rows = result.fetchall()
                    if rows:
                        # Supposons première colonne = ok (1 ou 0)
                        val = rows[0][0]
                        cur.close(); cnx.close()
                        return bool(val)
                cur.close(); cnx.close()
            except Exception as e:
                print("[WARN] Auth BD échouée, bascule sur simulation:", e)
        # Fallback simulation
        return user == "admin" and pwd == "admin"

class MainFrame(tk.Frame):
    def __init__(self, master, username, start_collector, stop_collector, get_state, set_frequency, get_frequency, set_threshold, get_threshold):
        super().__init__(master)
        self.username = username
        self.start_collector = start_collector
        self.stop_collector = stop_collector
        self.get_state = get_state
        self.set_frequency = set_frequency
        self.get_frequency = get_frequency
        self.set_threshold = set_threshold
        self.get_threshold = get_threshold
        self.latest_data = {}
        self.build_ui()
        self.update_display_periodic()

    def build_ui(self):
        top = tk.Frame(self)
        top.pack(fill="x", pady=5)
        tk.Label(top, text=f"Utilisateur: {self.username}", font=("Arial", 12)).pack(side="left", padx=10)
        tk.Button(top, text="Déconnexion", command=self.logout).pack(side="right", padx=10)

        data_box = tk.LabelFrame(self, text="Données capteur", padx=10, pady=10)
        data_box.pack(fill="x", padx=10, pady=5)
        self.var_temp = tk.StringVar(value="--")
        self.var_hum = tk.StringVar(value="--")
        self.var_dist = tk.StringVar(value="--")
        tk.Label(data_box, text="Température (°C):").grid(row=0, column=0, sticky="w")
        tk.Label(data_box, textvariable=self.var_temp).grid(row=0, column=1, sticky="w")
        tk.Label(data_box, text="Humidité (%):").grid(row=1, column=0, sticky="w")
        tk.Label(data_box, textvariable=self.var_hum).grid(row=1, column=1, sticky="w")
        tk.Label(data_box, text="Distance (cm):").grid(row=2, column=0, sticky="w")
        tk.Label(data_box, textvariable=self.var_dist).grid(row=2, column=1, sticky="w")

        control_box = tk.LabelFrame(self, text="Contrôle", padx=10, pady=10)
        control_box.pack(fill="x", padx=10, pady=5)
        self.btn_start = tk.Button(control_box, text="Démarrer", command=self.toggle_start)
        self.btn_start.grid(row=0, column=0, padx=5, pady=5)
        tk.Label(control_box, text="Fréquence (s)").grid(row=0, column=1, padx=5)
        self.spin_freq = tk.Spinbox(control_box, from_=0.2, to=10.0, increment=0.2, width=6, command=self.apply_frequency)
        self.spin_freq.delete(0, "end")
        self.spin_freq.insert(0, str(self.get_frequency()))
        self.spin_freq.grid(row=0, column=2, padx=5, pady=5)

        tk.Label(control_box, text="Seuil Température (°C)").grid(row=1, column=0, padx=5, pady=5)
        self.entry_threshold = tk.Entry(control_box, width=6)
        self.entry_threshold.insert(0, str(self.get_threshold()))
        self.entry_threshold.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(control_box, text="Appliquer seuil", command=self.apply_threshold).grid(row=1, column=2, padx=5, pady=5)

        self.label_status = tk.Label(self, text="Status: Arrêté", fg="red")
        self.label_status.pack(pady=5)

    def logout(self):
        self.master.show_login()

    def toggle_start(self):
        if self.get_state():
            self.stop_collector()
            self.btn_start.configure(text="Démarrer")
            self.label_status.configure(text="Status: Arrêté", fg="red")
        else:
            self.start_collector()
            self.btn_start.configure(text="Arrêter")
            self.label_status.configure(text="Status: En cours", fg="green")

    def apply_frequency(self):
        try:
            val = float(self.spin_freq.get())
            self.set_frequency(val)
        except ValueError:
            messagebox.showerror("Erreur", "Valeur fréquence invalide")

    def apply_threshold(self):
        try:
            val = float(self.entry_threshold.get())
            self.set_threshold(val)
        except ValueError:
            messagebox.showerror("Erreur", "Valeur seuil invalide")

    def update_display_periodic(self):
        if self.latest_data:
            temp = self.latest_data.get('temperature', '--')
            hum = self.latest_data.get('humidite', '--')
            dist = self.latest_data.get('distance', '--')
            self.var_temp.set(temp)
            self.var_hum.set(hum)
            self.var_dist.set(dist)
            # Indication seuil
            try:
                threshold = self.get_threshold()
                if isinstance(temp, (int, float)) and temp > threshold:
                    self.var_temp.set(f"{temp} !")
            except Exception:
                pass
        self.after(500, self.update_display_periodic)

    def receive_data(self, data):
        self.latest_data = data

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interface Capteur")
        self.geometry("420x420")
        # États
        self.running_flag = threading.Event()
        self.stop_event = threading.Event()
        self.frequency = 1.0
        self.temp_threshold = 28.0
        self.collector = DataCollector(self._on_data, self._get_frequency, self.running_flag, self.stop_event)
        self.collector.start()
        self.current_main_frame = None
        self.login_frame = LoginFrame(self, self.on_login_success)
        self.login_frame.pack(fill="both", expand=True)

    # --- Login / Navigation ---
    def on_login_success(self, username):
        self.login_frame.pack_forget()
        self.show_main(username)

    def show_login(self):
        if self.current_main_frame:
            self.current_main_frame.pack_forget()
            self.current_main_frame = None
        self.login_frame = LoginFrame(self, self.on_login_success)
        self.login_frame.pack(fill="both", expand=True)

    def show_main(self, username):
        self.current_main_frame = MainFrame(
            self,
            username,
            start_collector=self.start_collection,
            stop_collector=self.stop_collection,
            get_state=lambda: self.running_flag.is_set(),
            set_frequency=self.set_frequency,
            get_frequency=self._get_frequency,
            set_threshold=self.set_threshold,
            get_threshold=self.get_threshold
        )
        self.current_main_frame.pack(fill="both", expand=True)

    # --- Capteur / Données ---
    def _on_data(self, data):
        if self.current_main_frame:
            self.current_main_frame.receive_data(data)

    def start_collection(self):
        self.running_flag.set()

    def stop_collection(self):
        self.running_flag.clear()

    def set_frequency(self, val: float):
        self.frequency = max(0.2, float(val))

    def _get_frequency(self):
        return self.frequency

    def set_threshold(self, val: float):
        self.temp_threshold = float(val)

    def get_threshold(self):
        return self.temp_threshold

    def on_close(self):
        self.stop_event.set()
        self.destroy()

# --- Entrée principale ---
if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()