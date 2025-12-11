using Microsoft.Data.SqlClient;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using System.Data;

namespace StationMeteoBlazor.Data
{
    public class RegisterService
    {

        private readonly IDbContextFactory<Prog3a25MaStationContext> _factory;

        public RegisterService(IDbContextFactory<Prog3a25MaStationContext> factory)
        {
            _factory = factory;
        }

        /// <summary>
        /// Crée un utilisateur via verifieEmailExist
        /// Retourne l'identifiant généré ou 0 si email déjà utilisé.
        /// </summary>
        public async Task<int> CreerUtilisateur(
            string nom,
            string prenom,
            string email,
            string motDePasse,
            bool admin)
        {
            using var dbContext = _factory.CreateDbContext();

            // paramètres d’entrée
            var pNom = new SqlParameter("nom", nom);
            var pPrenom = new SqlParameter("prenom", prenom);
            var pEmail = new SqlParameter("email", email);
            var pMdp = new SqlParameter("motdepasse", motDePasse);
            var pAdmin = new SqlParameter("admin", admin ? 1 : 0);

            // paramètre OUTPUT
            var pIdentifiant = new SqlParameter("identifiant", SqlDbType.Int)
            {
                Direction = ParameterDirection.Output
            };

            // Appel de la procédure stockée
            await dbContext.Database.ExecuteSqlRawAsync(
                "EXEC verifieEmailExist @nom, @prenom, @email, @motdepasse, @admin, @identifiant OUTPUT",
                pNom, pPrenom, pEmail, pMdp, pAdmin, pIdentifiant
            );

            // Retourne l'ID généré (ou 0 si email existant)
            return pIdentifiant.Value != DBNull.Value
                ? (int)pIdentifiant.Value
                : 0;
        }
    }
}
