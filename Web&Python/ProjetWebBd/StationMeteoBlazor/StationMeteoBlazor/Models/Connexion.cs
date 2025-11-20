using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

namespace StationMeteoBlazor.Models;

[Table("Connexion")]
public partial class Connexion
{
    [Key]
    public int IdConnexion { get; set; }

    public int IdUtilisateur { get; set; }

    [Precision(0)]
    public DateTime DateConnexion { get; set; }

    public bool Reussi { get; set; }

    [ForeignKey("IdUtilisateur")]
    [InverseProperty("Connexions")]
    public virtual Utilisateur IdUtilisateurNavigation { get; set; } = null!;
}
