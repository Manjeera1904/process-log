using EI.API.Service.Data.Helpers.Model;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace EI.API.ProcessLogging.Data.Entities;

public class FileProcessLog : BaseDatabaseEntity
{
    public FileProcessLog()
    {
        // REQUIRED DEFAULTS (V1 cannot send these, DB requires them. Useful in POST/PUT). Adding same defaults we added in the migration.
        PurposeName ??= "Originating Contract";
        ProcessStatus ??= "New";
    }

    public Guid ProcessLogId { get; set; }

    [Required, MaxLength(1000)]
    public string FileName { get; set; } = default!;

    [Required, MaxLength(1000)]
    public string FilePath { get; set; } = default!;

    public int? FileSize { get; set; }

    [MaxLength(500)]
    public string? FileHash { get; set; }

    [ForeignKey(nameof(ProcessLogId))]
    public ProcessLog ProcessLog { get; set; } = default!;

    [Required, MaxLength(50)]
    public string PurposeName { get; set; } = default!;

    [ForeignKey(nameof(PurposeName))]
    public FilePurpose Purpose { get; set; } = default!;

    [Required, MaxLength(50)]
    public string ProcessStatus { get; set; } = default!;

    [ForeignKey(nameof(ProcessStatus))]
    public ProcessStatus Status { get; set; } = default!;
}
