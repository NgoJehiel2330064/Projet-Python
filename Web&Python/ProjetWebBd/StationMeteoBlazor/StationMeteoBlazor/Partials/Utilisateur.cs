using Microsoft.EntityFrameworkCore;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;


namespace StationMeteoBlazor.Models;
public partial class Utilisateur
{
    [NotMapped]
    public string MotDePasseNonHash { get; set; } = null!;
}

