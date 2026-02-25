using EI.API.ProcessLogging.Data.Entities;
using EI.API.Service.Data.Helpers.Entities;
using EI.API.Service.Data.Helpers.Model;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using Microsoft.Extensions.Configuration;

namespace EI.API.ProcessLogging.Data.Context;

public partial class ProcessLogDbContext
{
    public static string ConnectionStringName => "EIProcessLog";

    protected readonly string _connectionString = default!;

    public ProcessLogDbContext(IConfiguration configuration)
        : this(configuration.GetConnectionString(ConnectionStringName) ?? string.Empty) { }

    public ProcessLogDbContext(string connectionString)
    {
        if (string.IsNullOrWhiteSpace(connectionString))
            throw new ArgumentNullException(nameof(connectionString));

        _connectionString = connectionString;
    }

#if DEBUG
    public ProcessLogDbContext()
    {
        // Empty constructor is necessary for creating migrations
        // Fix warning CS8618 for non-nullable field
        _connectionString = null!;
    }
#endif

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        base.OnConfiguring(optionsBuilder);

        optionsBuilder.UseSqlServer(_connectionString);
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        SetupCustomKeysAndIndicies(modelBuilder);

        foreach (var tableType in modelBuilder.Model.GetEntityTypes())
        {
            var clrType = tableType.ClrType;

            var entityBuilder = modelBuilder.Entity(clrType);
            var table = entityBuilder.ToTable(
                tableType.GetTableName()
                    ?? throw new Exception(
                        $"Could not derive table name for type {clrType.FullName}"
                    ),
                tableBuilder =>
                {
                    SetupPrimaryKeys(modelBuilder, entityBuilder, tableBuilder, clrType);
                    SetupTemporalHistory(modelBuilder, entityBuilder, tableBuilder, clrType);
                }
            );
        }

        // Disable cascade delete for all relationships
        foreach (
            var relationship in modelBuilder
                .Model.GetEntityTypes()
                .SelectMany(e => e.GetForeignKeys())
        )
        {
            relationship.DeleteBehavior = DeleteBehavior.Restrict;
        }

        OnModelCreatingSeedData(modelBuilder);
    }

    partial void OnModelCreatingSeedData(ModelBuilder modelBuilder);

    private void SetupCustomKeysAndIndicies(ModelBuilder modelBuilder)
    {
        #region ActivityType: set up custom alternate key and FK that uses it
        modelBuilder.Entity<ActivityType>().HasAlternateKey(ak => ak.Type);

        modelBuilder
            .Entity<ProcessLog>()
            .HasOne<ActivityType>()
            .WithMany()
            .HasForeignKey(fk => fk.Type)
            .HasPrincipalKey(ak => ak.Type);
        #endregion ActivityType: set up custom alternate key and FKs that use it

        #region ProcessStatus: set up custom alternate key and FK that uses it
        modelBuilder.Entity<ProcessStatus>().HasAlternateKey(ak => ak.Status);

        modelBuilder
            .Entity<ProcessLog>()
            .HasOne<ProcessStatus>()
            .WithMany()
            .HasForeignKey(fk => fk.Status)
            .HasPrincipalKey(ak => ak.Status);
        #endregion ProcessStatus: set up custom alternate key and FKs that use it

        #region MessageLevel: set up custom alternate key and FK that uses it
        modelBuilder.Entity<MessageLevel>().HasAlternateKey(ak => ak.Level);

        modelBuilder
            .Entity<ProcessLogMessage>()
            .HasOne<MessageLevel>()
            .WithMany()
            .HasForeignKey(fk => fk.Level)
            .HasPrincipalKey(ak => ak.Level);

        modelBuilder
            .Entity<X12Message>()
            .HasOne<MessageLevel>()
            .WithMany()
            .HasForeignKey(fk => fk.Level)
            .HasPrincipalKey(ak => ak.Level);
        #endregion MessageLevel: set up custom alternate key and FKs that uses it

        #region X12Status: set up custom alternate key and FKs that uses it
        modelBuilder.Entity<X12Status>().HasAlternateKey(ak => ak.Status);

        modelBuilder
            .Entity<X12Interchange>()
            .HasOne<X12Status>()
            .WithMany()
            .HasForeignKey(fk => fk.Status)
            .HasPrincipalKey(ak => ak.Status);

        modelBuilder
            .Entity<X12FunctionalGroup>()
            .HasOne<X12Status>()
            .WithMany()
            .HasForeignKey(fk => fk.Status)
            .HasPrincipalKey(ak => ak.Status);

        modelBuilder
            .Entity<X12TransactionSet>()
            .HasOne<X12Status>()
            .WithMany()
            .HasForeignKey(fk => fk.Status)
            .HasPrincipalKey(ak => ak.Status);
        #endregion X12Status: set up custom alternate key and FKs that uses it

        #region FilePurpose: set up custom alternate key and FK that uses it
        modelBuilder.Entity<FilePurpose>()
            .HasAlternateKey(fp => fp.PurposeName);

        modelBuilder.Entity<FileProcessLog>()
            .HasOne(fpl => fpl.Purpose)
            .WithMany()
            .HasForeignKey(fpl => fpl.PurposeName)
            .HasPrincipalKey(fp => fp.PurposeName);
        #endregion FilePurpose: set up custom alternate key and FKs that uses it

        #region FileProcessLog ProcessStatus: FK using ProcessStatus.Status
        modelBuilder.Entity<FileProcessLog>()
            .HasOne(fpl => fpl.Status)
            .WithMany()
            .HasForeignKey(fpl => fpl.ProcessStatus)
            .HasPrincipalKey(ps => ps.Status);
        #endregion FileProcessLog ProcessStatus

        #region FileProcessLog (index)
        modelBuilder.Entity<FileProcessLog>()
            .HasIndex(f => new
            {
                f.ProcessLogId,
                f.FileName
            })
            .IsUnique();
        #endregion FileProcessLog (index)
    }

    private void SetupPrimaryKeys(
        ModelBuilder modelBuilder,
        EntityTypeBuilder entityBuilder,
        TableBuilder tableBuilder,
        Type clrType
    )
    {
        if (typeof(IDatabaseTranslationsEntity).IsAssignableFrom(clrType))
        {
            var translatedTableName = clrType.Name[..^"Translation".Length];
            var translatedTablePkCol = $"{translatedTableName}Id";

            entityBuilder.Property(nameof(IDatabaseEntity.Id)).HasColumnName(translatedTablePkCol);
        }
        else if (typeof(BaseDatabaseEntity).IsAssignableFrom(clrType))
        {
            entityBuilder
                .Property(nameof(BaseDatabaseEntity.Id))
                .HasColumnName($"{clrType.Name!}Id")
                .IsRequired();
        }
    }

    private void SetupTemporalHistory(
        ModelBuilder modelBuilder,
        EntityTypeBuilder entityBuilder,
        TableBuilder tableBuilder,
        Type clrType
    )
    {
        if (clrType == typeof(FilePurpose) || clrType == typeof(FilePurposeTranslation))
            return;

        tableBuilder.IsTemporal(ttBuilder =>
        {
            ttBuilder.HasPeriodStart(nameof(EntityHistory<ActivityType>.ValidFrom));
            ttBuilder.HasPeriodEnd(nameof(EntityHistory<ActivityType>.ValidTo));
        });
    }
}
