using EI.API.Service.Rest.Helpers.Model;
using System.ComponentModel.DataAnnotations;

namespace EI.API.ProcessLogging.Model;

/// <summary>
///   Represents the severity of a message, used to categorize messages and determine how they should be
///   displayed and interpreted.
/// </summary>
public class MessageLevelV1 : BaseTranslationDto
{
    /// <summary>
    ///   A unique code that identifies the level, used for readability and programmatic access.
    /// </summary>
    [Required, MaxLength(50)]
    public string Level { get; set; } = default!;

    /// <summary>
    ///   The name of the Message Level for the specified <see cref="BaseTranslationDto.CultureCode"/>.
    /// </summary>
    [Required, MaxLength(250)]
    public string Name { get; set; } = default!;

    /// <summary>
    ///   An optional description of the Message Level for the specified <see cref="BaseTranslationDto.CultureCode"/>.
    /// </summary>
    [MaxLength(8192)]
    public string? Description { get; set; }
}