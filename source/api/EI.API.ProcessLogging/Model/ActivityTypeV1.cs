using EI.API.Service.Rest.Helpers.Model;
using System.ComponentModel.DataAnnotations;

namespace EI.API.ProcessLogging.Model;

/// <summary>
///   An Activity Type defines a specific type of process that can be logged by the Process Logging application.
///   Examples of Activity Types could include "Receive File", "Send File", "Perform FHIR Call", etc.
/// </summary>
public class ActivityTypeV1 : BaseTranslationDto
{
    /// <summary>
    ///   A unique code that identifies the type, used for readability and programmatic access.
    /// </summary>
    [Required, MaxLength(50)]
    public string Type { get; set; } = default!;

    /// <summary>
    ///   Flag that indicates that the activity was triggered by an external actor, for example an external system
    ///   pushing a file to an application on the platform, or making an API call to the platform.
    /// </summary>
    public bool IsInbound { get; set; }

    /// <summary>
    ///   Flag that indicates that the activity was triggered by an application on the platform, for example the
    ///   application exporting a file, or making an API call to an external system.
    /// </summary>
    public bool IsOutbound { get; set; }

    /// <summary>
    ///   The name of the Activity Type for the specified <see cref="BaseTranslationDto.CultureCode"/>.
    /// </summary>
    [Required, MaxLength(250)]
    public string Name { get; set; } = default!;

    /// <summary>
    ///   An optional description of the Activity Type for the specified <see cref="BaseTranslationDto.CultureCode"/>.
    /// </summary>
    [MaxLength(8192)]
    public string? Description { get; set; }
}