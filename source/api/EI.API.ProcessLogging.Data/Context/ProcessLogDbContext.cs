using EI.API.ProcessLogging.Data.Entities;
using Microsoft.EntityFrameworkCore;

namespace EI.API.ProcessLogging.Data.Context;

public partial class ProcessLogDbContext : DbContext
{
    public DbSet<MessageLevel> MessageLevels { get; set; } = default!;
    public DbSet<MessageLevelTranslation> MessageLevelTranslations { get; set; } = default!;

    public DbSet<ActivityType> ActivityTypes { get; set; } = default!;
    public DbSet<ActivityTypeTranslation> ActivityTypeTranslations { get; set; } = default!;

    public DbSet<ProcessStatus> ProcessStatuses { get; set; } = default!;
    public DbSet<ProcessStatusTranslation> ProcessStatusTranslations { get; set; } = default!;

    public DbSet<ProcessLog> ProcessLogs { get; set; } = default!;
    public DbSet<ProcessLogMessage> ProcessLogMessages { get; set; } = default!;
    public DbSet<FileProcessLog> FileProcessLogs { get; set; } = default!;

    public DbSet<X12Message> X12Messages { get; set; } = default!;
    public DbSet<X12Status> X12Statuses { get; set; } = default!;
    public DbSet<X12StatusTranslation> X12StatusTranslations { get; set; } = default!;
    public DbSet<X12Interchange> X12Interchanges { get; set; } = default!;
    public DbSet<X12FunctionalGroup> X12FunctionalGroups { get; set; } = default!;
    public DbSet<X12TransactionSet> X12TransactionSets { get; set; } = default!;
    public DbSet<FilePurpose> FilePurposes { get; set; } = default!;
    public DbSet<FilePurposeTranslation> FilePurposeTranslations { get; set; } = default!;

}
