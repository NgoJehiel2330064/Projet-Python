using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

namespace StationMeteoBlazor.Models;

[Keyless]
public partial class VAlerte
{
    public int IdAlerte { get; set; }

    [StringLength(20)]
    [Unicode(false)]
    public string Capteur { get; set; } = null!;

    [StringLength(300)]
    public string Message { get; set; } = null!;

    public bool Active { get; set; }

    [Precision(0)]
    public DateTime DateCreation { get; set; }

    public int IdDonneeCapteur { get; set; }

    public int IdUtilisateur { get; set; }

    [Precision(0)]
    public DateTime DateMesure { get; set; }
}
