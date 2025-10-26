using System;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;
using StationMeteoBlazor.Models;

namespace StationMeteoBlazor.Data;

public partial class Prog3a25MaStationContext : DbContext
{
    public Prog3a25MaStationContext()
    {
    }

    public Prog3a25MaStationContext(DbContextOptions<Prog3a25MaStationContext> options)
        : base(options)
    {
    }

    public virtual DbSet<Alerte> Alertes { get; set; }

    public virtual DbSet<Commentaire> Commentaires { get; set; }

    public virtual DbSet<DonneeCapteur> DonneeCapteurs { get; set; }

    public virtual DbSet<Produit> Produits { get; set; }

    public virtual DbSet<Ticket> Tickets { get; set; }

    public virtual DbSet<Utilisateur> Utilisateurs { get; set; }

    public virtual DbSet<VAlerte> VAlertes { get; set; }

    public virtual DbSet<VCommentaire> VCommentaires { get; set; }

    public virtual DbSet<VMesuresBase> VMesuresBases { get; set; }

    public virtual DbSet<VTableauDeBord> VTableauDeBords { get; set; }

    public virtual DbSet<VTicketsAvecUser> VTicketsAvecUsers { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        => optionsBuilder.UseSqlServer("Name=MaConnexion");

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Alerte>(entity =>
        {
            entity.Property(e => e.Active).HasDefaultValue(true);
            entity.Property(e => e.DateCreation).HasDefaultValueSql("(sysdatetime())");

            entity.HasOne(d => d.IdDonneeCapteurNavigation).WithMany(p => p.Alertes).HasConstraintName("FK_Alerte_Donnee");
        });

        modelBuilder.Entity<Commentaire>(entity =>
        {
            entity.Property(e => e.DateCommentaire).HasDefaultValueSql("(sysdatetime())");

            entity.HasOne(d => d.IdTicketNavigation).WithMany(p => p.Commentaires).HasConstraintName("FK_Com_Ticket");

            entity.HasOne(d => d.IdUtilisateurNavigation).WithMany(p => p.Commentaires)
                .OnDelete(DeleteBehavior.ClientSetNull)
                .HasConstraintName("FK_Com_User");
        });

        modelBuilder.Entity<DonneeCapteur>(entity =>
        {
            entity.ToTable("DonneeCapteur", tb => tb.HasTrigger("verifeCapteurDonneeAlerte"));

            entity.Property(e => e.DateMesure).HasDefaultValueSql("(sysdatetime())");

            entity.HasOne(d => d.IdUtilisateurNavigation).WithMany(p => p.DonneeCapteurs).HasConstraintName("FK_Donnee_User");
        });

        modelBuilder.Entity<Produit>(entity =>
        {
            entity.HasOne(d => d.IdUtilisateurNavigation).WithMany(p => p.Produits).HasConstraintName("FK_Produit_User");
        });

        modelBuilder.Entity<Ticket>(entity =>
        {
            entity.ToTable("Ticket", tb => tb.HasTrigger("Ticket_Resolution"));

            entity.Property(e => e.DateCreation).HasDefaultValueSql("(sysdatetime())");

            entity.HasOne(d => d.IdUtilisateurNavigation).WithMany(p => p.Tickets).HasConstraintName("FK_Ticket_User");
        });

        modelBuilder.Entity<Utilisateur>(entity =>
        {
            entity.Property(e => e.DateCreation).HasDefaultValueSql("(sysdatetime())");
            entity.Property(e => e.Sel).HasDefaultValueSql("(newid())");
        });

        modelBuilder.Entity<VAlerte>(entity =>
        {
            entity.ToView("v_Alertes");
        });

        modelBuilder.Entity<VCommentaire>(entity =>
        {
            entity.ToView("v_Commentaires");
        });

        modelBuilder.Entity<VMesuresBase>(entity =>
        {
            entity.ToView("v_MesuresBase");

            entity.Property(e => e.IdDonneeCapteur).ValueGeneratedOnAdd();
        });

        modelBuilder.Entity<VTableauDeBord>(entity =>
        {
            entity.ToView("v_TableauDeBord");
        });

        modelBuilder.Entity<VTicketsAvecUser>(entity =>
        {
            entity.ToView("v_TicketsAvecUser");
        });

        OnModelCreatingPartial(modelBuilder);
    }

    partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
}
