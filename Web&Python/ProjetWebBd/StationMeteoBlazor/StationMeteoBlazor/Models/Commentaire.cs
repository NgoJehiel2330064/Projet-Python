using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

namespace StationMeteoBlazor.Models;

[Table("Commentaire")]
public partial class Commentaire
{
    [Key]
    public int IdCommentaire { get; set; }

    public int IdUtilisateur { get; set; }

    public int IdTicket { get; set; }

    public string Reponse { get; set; } = null!;

    [Precision(0)]
    public DateTime DateCommentaire { get; set; }

    [ForeignKey("IdTicket")]
    [InverseProperty("Commentaires")]
    public virtual Ticket IdTicketNavigation { get; set; } = null!;

    [ForeignKey("IdUtilisateur")]
    [InverseProperty("Commentaires")]
    public virtual Utilisateur IdUtilisateurNavigation { get; set; } = null!;
}
