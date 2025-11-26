USE Prog3a25MaStation;
GO

CREATE OR ALTER PROCEDURE connexionProced
    @emailUser      VARCHAR(150),
    @motDePasseUser NVARCHAR(255),
    @reponse        INT OUTPUT,
    @roleParam      NVARCHAR(50) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        DECLARE @IdUser INT;
        DECLARE @IsAdmin BIT;

        -- Vérification du login
        SELECT 
            @IdUser = IdUtilisateur,
            @IsAdmin = Admin
        FROM Utilisateur
        WHERE Email = @emailUser
        AND MotDePasse = HASHBYTES('SHA2_512', @motDePasseUser + CAST(ISNULL(Sel, '') AS NVARCHAR(36)));

        -- Échec de connexion
        IF @IdUser IS NULL
        BEGIN
            SET @reponse = -1;
            SET @roleParam = '';  -- Aucun rôle

            INSERT INTO Connexion (IdUtilisateur, Reussi)
            VALUES (
                (SELECT TOP 1 IdUtilisateur FROM Utilisateur WHERE Email = @emailUser),
                0
            );
        END
        ELSE
        BEGIN
            -- Succès
            SET @reponse = @IdUser;
            SET @roleParam = CASE WHEN @IsAdmin = 1 THEN 'Admin' ELSE 'User' END;

            INSERT INTO Connexion (IdUtilisateur, Reussi)
            VALUES (@IdUser, 1);
        END
    END TRY

    BEGIN CATCH
        SET @reponse = -99;
        SET @roleParam = '';
    END CATCH
END;
GO
