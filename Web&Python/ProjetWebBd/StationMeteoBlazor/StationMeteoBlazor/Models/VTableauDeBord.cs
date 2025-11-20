using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

namespace StationMeteoBlazor.Models;

[Keyless]
public partial class VTableauDeBord
{
    public int? IdUtilisateur { get; set; }

    [StringLength(100)]
    [Unicode(false)]
    public string? Nom { get; set; }

    [StringLength(100)]
    [Unicode(false)]
    public string? Prenom { get; set; }

    public int? IdTicket { get; set; }

    public string? Probleme { get; set; }

    public bool? Resolue { get; set; }

    [Precision(0)]
    public DateTime? DateTicket { get; set; }

    public int? NbCommentaires { get; set; }

    [Precision(0)]
    public DateTime DerniereMesure { get; set; }

    [Column(TypeName = "decimal(5, 2)")]
    public decimal TemperatureDerniere { get; set; }

    [Column(TypeName = "decimal(5, 2)")]
    public decimal HumiditeDerniere { get; set; }

    [Column(TypeName = "decimal(7, 2)")]
    public decimal PressionDerniere { get; set; }

    [StringLength(3)]
    [Unicode(false)]
    public string AlerteActive { get; set; } = null!;
}
