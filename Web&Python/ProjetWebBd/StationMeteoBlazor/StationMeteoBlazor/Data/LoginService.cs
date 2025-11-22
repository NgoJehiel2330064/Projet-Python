using StationMeteoBlazor.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.Data.SqlClient;
using System.Data;

namespace StationMeteoBlazor.Data
{
    public class LoginService
    {
        private readonly IDbContextFactory<Prog3a25MaStationContext> _factory;

        public LoginService(IDbContextFactory<Prog3a25MaStationContext> factory)
        {
            _factory = factory;
        }

        // Retourne (IdUtilisateur, Role). La proc stockée doit remplir @reponseParam (int) et @roleParam (nvarchar).
        public async Task<(int Id, string Role)> SeConnecter(string email, string password)
        {
            using var dbContext = _factory.CreateDbContext();
            var param1 = new SqlParameter("emailParam", email);
            var param2 = new SqlParameter("passwordParam", password);
            var param3 = new SqlParameter("reponseParam", SqlDbType.Int) { Direction = ParameterDirection.Output };
            var param4 = new SqlParameter("roleParam", SqlDbType.NVarChar, 50) { Direction = ParameterDirection.Output };

            await dbContext.Database.ExecuteSqlRawAsync(
                "EXEC connexionProced @emailParam,@passwordParam,@reponseParam OUTPUT,@roleParam OUTPUT",
                param1, param2, param3, param4);

            int id = param3.Value != DBNull.Value ? (int)param3.Value : 0;
            string role = param4.Value != DBNull.Value ? param4.Value.ToString()! : string.Empty;

            return (id, role);
        }
    }
}


