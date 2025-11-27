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

# Remplacement import tkinter par CustomTkinter si disponible + configuration thème
try:
    import customtkinter as ctk
    tk = ctk  # alias pour garder le reste du code similaire
    USING_CT = True
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
except ImportError:
    import tkinter as tk
    from tkinter import messagebox
    USING_CT = False

# Code Python pour interface de connexion Tkinter utilisant la procédure stockée connexionProced.
import pyodbc


def get_connection():
    """Retourne une connexion pyodbc vers SQL Server."""
    return pyodbc.connect(connection_string)


def authentifier(email: str, mot_de_passe: str) -> tuple[int, str]:
    """Appelle la procédure stockée connexionProced.
    Retourne (code, role)
      code >0 : IdUtilisateur
      code -1 : identifiants invalides
      code -99: erreur interne
      role : 'Admin', 'User' ou ''
    """
    if not email or not mot_de_passe:
        return -1, ''
    try:
        with get_connection() as cnx:
            cur = cnx.cursor()
            cur.execute(
                """
                DECLARE @ret INT, @role NVARCHAR(50);
                EXEC connexionProced @emailUser=?, @motDePasseUser=?, @reponse=@ret OUTPUT, @roleParam=@role OUTPUT;
                SELECT @ret AS reponse, @role AS role;
                """,
                email, mot_de_passe
            )
            row = cur.fetchone()
            if row:
                return int(row[0]), row[1] or ''
            return -99, ''
    except Exception:
        return -99, ''


class MainWindow(tk.CTkToplevel if USING_CT else tk.Toplevel):
    def __init__(self, parent, id_user: int, role: str):
        super().__init__(parent)
        self.title("Accueil")
        self.geometry("420x250")
        label = (tk.CTkLabel if USING_CT else tk.Label)(self, text=f"Bienvenue utilisateur #{id_user} ({role or 'Sans rôle'})")
        label.pack(pady=30)
        btn_frame = (tk.CTkFrame if USING_CT else tk.Frame)(self)
        btn_frame.pack(pady=10)
        (tk.CTkButton if USING_CT else tk.Button)(btn_frame, text="Déconnexion", command=self.logout).grid(row=0, column=0, padx=5)
        (tk.CTkButton if USING_CT else tk.Button)(btn_frame, text="Quitter", command=self.destroy).grid(row=0, column=1, padx=5)

    def logout(self):
        self.destroy()
        # Ré-affiche la fenêtre de login
        self.master.deiconify()
        if hasattr(self.master, 'reset_login'):
            self.master.reset_login()


class LoginWindow(tk.CTk if USING_CT else tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Connexion")
        self.geometry("420x280")
        self.resizable(False, False)

        label_email = (tk.CTkLabel if USING_CT else tk.Label)(self, text="Courriel")
        label_email.pack(anchor="w", padx=20, pady=(20, 0))
        self.email_entry = (tk.CTkEntry if USING_CT else tk.Entry)(self, width=260)
        self.email_entry.pack(padx=20)

        label_pwd = (tk.CTkLabel if USING_CT else tk.Label)(self, text="Mot de passe")
        label_pwd.pack(anchor="w", padx=20, pady=(15, 0))
        self.pwd_entry = (tk.CTkEntry if USING_CT else tk.Entry)(self, width=260, show="*")
        self.pwd_entry.pack(padx=20)

        self.error_label = (tk.CTkLabel if USING_CT else tk.Label)(self, text="", fg_color="transparent", text_color="red" if USING_CT else "red")
        self.error_label.pack(pady=10)

        btn_frame = (tk.CTkFrame if USING_CT else tk.Frame)(self)
        btn_frame.pack(pady=5)
        self.login_btn = (tk.CTkButton if USING_CT else tk.Button)(btn_frame, text="Se connecter", command=self.on_login)
        self.login_btn.grid(row=0, column=0, padx=5)
        cancel_btn = (tk.CTkButton if USING_CT else tk.Button)(btn_frame, text="Quitter", command=self.destroy)
        cancel_btn.grid(row=0, column=1, padx=5)

        self.bind('<Return>', lambda _ : self.on_login())

    def reset_login(self):
        self.pwd_entry.delete(0, 'end') if not USING_CT else self.pwd_entry.delete(0, len(self.pwd_entry.get()))
        self.error_label.configure(text="") if USING_CT else self.error_label.config(text="")
        self.login_btn.configure(state='normal') if USING_CT else self.login_btn.config(state='normal')

    def on_login(self):
        email = self.email_entry.get().strip()
        pwd = self.pwd_entry.get()
        # Désactive bouton pendant tentative
        (self.login_btn.configure if USING_CT else self.login_btn.config)(state='disabled')
        code, role = authentifier(email, pwd)
        if code > 0:
            (self.error_label.configure if USING_CT else self.error_label.config)(text="")
            # Masque la fenêtre de login
            self.withdraw()
            MainWindow(self, code, role)
        elif code == -1:
            (self.error_label.configure if USING_CT else self.error_label.config)(text="Identifiants invalides.")
        else:
            (self.error_label.configure if USING_CT else self.error_label.config)(text="Erreur interne, réessayez plus tard.")
        # Réactive bouton si échec
        if code <= 0:
            (self.login_btn.configure if USING_CT else self.login_btn.config)(state='normal')


def main():
    app = LoginWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
