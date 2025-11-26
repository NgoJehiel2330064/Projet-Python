using StationMeteoBlazor.Models; //Donne accès à la classe DonneeCapteur
using Microsoft.EntityFrameworkCore;

namespace StationMeteoBlazor.Data
{
    public class DonneeCapteurService
    {
        private readonly IDbContextFactory<Prog3a25MaStationContext> _factory;

        public DonneeCapteurService(IDbContextFactory<Prog3a25MaStationContext> factory)
        {
            _factory = factory;
        }

        public async Task<List<DonneeCapteur>> GetAllAsync(int id)
        {
            var context = _factory.CreateDbContext();
            var capteurs = context.DonneeCapteurs.Where(context => context.IdUtilisateur == id).OrderByDescending(c => c.DateMesure).ToListAsync();

            return await capteurs;
        }
    }
}
