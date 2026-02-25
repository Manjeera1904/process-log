using EI.API.Service.Rest.Helpers.Model;
using System.ComponentModel.DataAnnotations;

namespace EI.API.ProcessLogging.Model;

/// <summary>
///   Represents an EDI X12 Functional Group, which is a collection of one or more
///   <see cref="X12TransactionSetV1">EDI X12 Transaction Sets</see>
///   within an <see cref="X12InterchangeV1">EDI X12 Interchange</see>.
/// </summary>
public class X12InterchangeV1 : BaseDto
{
    public Guid FileProcessLogId { get; set; }

    [Required, MaxLength(50)]
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
}