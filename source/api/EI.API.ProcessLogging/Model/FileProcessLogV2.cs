using System.ComponentModel.DataAnnotations;

namespace EI.API.ProcessLogging.Model;

public class FileProcessLogV2 : FileProcessLogV1
{
    /// <summary>
    ///   The lookup name of the purpose of this file (FK to FilePurpose).
    /// </summary>
    [Required, MaxLength(50)]
    public string PurposeName { get; set; } = default!;

    /// <summary>
    ///   The lookup status of this file (FK to ProcessStatus).
    /// </summary>
    [Required, MaxLength(50)]
    public string ProcessStatus { get; set; } = default!;
}
