using System.ComponentModel.DataAnnotations;

namespace EI.API.ProcessLogging.Model;

public class ProcessLogMessageV2 : ProcessLogMessageV1
{
    /// <summary>
    ///   The ID of the <see cref="FileProcessLogV1"/> that this Message is associated with.
    /// </summary>
    public Guid? FileProcessLogId { get; set; }
}
