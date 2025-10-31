USE Prog3a25MaStation;
GO

/* Derni�res mesures de capteur */
CREATE  OR ALTER VIEW v_MesuresBase AS
SELECT IdDonneeCapteur, IdUtilisateur, DateMesure, Temperature, Humidite, Pression
FROM DonneeCapteur;
GO

/* Tickets avec le nom de l�utilisateur */
CREATE OR ALTER VIEW v_TicketsAvecUser AS
SELECT t.IdTicket, u.Nom, u.Prenom, t.Probleme, t.Resolue, t.DateCreation
FROM Ticket t
JOIN Utilisateur u ON u.IdUtilisateur = t.IdUtilisateur;
GO

/* Commentaires avec ticket et auteur  */
CREATE OR ALTER VIEW v_Commentaires AS
SELECT c.IdCommentaire, c.IdTicket, t.Probleme, u.Nom, u.Prenom, c.Reponse, c.DateCommentaire
FROM Commentaire c
JOIN Ticket t      ON t.IdTicket = c.IdTicket
JOIN Utilisateur u ON u.IdUtilisateur = c.IdUtilisateur;
GO

/* ===========================================================
  VUE : v_TableauDeBord
  -----------------------------------------------------------
  Objectif :
  Fournir une vue globale combinant :
  - les utilisateurs
  - leurs tickets
  - le nombre de commentaires par ticket
  - la derni�re mesure de capteur (r�elle)
  - la pr�sence ou non d'une alerte active
  Technique :
  Utilise CROSS APPLY pour r�cup�rer la derni�re mesure
  de chaque utilisateur sans r�p�ter plusieurs sous-requ�tes.
  =========================================================== */

CREATE OR ALTER VIEW v_TableauDeBord AS
SELECT
   u.IdUtilisateur,
   u.Nom,
   u.Prenom,
   t.IdTicket,
   t.Probleme,
   t.Resolue,
   t.DateCreation AS DateTicket,
   COUNT(c.IdCommentaire) AS NbCommentaires,
   -- Donn�es issues de la derni�re mesure via CROSS APPLY
   Derniere.DateMesure   AS DerniereMesure,
   Derniere.Temperature  AS TemperatureDerniere,
   Derniere.Humidite     AS HumiditeDerniere,
   Derniere.Pression     AS PressionDerniere,
   -- V�rifie si l'utilisateur a une alerte active
   CASE
       WHEN EXISTS (
           SELECT 1
           FROM Alerte a
           JOIN DonneeCapteur dca
             ON a.IdDonneeCapteur = dca.IdDonneeCapteur
           WHERE dca.IdUtilisateur = u.IdUtilisateur
             AND a.Active = 1
       ) THEN 'Oui'
       ELSE 'Non'
   END AS AlerteActive
FROM Ticket t
full Outer JOIN Utilisateur u
   ON u.IdUtilisateur = t.IdUtilisateur
FULL outer JOIN Commentaire c
   ON c.IdTicket = t.IdTicket
-- CROSS APPLY : r�cup�re la derni�re mesure de chaque utilisateur
CROSS APPLY (
   SELECT TOP 1
       Temperature,
       Humidite,
       Pression,
       DateMesure
   FROM DonneeCapteur d2
   WHERE d2.IdUtilisateur = u.IdUtilisateur
   ORDER BY DateMesure DESC
) Derniere
GROUP BY
   u.IdUtilisateur,
   u.Nom,
   u.Prenom,
   t.IdTicket,
   t.Probleme,
   t.Resolue,
   t.DateCreation,
   Derniere.DateMesure,
   Derniere.Temperature,
   Derniere.Humidite,
   Derniere.Pression;
GO