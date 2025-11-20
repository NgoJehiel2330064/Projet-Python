using StationMeteoBlazor.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.Data.SqlClient;


namespace StationMeteoBlazor.Data
{
    public class LoginService
    {

        private readonly IDbContextFactory<Prog3a25MaStationContext> _factory;

        public LoginService(IDbContextFactory<Prog3a25MaStationContext> factory)
        {
            _factory = factory;
        }

        public async Task<int> SeConnecter(string email, string password)
        {
            
            var dbContext = _factory.CreateDbContext();
            var param1 = new SqlParameter("emailParam", email);
            var param2 = new SqlParameter("passwordParam",password);
            var param3 = new SqlParameter("reponseParam", System.Data.SqlDbType.Int)
            {
                Direction = System.Data.ParameterDirection.Output
            };

           await dbContext.Database.ExecuteSqlRawAsync("EXEC connexionProced @emailParam,@passwordParam,@reponseParam OUTPUT", param1, param2,param3);
            return (int)param3.Value;
         }
    }
}


