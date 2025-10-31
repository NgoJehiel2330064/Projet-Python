USE Prog3a25MaStation;
GO

/* ==============================================================
   PROCÉDURE : connexionProced
   --------------------------------------------------------------
   But :
     - Vérifier les informations de connexion d'un utilisateur
     - Retourner son IdUtilisateur si la connexion réussit
     - Retourner -1 si les identifiants sont invalides
     - Enregistrer chaque tentative dans la table Connexion
   ============================================================== */
CREATE OR ALTER PROCEDURE connexionProced
    @emailUser      VARCHAR(150),
    @motDePasseUser NVARCHAR(255),
    @reponse        INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        DECLARE @IdUser INT;

        -- Vérifie le mot de passe haché avec le sel
        SELECT @IdUser = IdUtilisateur
        FROM Utilisateur
        WHERE Email = @emailUser
        AND MotDePasse = HASHBYTES('SHA2_512', @motDePasseUser + CAST(ISNULL(Sel, '') AS NVARCHAR(36)));

        -- Si aucun utilisateur trouvé → connexion échouée
        IF @IdUser IS NULL
        BEGIN
            SET @reponse = -1;

			-- Enregistre la tentative de connexion dans la table connexion
            INSERT INTO Connexion (IdUtilisateur, Reussi)
            VALUES (
                (SELECT TOP 1 IdUtilisateur FROM Utilisateur WHERE Email = @emailUser),0);
        END
        ELSE
        BEGIN
            SET @reponse = @IdUser;

			-- Enregistre la tentative de connexion dans la table connexion
            INSERT INTO Connexion (IdUtilisateur, Reussi)
            VALUES (@IdUser, 1);
        END
    END TRY

    BEGIN CATCH
        SET @reponse = -99; -- Code d’erreur générique
    END CATCH
END;
GO
