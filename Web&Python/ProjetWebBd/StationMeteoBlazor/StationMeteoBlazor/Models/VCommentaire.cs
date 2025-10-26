using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

namespace StationMeteoBlazor.Models;

[Keyless]
public partial class VCommentaire
{
    public int IdCommentaire { get; set; }

    public int IdTicket { get; set; }

    public string Probleme { get; set; } = null!;

    [StringLength(100)]
    [Unicode(false)]
    public string Nom { get; set; } = null!;

    [StringLength(100)]
    [Unicode(false)]
    public string Prenom { get; set; } = null!;

    public string Reponse { get; set; } = null!;

    [Precision(0)]
    public DateTime DateCommentaire { get; set; }
}
