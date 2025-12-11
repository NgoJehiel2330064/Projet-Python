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

        public async Task<Utilisateur?> GetUserById(int id)
        {
            using var db = _factory.CreateDbContext();
            return await db.Utilisateurs
                .Where(u => u.IdUtilisateur == id)
                .Select(u => new Utilisateur
                {
                    IdUtilisateur = u.IdUtilisateur,
                    Nom = u.Nom,
                    Prenom = u.Prenom,
                    Email = u.Email
                })
                .FirstOrDefaultAsync();
        }

        public async Task<bool> UpdateUserField(int id, string field, string value)
        {
            using var db = _factory.CreateDbContext();

            var user = await db.Utilisateurs.FirstOrDefaultAsync(x => x.IdUtilisateur == id);
            if (user == null) return false;

            switch (field)
            {
                case "nom": user.Nom = value; break;
                case "prenom": user.Prenom = value; break;
                case "email": user.Email = value; break;
            }

            await db.SaveChangesAsync();
            return true;
        }

    }
}
