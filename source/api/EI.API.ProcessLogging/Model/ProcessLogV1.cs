using EI.API.Service.Rest.Helpers.Model;
using System.ComponentModel.DataAnnotations;

namespace EI.API.ProcessLogging.Model;

public class ProcessLogV1 : BaseDto
{
    /// <summary>
    ///   The <see cref="ActivityTypeV1.Type">Activity Type</see> that this Process Log entry describes.
    /// </summary>
    [Required, MaxLength(50)]
    public string Type { get; set; } = default!;

    /// <summary>
    ///   The <see cref="ProcessStatusV1.Status">Process Status</see> of this Process Log entry.
    /// </summary>
    [Required, MaxLength(50)]
    public string Status { get; set; } = default!;

    /// <summary>
    ///  The UTC timestamp of when this process was started.
    /// </summary>
    public DateTime StartTimestamp { get; set; }

    /// <summary>
    ///   The UTC timestamp of the last time this Process Log had activity.
    /// </summary>
    public DateTime LastUpdatedTimestamp { get; set; }
}