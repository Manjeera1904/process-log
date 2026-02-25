using EI.API.Service.Rest.Helpers.Model;
using System.ComponentModel.DataAnnotations;

namespace EI.API.ProcessLogging.Model;

/// <summary>
///   Describes the status of a <see cref="ProcessLogV1"/>, for example "In Progress", "Completed", "Failed", etc.
/// </summary>
public class ProcessStatusV1 : BaseTranslationDto
{
    /// <summary>
    ///   The <see cref="ProcessLogV1.Status">Process Status</see> of this Process Log entry.
    /// </summary>
    [Required, MaxLength(50)]
    public string Status { get; set; } = default!;

    /// <summary>
    ///   The name of the Status for the specified <see cref="BaseTranslationDto.CultureCode"/>.
    /// </summary>
    [Required, MaxLength(250)]
    public string Name { get; set; } = default!;

    /// <summary>
    ///   An optional description of the Status for the specified <see cref="BaseTranslationDto.CultureCode"/>.
    /// </summary>
    [MaxLength(8192)]
    public string? Description { get; set; }
}