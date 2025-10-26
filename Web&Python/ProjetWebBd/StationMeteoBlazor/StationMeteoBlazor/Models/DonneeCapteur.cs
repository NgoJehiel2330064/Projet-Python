using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

namespace StationMeteoBlazor.Models;

[Table("DonneeCapteur")]
public partial class DonneeCapteur
{
    [Key]
    public int IdDonneeCapteur { get; set; }

    public int IdUtilisateur { get; set; }

    [Precision(0)]
    public DateTime DateMesure { get; set; }

    [Column(TypeName = "decimal(5, 2)")]
    public decimal Temperature { get; set; }

    [Column(TypeName = "decimal(5, 2)")]
    public decimal Humidite { get; set; }

    [Column(TypeName = "decimal(7, 2)")]
    public decimal Pression { get; set; }

    [Column(TypeName = "decimal(10, 2)")]
    public decimal? Lumiere { get; set; }

    [Column(TypeName = "decimal(10, 2)")]
    public decimal? Pluie { get; set; }

    [Column(TypeName = "decimal(6, 2)")]
    public decimal? VentDirection { get; set; }

    [Column(TypeName = "decimal(6, 2)")]
    public decimal? VentVitesse { get; set; }

    [InverseProperty("IdDonneeCapteurNavigation")]
    public virtual ICollection<Alerte> Alertes { get; set; } = new List<Alerte>();

    [ForeignKey("IdUtilisateur")]
    [InverseProperty("DonneeCapteurs")]
    public virtual Utilisateur IdUtilisateurNavigation { get; set; } = null!;
}
