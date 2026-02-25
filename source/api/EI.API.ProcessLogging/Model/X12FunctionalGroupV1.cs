using EI.API.Service.Rest.Helpers.Model;
using System.ComponentModel.DataAnnotations;

namespace EI.API.ProcessLogging.Model;

/// <summary>
///   Represents an EDI X12 Functional Group, which is a collection of one or more
///   <see cref="X12TransactionSetV1">EDI X12 Transaction Sets</see>
///   within an <see cref="X12InterchangeV1">EDI X12 Interchange</see>.
/// </summary>
public class X12FunctionalGroupV1 : BaseDto
{
    public Guid X12InterchangeId { get; set; }

    [Required, MaxLength(50)]
    public string Status { get; set; } = default!;

    [MaxLength(02)]
    public string? FunctionalIdentifierCode { get; set; }

    [MaxLength(15)]
    public string? ApplicationSenderCode { get; set; }

    [MaxLength(15)]
    public string? ApplicationReceiverCode { get; set; }

    [MaxLength(08)]
    public string? Date { get; set; }

    [MaxLength(08)]
    public string? Time { get; set; }

    [MaxLength(09)]
    public string? GroupControlNumber { get; set; }

    [MaxLength(02)]
    public string? ResponsibleAgencyCode { get; set; }

    [MaxLength(12)]
    public string? VersionReleaseIndustryIdentifierCode { get; set; }
}