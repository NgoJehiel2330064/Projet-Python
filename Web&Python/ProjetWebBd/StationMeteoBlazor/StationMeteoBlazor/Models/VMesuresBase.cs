using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

namespace StationMeteoBlazor.Models;

[Keyless]
public partial class VMesuresBase
{
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
}
