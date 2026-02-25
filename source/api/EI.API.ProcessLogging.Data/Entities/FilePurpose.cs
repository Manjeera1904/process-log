using EI.API.Service.Data.Helpers.Model;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace EI.API.ProcessLogging.Data.Entities;

public class FilePurpose : BaseDatabaseEntityWithTranslation<FilePurposeTranslation>
{
    [Required, MaxLength(50), Column("PurposeName")]
    public string PurposeName { get; set; } = string.Empty;

    public bool IsSystemGenerated { get; set; }

    public bool IsDownloadable { get; set; }
}

public class FilePurposeTranslation : BaseDatabaseTranslationsEntity<FilePurpose>
{
    [Required]
    public string Name { get; set; } = string.Empty;

    [MaxLength(8192)]
    public string? Description { get; set; }
}
