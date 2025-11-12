using Microsoft.AspNetCore.Components.Server.ProtectedBrowserStorage;
using StationMeteoBlazor.Components;
using StationMeteoBlazor.Authentification;
using Microsoft.AspNetCore.Components.Authorization;

namespace StationMeteoBlazor
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);

            // Add services to the container.
            builder.Services.AddRazorComponents()
                .AddInteractiveServerComponents();
            builder.Services.AddScoped<ProtectedSessionStorage>();
            //ajout de de d authentificationState
            builder.Services.AddScoped<AuthenticationStateProvider, CustomAuthenticationStateProvider >();
            builder.Services.AddAuthenticationCore();

            var app = builder.Build();

            // Configure the HTTP request pipeline.
            if (!app.Environment.IsDevelopment())
            {
                app.UseExceptionHandler("/Error");
                // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
                app.UseHsts();
            }

            app.UseHttpsRedirection();

            app.UseStaticFiles();
            app.UseAntiforgery();

            app.MapRazorComponents<App>()
                .AddInteractiveServerRenderMode();


            app.Run();
        }
    }
}
