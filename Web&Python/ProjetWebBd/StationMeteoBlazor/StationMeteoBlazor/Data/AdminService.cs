using Microsoft.EntityFrameworkCore;
using StationMeteoBlazor.Models;

namespace StationMeteoBlazor.Data
{
    public class AdminService
    {
        private readonly IDbContextFactory<Prog3a25MaStationContext> _factory;

        public AdminService(IDbContextFactory<Prog3a25MaStationContext> factory)
        {
            _factory = factory;
        }

        public async Task<List<Utilisateur>> SearchUsers(string search)
        {
            using var db = _factory.CreateDbContext();

            return await db.Utilisateurs
                .Where(u =>
                    string.IsNullOrEmpty(search) ||
                    u.Nom.Contains(search) ||
                    u.Prenom.Contains(search) ||
                    u.Email.Contains(search))
                .Select(u => new Utilisateur
                {
                    IdUtilisateur = u.IdUtilisateur,
                    Nom = u.Nom,
                    Prenom = u.Prenom,
                    Email = u.Email,
                    Admin = u.Admin
                })
                .ToListAsync();
        }

        public async Task<bool> PromoteToAdmin(int id)
        {
            using var db = _factory.CreateDbContext();

            var user = await db.Utilisateurs.FindAsync(id);
            if (user == null) return false;

            user.Admin = true;

            await db.SaveChangesAsync();
            return true;
        }
    }

}
