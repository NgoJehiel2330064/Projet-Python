USE master;
IF DB_ID('Prog3a25MaStationProd') IS NOT NULL DROP DATABASE Prog3a25MaStationProd;
GO

CREATE DATABASE Prog3a25MaStation;	--Cree une base de donnée
GO
USE Prog3a25MaStation; --j'utilise la base de donnée
GO

CREATE TABLE Utilisateur (
  IdUtilisateur INT IDENTITY(1,1)	NOT NULL,	--Type Int Identity permet de remplacer le auto_increment
  Nom           VARCHAR(100)		NOT NULL,
  Prenom        VARCHAR(100)		NOT NULL,
  Email         VARCHAR(150)		NOT NULL,
  MotDePasse    VARBINARY(64)		NOT NULL,
  Sel           UNIQUEIDENTIFIER	NOT NULL,	
  Admin         BIT					NOT NULL,
  DateCreation  DATETIME2(0)		NOT NULL
);


CREATE TABLE Connexion (
  IdConnexion   INT IDENTITY(1,1)	NOT NULL,
  IdUtilisateur INT					NOT NULL,
  DateConnexion DATETIME2(0)		NOT NULL,
  Reussi        BIT					NOT NULL
);


CREATE TABLE Produit (
  IdProduit     INT IDENTITY(1,1)	NOT NULL,
  IdUtilisateur INT					NOT NULL
);


CREATE TABLE DonneeCapteur (
  IdDonneeCapteur INT IDENTITY(1,1)	NOT NULL,
  IdUtilisateur   INT				NOT NULL,
  DateMesure      DATETIME2(0)		NOT NULL,
  Temperature     DECIMAL(5,2)		NOT NULL,
  Humidite        DECIMAL(5,2)		NOT NULL,
  Pression        DECIMAL(7,2)		NOT NULL,
  Lumiere         DECIMAL(10,2)		NULL,
  Pluie           DECIMAL(10,2)		NULL,
  VentDirection   DECIMAL(6,2)		NULL,
  VentVitesse     DECIMAL(6,2)		NULL
);

CREATE TABLE Alerte (
  IdAlerte        INT IDENTITY(1,1)	NOT NULL,
  IdDonneeCapteur INT				NOT NULL,
  Capteur         VARCHAR(20)		NOT NULL,
  Message         NVARCHAR(300)		NOT NULL,
  Active          BIT				NOT NULL,
  DateCreation    DATETIME2(0)		NOT NULL
);

CREATE TABLE Ticket (
  IdTicket       INT IDENTITY(1,1)	NOT NULL,
  IdUtilisateur  INT				NOT NULL,
  Probleme       NVARCHAR(MAX)		NOT NULL,
  Resolue        BIT				NOT NULL,
  DateCreation   DATETIME2(0)		NOT NULL,
  DateResolution DATETIME2(0)		NULL
);

CREATE TABLE Commentaire (
  IdCommentaire   INT IDENTITY(1,1)	NOT NULL,
  IdUtilisateur   INT				NOT NULL,
  IdTicket        INT				NOT NULL,
  Reponse         NVARCHAR(MAX)		NOT NULL,
  DateCommentaire DATETIME2(0)		NOT NULL
);











