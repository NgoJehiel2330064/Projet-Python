using StationMeteoBlazor.Models;
using Microsoft.EntityFrameworkCore;

namespace StationMeteoBlazor.Data
{
    public class SupportService
    {
        private readonly IDbContextFactory<Prog3a25MaStationContext> _factory;

        public SupportService(IDbContextFactory<Prog3a25MaStationContext> factory)
        {
            _factory = factory;
        }

        // 1. Tickets d’un utilisateur
        public async Task<List<VTicketsAvecUser>> GetTicketUser(int idUtilisateur)
        {
            using var context = _factory.CreateDbContext();
            return await context.VTicketsAvecUsers
                .Where(t => t.IdUtilisateur == idUtilisateur)
                .OrderByDescending(t => t.DateCreation)
                .ToListAsync();
        }

        // 2. Ticket par Id (vue + info utilisateur)
        public async Task<VTicketsAvecUser?> GetTicketById(int idTicket)
        {
            using var context = _factory.CreateDbContext();
            return await context.VTicketsAvecUsers
                .FirstOrDefaultAsync(t => t.IdTicket == idTicket);
        }

        // 3. Liste des commentaires d’un ticket
        public async Task<List<VCommentaire>> GetCommentaires(int idTicket)
        {
            using var context = _factory.CreateDbContext();
            return await context.VCommentaires
                .Where(c => c.IdTicket == idTicket)
                .OrderBy(c => c.DateCommentaire)
                .ToListAsync();
        }

        // 4. Ajouter un commentaire
        public async Task AjouterCommentaire(int idTicket, int idUtilisateur, string reponse)
        {
            using var context = _factory.CreateDbContext();

            var c = new Commentaire
            {
                IdTicket = idTicket,
                IdUtilisateur = idUtilisateur,
                Reponse = reponse,
                DateCommentaire = DateTime.Now
            };

            context.Commentaires.Add(c);
            await context.SaveChangesAsync();
        }

        // 5. Créer un ticket
        public async Task CreerTicket(int idUtilisateur, string probleme)
        {
            using var context = _factory.CreateDbContext();

            var t = new Ticket
            {
                IdUtilisateur = idUtilisateur,
                Probleme = probleme,
                Resolue = false,
                DateCreation = DateTime.Now
            };

            context.Tickets.Add(t);
            await context.SaveChangesAsync();
        }

        // 6. Marquer comme résolu
        public async Task MarquerCommeResolue(int idTicket)
        {
            using var context = _factory.CreateDbContext();

            var t = await context.Tickets.FindAsync(idTicket);
            if (t == null) return;

            t.Resolue = true;
            t.DateResolution = DateTime.Now;

            await context.SaveChangesAsync();
        }

        // ADMIN : Tous les tickets
        public async Task<List<VTicketsAvecUser>> GetAllTickets()
        {
            using var context = _factory.CreateDbContext();

            return await context.VTicketsAvecUsers
                .OrderByDescending(t => t.DateCreation)
                .ToListAsync();
        }

        public async Task<Dictionary<string, int>> GetStats()
        {
            using var context = _factory.CreateDbContext();

            int total = await context.VTicketsAvecUsers.CountAsync();
            int resolus = await context.VTicketsAvecUsers.Where(t => t.Resolue).CountAsync();
            int nonResolus = await context.VTicketsAvecUsers.Where(t => !t.Resolue).CountAsync();
            int aujourdHui = await context.VTicketsAvecUsers
                .Where(t => t.DateCreation.Date == DateTime.Now.Date)
                .CountAsync();

            return new Dictionary<string, int>
    {
        { "total", total },
        { "resolus", resolus },
        { "nonResolus", nonResolus },
        { "aujourdHui", aujourdHui }
    };
        }

    }


}

