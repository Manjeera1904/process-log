using EI.API.Service.Data.Helpers.Model;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace EI.API.ProcessLogging.Data.Entities;

public class X12Interchange : BaseDatabaseEntity
{
    public Guid FileProcessLogId { get; set; }

    [Required, MaxLength(50), Column("X12Status")]
    public string Status { get; set; } = default!;

    [MaxLength(10)]
    public string? InterchangeSenderIdQualifier { get; set; }

    [MaxLength(15)]
    public string? InterchangeSenderId { get; set; }

    [MaxLength(10)]
    public string? InterchangeReceiverIdQualifier { get; set; }

    [MaxLength(15)]
    public string? InterchangeReceiverId { get; set; }

    [MaxLength(06)]
    public string? InterchangeDate { get; set; }

    [MaxLength(04)]
    public string? InterchangeTime { get; set; }

    [MaxLength(04)]
    public string? RepetitionSeparator { get; set; }

    [MaxLength(05)]
    public string? InterchangeControlVersionNumber { get; set; }

    [MaxLength(09)]
    public string? InterchangeControlNumber { get; set; }

    [MaxLength(01)]
    public string? AcknowledgementRequested { get; set; }

    [MaxLength(01)]
    public string? UsageIndicator { get; set; }

    [MaxLength(01)]
    public string? ComponentElementSeparator { get; set; }

    [ForeignKey(nameof(FileProcessLogId))]
    public FileProcessLog FileProcessLog { get; set; } = default!;
}