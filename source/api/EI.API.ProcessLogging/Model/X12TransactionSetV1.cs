using EI.API.Service.Rest.Helpers.Model;
using System.ComponentModel.DataAnnotations;

namespace EI.API.ProcessLogging.Model;

/// <summary>
///   Represents an EDI X12 Functional Group, which is a collection of one or more
///   <see cref="X12TransactionSetV1">EDI X12 Transaction Sets</see>
///   within an <see cref="X12InterchangeV1">EDI X12 Interchange</see>.
/// </summary>
public class X12TransactionSetV1 : BaseDto
{
    public Guid X12FunctionalGroupId { get; set; }

    [Required, MaxLength(50)]
    public string Status { get; set; } = default!;

    [MaxLength(3)]
    public string? TransactionSetIdentifierCode { get; set; }

    [MaxLength(9)]
    public string? TransactionSetControlNumber { get; set; }
}