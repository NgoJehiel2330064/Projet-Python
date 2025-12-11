using StationMeteoBlazor.Models; //Donne accès à la classe DonneeCapteur
using Microsoft.EntityFrameworkCore;

namespace StationMeteoBlazor.Data
{
    public class ParmService
    {
        private readonly IDbContextFactory<Prog3a25MaStationContext> _factory;

        public ParmService(IDbContextFactory<Prog3a25MaStationContext> factory)
        {
            _factory = factory;
        }

        public async Task<Utilisateur?> GetUtilisateurById(int id)
        {
            var context = _factory.CreateDbContext();
            return await context.Utilisateurs.FirstOrDefaultAsync(u => u.IdUtilisateur == id);

        }


        public async Task<DonneeCapteur?> GetAllAsync(int id)
        {
            using var context = _factory.CreateDbContext();

            var capteur = await context.DonneeCapteurs
                .Where(c => c.IdUtilisateur == id)
                .OrderByDescending(c => c.DateMesure)
                .FirstOrDefaultAsync();

            return capteur;
        }
    }
}
