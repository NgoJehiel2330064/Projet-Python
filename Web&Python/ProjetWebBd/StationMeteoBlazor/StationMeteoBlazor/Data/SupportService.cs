using StationMeteoBlazor.Models; 
using Microsoft.EntityFrameworkCore;
using Microsoft.Data.SqlClient;




namespace StationMeteoBlazor.Data
{
    public class SupportService
    {

        private readonly IDbContextFactory<Prog3a25MaStationContext> _factory;

        public SupportService(IDbContextFactory<Prog3a25MaStationContext> factory)
        {
            _factory = factory;
        }

        public async Task<List<VTicketsAvecUser>> GetTicketUser(int id)
        {
            var context = _factory.CreateDbContext();
            var ticketUser = context.VTicketsAvecUsers.Where(t => t.IdUtilisateur == id).ToListAsync();

            return await ticketUser;
        }

    }
}
