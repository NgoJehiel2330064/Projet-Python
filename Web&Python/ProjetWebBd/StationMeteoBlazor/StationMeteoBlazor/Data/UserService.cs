using StationMeteoBlazor.Models;
using Microsoft.EntityFrameworkCore;
using System.Security.Cryptography;
using System.Text;

namespace StationMeteoBlazor.Data
{
    public class UserService
    {
        private readonly IDbContextFactory<Prog3a25MaStationContext> _factory;

        public UserService(IDbContextFactory<Prog3a25MaStationContext> factory)
        {
            _factory = factory;
        }

        // -------------------------------------------------------
        // 🔐  Hash & Vérification du mot de passe
        // -------------------------------------------------------
        public static string HashPassword(string password, Guid salt)
        {
            using var sha = SHA256.Create();
            var combined = password + salt.ToString();

            var bytes = Encoding.UTF8.GetBytes(combined);
            var hash = sha.ComputeHash(bytes);

            return Convert.ToBase64String(hash);
        }

        public static bool VerifyPassword(string password, Guid salt, string storedHash)
        {
            var hash = HashPassword(password, salt);
            return hash == storedHash;
        }

        // -------------------------------------------------------
        // 🔍  Récupération d'un utilisateur par ID
        // -------------------------------------------------------
        public async Task<Utilisateur?> GetUserById(int idUtilisateur)
        {
            using var context = _factory.CreateDbContext();
            return await context.Utilisateurs.FirstOrDefaultAsync(u => u.IdUtilisateur == idUtilisateur);
        }

        // -------------------------------------------------------
        // ✏️  Modifier profil (Nom, Prénom, Email, Tel, etc.)
        // -------------------------------------------------------
        public async Task<bool> UpdateUserProfile(Utilisateur updated)
        {
            using var context = _factory.CreateDbContext();

            var user = await context.Utilisateurs.FindAsync(updated.IdUtilisateur);
            if (user == null) return false;

            user.Nom = updated.Nom;
            user.Prenom = updated.Prenom;
            user.Email = updated.Email;
            await context.SaveChangesAsync();
            return true;
        }

    }
}
