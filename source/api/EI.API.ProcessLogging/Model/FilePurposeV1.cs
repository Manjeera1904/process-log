using EI.API.Service.Rest.Helpers.Model;
using System.ComponentModel.DataAnnotations;

namespace EI.API.ProcessLogging.Model;

public class FilePurposeV1 : BaseTranslationDto
{
    [Required, MaxLength(50)]
    public string PurposeName { get; set; } = default!;

    public bool IsSystemGenerated { get; set; }

    [Required, MaxLength(250)]
    public string Name { get; set; } = default!;

    [MaxLength(8192)]
    public string? Description { get; set; }
}
