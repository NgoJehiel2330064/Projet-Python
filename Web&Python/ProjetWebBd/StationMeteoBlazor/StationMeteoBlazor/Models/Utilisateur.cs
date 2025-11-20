using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

namespace StationMeteoBlazor.Models;

[Table("Utilisateur")]
[Index("Email", Name = "UQ_Utilisateur_Email", IsUnique = true)]
public partial class Utilisateur
{
    [Key]
    public int IdUtilisateur { get; set; }

    [StringLength(100)]
    [Unicode(false)]
    public string Nom { get; set; } = null!;

    [StringLength(100)]
    [Unicode(false)]
    public string Prenom { get; set; } = null!;

    [StringLength(150)]
    [Unicode(false)]
    public string Email { get; set; } = null!;

    [MaxLength(64)]
    public byte[] MotDePasse { get; set; } = null!;

    public Guid Sel { get; set; }

    public bool Admin { get; set; }

    [Precision(0)]
    public DateTime DateCreation { get; set; }

    [InverseProperty("IdUtilisateurNavigation")]
    public virtual ICollection<Commentaire> Commentaires { get; set; } = new List<Commentaire>();

    [InverseProperty("IdUtilisateurNavigation")]
    public virtual ICollection<Connexion> Connexions { get; set; } = new List<Connexion>();

    [InverseProperty("IdUtilisateurNavigation")]
    public virtual ICollection<DonneeCapteur> DonneeCapteurs { get; set; } = new List<DonneeCapteur>();

    [InverseProperty("IdUtilisateurNavigation")]
    public virtual ICollection<Produit> Produits { get; set; } = new List<Produit>();

    [InverseProperty("IdUtilisateurNavigation")]
    public virtual ICollection<Ticket> Tickets { get; set; } = new List<Ticket>();
}
