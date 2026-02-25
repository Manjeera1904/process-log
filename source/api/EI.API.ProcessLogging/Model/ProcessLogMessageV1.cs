using EI.API.Service.Rest.Helpers.Model;
using System.ComponentModel.DataAnnotations;

namespace EI.API.ProcessLogging.Model;

/// <summary>
///   Messages describing the actions that occurred while the <see cref="ProcessLogV1">Process</see> was active
/// </summary>
public class ProcessLogMessageV1 : BaseDto
{
    /// <summary>
    ///   The ID of the <see cref="ProcessLogV1"/> that this Message is associated with.
    /// </summary>
    public Guid ProcessLogId { get; set; }

    /// <summary>
    ///    The <see cref="MessageLevelV1.Level">Level</see> of message, indicating the severity or importance of the message.
    /// </summary>
    [Required, MaxLength(50)]
    public string Level { get; set; } = default!;

    /// <summary>
    ///   The message text.
    /// </summary>
    [Required, MaxLength(8192)]
    public string Message { get; set; } = default!;

    /// <summary>
    ///   The UTC timestamp of when this message was created.
    /// </summary>
    public DateTime MessageTimestamp { get; set; }
}