using Microsoft.Data.SqlClient;
using Microsoft.EntityFrameworkCore;
using StationMeteoBlazor.Components;
using StationMeteoBlazor.Data;
using StationMeteoBlazor.Authentification;
using Microsoft.AspNetCore.Components.Authorization;
using Microsoft.AspNetCore.Components.Server.ProtectedBrowserStorage;
using Microsoft.AspNetCore.Authentication.Cookies;
using System.Security.Claims;

namespace StationMeteoBlazor
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);

            var conStrBuilder = new SqlConnectionStringBuilder(builder.Configuration.GetConnectionString("MaConnexion"));
            conStrBuilder.Password = "fenetre98";

            builder.Services.AddDbContextFactory<Prog3a25MaStationContext>(x => x.UseSqlServer(conStrBuilder.ConnectionString));

            builder.Services.AddScoped<DonneeCapteurService>();
            builder.Services.AddScoped<LoginService>();
            builder.Services.AddScoped<SupportService>();
            builder.Services.AddScoped<AuthenticationStateProvider, CustomAuthenticationStateProvider>();
            builder.Services.AddScoped<ProtectedSessionStorage>();

            // Pour Blazor Server utiliser AddAuthorization (pas AddAuthorizationCore)
            builder.Services.AddAuthorization();

            // HttpClient pour appels internes (ex: création du cookie via endpoint)
            builder.Services.AddHttpClient();

            builder.Services.AddAuthentication(CookieAuthenticationDefaults.AuthenticationScheme)
                .AddCookie(options =>
                {
                    options.LoginPath = "/login";
                    options.ExpireTimeSpan = TimeSpan.FromMinutes(20);
                });

            builder.Services.AddRazorComponents()
                .AddInteractiveServerComponents();

            var app = builder.Build();

            if (!app.Environment.IsDevelopment())
            {
                app.UseExceptionHandler("/Error");
                app.UseHsts();
            }

            app.UseHttpsRedirection();
            app.UseStaticFiles();

            app.UseRouting();

            app.UseAuthentication();
            app.UseAuthorization();

            app.UseAntiforgery();

            app.MapRazorComponents<App>()
               .AddInteractiveServerRenderMode();

            app.Run();
        }
    }
}
