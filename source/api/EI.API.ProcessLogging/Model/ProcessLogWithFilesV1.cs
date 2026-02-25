using EI.API.ProcessLogging.Model;

public class ProcessLogWithFilesV1 : ProcessLogV1
{
    /// <summary>
    /// List of files associated with this process log.
    /// </summary>
    public List<FileProcessLogV1>? Files { get; set; }

    /// <summary>
    /// Count of files associated with this process log.
    /// </summary>
    public int FileCount { get; set; }
}
