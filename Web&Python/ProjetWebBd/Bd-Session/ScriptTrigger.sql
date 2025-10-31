USE Prog3a25MaStation;
GO

CREATE OR ALTER TRIGGER Ticket_Resolution 
ON dbo.Ticket AFTER UPDATE AS
BEGIN

SET NOCOUNT ON;

UPDATE t
SET DateResolution = SYSDATETIME() -- Met � jour la date de r�solution
FROM Ticket t 
JOIN inserted i --Utilise la table Tiket et la join � inserted qui contient les nouvelles donn�es mise � jour
ON t.IdTicket = i.IdTicket 
JOIN deleted d ON t.IdTicket = d.IdTicket -- Ici on utilise deleted qui contient les donn�es avant la mise � jour
WHERE i.Resolue = 1 AND d.Resolue = 0 AND t.DateResolution IS NULL; -- Ici l'on regarde si resolue inserted = 1 ainsi que les autres conditions

END;

