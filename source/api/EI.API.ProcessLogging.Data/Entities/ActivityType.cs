using EI.API.Service.Data.Helpers.Model;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace EI.API.ProcessLogging.Data.Entities;

public class ActivityType : BaseDatabaseEntityWithTranslation<ActivityTypeTranslation>
{
    [Required, MaxLength(50), Column("ActivityType")]
    public string Type { get; set; } = default!;

    [Column("Inbound")]
    public bool IsInbound { get; set; }

    [Column("Outbound")]
    public bool IsOutbound { get; set; }
}

public class ActivityTypeTranslation : BaseDatabaseTranslationsEntity<ActivityType>
{
    [Required]
    [MaxLength(250)]
    public string Name { get; set; } = default!;

    [MaxLength(8192)]
    public string? Description { get; set; }
}
