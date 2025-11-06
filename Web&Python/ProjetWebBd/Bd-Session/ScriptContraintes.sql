USE Prog3a25MaStation;
GO

 
/* ===== PRIMARY KEY ===== */
ALTER TABLE Utilisateur   ADD CONSTRAINT PK_Utilisateur   PRIMARY KEY (IdUtilisateur);
ALTER TABLE Connexion     ADD CONSTRAINT PK_Connexion     PRIMARY KEY (IdConnexion);
ALTER TABLE Produit       ADD CONSTRAINT PK_Produit       PRIMARY KEY (IdProduit);
ALTER TABLE DonneeCapteur ADD CONSTRAINT PK_DonneeCapteur PRIMARY KEY (IdDonneeCapteur);
ALTER TABLE Ticket        ADD CONSTRAINT PK_Ticket        PRIMARY KEY (IdTicket);
ALTER TABLE Commentaire   ADD CONSTRAINT PK_Commentaire   PRIMARY KEY (IdCommentaire);
ALTER TABLE Alerte        ADD CONSTRAINT PK_Alerte        PRIMARY KEY (IdAlerte);

/* ===== FOREIGN KEY ===== */
ALTER TABLE Connexion
  ADD CONSTRAINT FK_Connexion_User FOREIGN KEY (IdUtilisateur) --Clé etrangère 
  REFERENCES Utilisateur(IdUtilisateur) ON DELETE CASCADE;

ALTER TABLE Produit
  ADD CONSTRAINT FK_Produit_User FOREIGN KEY (IdUtilisateur)
  REFERENCES Utilisateur(IdUtilisateur) ON DELETE CASCADE;

ALTER TABLE DonneeCapteur
  ADD CONSTRAINT FK_Donnee_User FOREIGN KEY (IdUtilisateur)
  REFERENCES Utilisateur(IdUtilisateur) ON DELETE CASCADE;

ALTER TABLE Ticket
  ADD CONSTRAINT FK_Ticket_User FOREIGN KEY (IdUtilisateur)
  REFERENCES Utilisateur(IdUtilisateur) ON DELETE CASCADE;

ALTER TABLE Commentaire
  ADD CONSTRAINT FK_Com_User FOREIGN KEY (IdUtilisateur)
  REFERENCES Utilisateur(IdUtilisateur);

ALTER TABLE Commentaire
  ADD CONSTRAINT FK_Com_Ticket FOREIGN KEY (IdTicket)
  REFERENCES Ticket(IdTicket) ON DELETE CASCADE;

ALTER TABLE Alerte
  ADD CONSTRAINT FK_Alerte_Donnee FOREIGN KEY (IdDonneeCapteur)
  REFERENCES DonneeCapteur(IdDonneeCapteur) ON DELETE CASCADE;


/* ===== UNIQUE ===== */
ALTER TABLE Utilisateur	  ADD CONSTRAINT UQ_Utilisateur_Email UNIQUE (Email);

/* ===== DEFAULT ===== */
ALTER TABLE Utilisateur   ADD CONSTRAINT DF_User_Admin     DEFAULT (0)             FOR Admin;
ALTER TABLE Utilisateur   ADD CONSTRAINT DF_User_DateCre   DEFAULT (SYSDATETIME()) FOR DateCreation;
ALTER TABLE Utilisateur	  ADD CONSTRAINT DF_User_Sel	   DEFAULT  NEWID() FOR Sel;

ALTER TABLE Connexion     ADD CONSTRAINT DF_Connexion_Date DEFAULT (SYSDATETIME()) FOR DateConnexion;

ALTER TABLE DonneeCapteur ADD CONSTRAINT DF_Donnee_Date    DEFAULT (SYSDATETIME()) FOR DateMesure;
-- Valeur par défaut pour la luminosité
ALTER TABLE DonneeCapteur ADD CONSTRAINT DF_Lumiere_Default DEFAULT 0.0 FOR Lumiere;
GO

-- Valeur par défaut pour la pluie
ALTER TABLE DonneeCapteur ADD CONSTRAINT DF_Pluie_Default DEFAULT 0.0 FOR Pluie;
GO

-- Valeur par défaut pour la direction du vent
ALTER TABLE DonneeCapteur ADD CONSTRAINT DF_VentDirection_Default DEFAULT 0.0 FOR VentDirection;
GO

-- Valeur par défaut pour la vitesse du vent
ALTER TABLE DonneeCapteur ADD CONSTRAINT DF_VentVitesse_Default DEFAULT 0.0 FOR VentVitesse;
GO



ALTER TABLE Ticket        ADD CONSTRAINT DF_Ticket_Resolue DEFAULT (0)             FOR Resolue;
ALTER TABLE Ticket        ADD CONSTRAINT DF_Ticket_DateCre DEFAULT (SYSDATETIME()) FOR DateCreation;

ALTER TABLE Commentaire   ADD CONSTRAINT DF_Com_Date       DEFAULT (SYSDATETIME()) FOR DateCommentaire;

ALTER TABLE Alerte        ADD CONSTRAINT DF_Alerte_Active  DEFAULT (1)             FOR Active;
ALTER TABLE Alerte        ADD CONSTRAINT DF_Alerte_DateCre DEFAULT (SYSDATETIME()) FOR DateCreation;

/* ===== CHECK ===== */
ALTER TABLE DonneeCapteur ADD CONSTRAINT CK_Humidite_0_100		CHECK (Humidite BETWEEN 0 AND 100);
ALTER TABLE DonneeCapteur ADD CONSTRAINT CK_VentDir_0_360		CHECK (VentDirection IS NULL OR VentDirection BETWEEN 0 AND 360);
ALTER TABLE DonneeCapteur ADD CONSTRAINT CK_VentVit_Pos			CHECK (VentVitesse  IS NULL OR VentVitesse >= 0);
ALTER TABLE DonneeCapteur ADD CONSTRAINT CK_Donnee_Date_Valide  CHECK (DateMesure <= SYSDATETIME());
ALTER TABLE Ticket        ADD CONSTRAINT CK_Ticket_Resolution_Logique 
CHECK (
    (Resolue = 0 AND DateResolution IS NULL)
 OR (Resolue = 1 AND DateResolution IS NOT NULL)
);



ALTER TABLE Alerte ADD CONSTRAINT CK_Alerte_Capteur CHECK (
  Capteur IN ('temperature','humidite','pression','lumiere','pluie','vent_direction','vent_vitesse')
);





SELECT * from Utilisateur ;