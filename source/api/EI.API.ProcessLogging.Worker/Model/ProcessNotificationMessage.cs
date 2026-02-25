using System.Text.Json;
using System.Text.Json.Serialization;

namespace EI.API.ProcessLogging.Worker.Model;

public class ProcessNotificationMessage
{
    public DateTime? ReceiveTimestamp { get; set; }

    [JsonPropertyName("Messages")]
    public List<MessageEntry>? Messages { get; set; }

    [JsonPropertyName("Files")]
    public List<FileEntry>? Files { get; set; }

    [JsonPropertyName("X12Interchanges")]
    public List<X12Interchange>? X12Interchanges { get; set; }

    [JsonPropertyName("X12FunctionalGroups")]
    public List<X12FunctionalGroup>? X12FunctionalGroups { get; set; }

    [JsonPropertyName("X12TransactionSets")]
    public List<X12TransactionSet>? X12TransactionSets { get; set; }

    // Allow other undefined props to arrive (for future compatibility)
    [JsonExtensionData]
    public Dictionary<string, JsonElement>? AdditionalData { get; set; }
}

public class MessageEntry
{
    public string? MessageLevel { get; set; }
    public string? Message { get; set; }
}

public class FileEntry
{
    public string? FileName { get; set; }
    public string? FilePath { get; set; }
    public int? FileSize { get; set; }
    public string? FileType { get; set; }
    public string? FileHash { get; set; }
    public string? Status { get; set; }
    public string FilePurpose { get; set; } = string.Empty;
    public List<MessageEntry>? Messages { get; set; }
}

// Placeholders EDI (TBD)
public class X12Interchange
{
    public string? ControlNumber { get; set; }
    public string? SenderId { get; set; }
    public string? ReceiverId { get; set; }
    public List<X12FunctionalGroup>? FunctionalGroups { get; set; }
}

public class X12FunctionalGroup
{
    public string? ControlNumber { get; set; }
    public string? TransactionType { get; set; }
    public List<X12TransactionSet>? TransactionSets { get; set; }
}

public class X12TransactionSet
{
    public string? TransactionSetId { get; set; }
    public string? ControlNumber { get; set; }
    public string? Description { get; set; }
}
