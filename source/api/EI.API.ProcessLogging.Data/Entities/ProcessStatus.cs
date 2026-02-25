using EI.API.Service.Data.Helpers.Model;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace EI.API.ProcessLogging.Data.Entities;

public class ProcessStatus : BaseDatabaseEntityWithTranslation<ProcessStatusTranslation>
{
    [Required, MaxLength(50), Column("ProcessStatus")]
    public string Status { get; set; } = default!;
}

public class ProcessStatusTranslation : BaseDatabaseTranslationsEntity<ProcessStatus>
{
    [Required]
    [MaxLength(250)]
    public string Name { get; set; } = default!;

    [MaxLength(8192)]
    public string? Description { get; set; }
}
