using EI.API.Service.Data.Helpers.Model;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace EI.API.ProcessLogging.Data.Entities;

public class ProcessLog : BaseDatabaseEntity
{
    [Required, MaxLength(50), Column("ActivityType")]
    public string Type { get; set; } = default!;
    [Required, MaxLength(50), Column("ProcessStatus")]
    public string Status { get; set; } = default!;

    public DateTime StartTimestamp { get; set; } = default!;
    public DateTime LastUpdatedTimestamp { get; set; } = default!;
    [MaxLength(120)]
    public string? CreatedBy { get; set; }
    public Guid? CreatedByUserId { get; set; }
    public Guid? ApplicationId { get; set; }
    public ICollection<FileProcessLog>? FileProcessLogs { get; set; }
}