using EI.API.Service.Data.Helpers.Model;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace EI.API.ProcessLogging.Data.Entities;

public class MessageLevel : BaseDatabaseEntityWithTranslation<MessageLevelTranslation>
{
    [Required, MaxLength(50), Column("MessageLevel")]
    public string Level { get; set; } = default!;
}

public class MessageLevelTranslation : BaseDatabaseTranslationsEntity<MessageLevel>
{
    [Required]
    [MaxLength(250)]
    public string Name { get; set; } = default!;

    [MaxLength(8192)]
    public string? Description { get; set; }
}
