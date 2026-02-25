using EI.API.Service.Rest.Helpers.Model;
using System.ComponentModel.DataAnnotations;

namespace EI.API.ProcessLogging.Model;

/// <summary>
///   A specific variant of a <see cref="ProcessLogV1"/> that is used to log the processing of a file.
/// </summary>
public class FileProcessLogV1 : BaseDto
{
    /// <summary>
    ///   The ID of the <see cref="ProcessLogV1"/> that this File Process Log is associated with.
    /// </summary>
    public Guid ProcessLogId { get; set; }

    /// <summary>
    ///   The name of the file that this <see cref="ProcessLogV1">Process Log</see> is associated with.
    /// </summary>
    [Required, MaxLength(1000)]
    public string FileName { get; set; } = default!;

    /// <summary>
    ///   The path of the file that this <see cref="ProcessLogV1">Process Log</see> is associated with, typically
    ///   a URI to the file in a Storage Account.
    /// </summary>
    [Required, MaxLength(1000)]
    public string FilePath { get; set; } = default!;

    /// <summary>
    ///   The (optional) size of the file in bytes.
    /// </summary>
    public int? FileSize { get; set; }

    /// <summary>
    ///   The (optional) SHA3-256 hash of the file, used for file integrity checking.
    /// </summary>
    [MaxLength(500)]
    public string? FileHash { get; set; }
}
