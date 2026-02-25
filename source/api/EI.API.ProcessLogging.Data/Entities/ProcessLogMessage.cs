using EI.API.Service.Data.Helpers.Model;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace EI.API.ProcessLogging.Data.Entities;

public class ProcessLogMessage : BaseDatabaseEntity
{
    public Guid ProcessLogId { get; set; }

    [Required, MaxLength(50), Column("MessageLevel")]
    public string Level { get; set; } = default!;

    [Required, MaxLength(8192)]
    public string Message { get; set; } = default!;

    public DateTime MessageTimestamp { get; set; } = default!;

    [ForeignKey(nameof(ProcessLogId))]
    public ProcessLog ProcessLog { get; set; } = default!;

    public Guid? FileProcessLogId { get; set; }

    [ForeignKey(nameof(FileProcessLogId))]
    public FileProcessLog? FileProcessLog { get; set; }
}
