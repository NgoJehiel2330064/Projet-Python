USE master;
GO

BACKUP DATABASE Prog3a25MaStationProd
TO DISK = 'C:\Program Files\Microsoft SQL Server\MSSQL15.MSSQLSERVER\MSSQL\Backup\Prog3a25MaStationProd_FULL.bak'
WITH FORMAT,
     INIT,
     NAME = 'Sauvegarde complète Prog3a25MaStationProd',
     STATS = 10;
GO
