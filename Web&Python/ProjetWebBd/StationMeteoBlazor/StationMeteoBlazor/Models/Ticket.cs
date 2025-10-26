using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

namespace StationMeteoBlazor.Models;

[Table("Ticket")]
public partial class Ticket
{
    [Key]
    public int IdTicket { get; set; }

    public int IdUtilisateur { get; set; }

    public string Probleme { get; set; } = null!;

    public bool Resolue { get; set; }

    [Precision(0)]
    public DateTime DateCreation { get; set; }

    [Precision(0)]
    public DateTime? DateResolution { get; set; }

    [InverseProperty("IdTicketNavigation")]
    public virtual ICollection<Commentaire> Commentaires { get; set; } = new List<Commentaire>();

    [ForeignKey("IdUtilisateur")]
    [InverseProperty("Tickets")]
    public virtual Utilisateur IdUtilisateurNavigation { get; set; } = null!;
}
