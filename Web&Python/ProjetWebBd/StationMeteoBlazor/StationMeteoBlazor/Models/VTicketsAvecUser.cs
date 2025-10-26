using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

namespace StationMeteoBlazor.Models;

[Keyless]
public partial class VTicketsAvecUser
{
    public int IdTicket { get; set; }

    [StringLength(100)]
    [Unicode(false)]
    public string Nom { get; set; } = null!;

    [StringLength(100)]
    [Unicode(false)]
    public string Prenom { get; set; } = null!;

    public string Probleme { get; set; } = null!;

    public bool Resolue { get; set; }

    [Precision(0)]
    public DateTime DateCreation { get; set; }
}
