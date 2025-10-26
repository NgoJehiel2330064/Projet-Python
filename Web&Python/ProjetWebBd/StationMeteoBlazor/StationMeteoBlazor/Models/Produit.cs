using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

namespace StationMeteoBlazor.Models;

[Table("Produit")]
public partial class Produit
{
    [Key]
    public int IdProduit { get; set; }

    public int IdUtilisateur { get; set; }

    [ForeignKey("IdUtilisateur")]
    [InverseProperty("Produits")]
    public virtual Utilisateur IdUtilisateurNavigation { get; set; } = null!;
}
