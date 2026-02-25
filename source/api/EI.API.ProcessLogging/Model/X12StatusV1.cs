using EI.API.Service.Rest.Helpers.Model;
using System.ComponentModel.DataAnnotations;

namespace EI.API.ProcessLogging.Model;

/// <summary>
///   Describes the status of a <see cref="X12InterchangeV1"/>, <see cref="X12FunctionalGroupV1"/>, or
///   <see cref="X12TransactionSetV1"/>, for example "In Progress", "Completed", "Failed", etc.
/// </summary>
public class X12StatusV1 : BaseTranslationDto
{
    /// <summary>
    ///   The Status of the X12 entity.
    ///   <seealso cref="X12InterchangeV1.Status"/>
    ///   <seealso cref="X12FunctionalGroupV1.Status"/>
    ///   <seealso cref="X12TransactionSetV1.Status"/>
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