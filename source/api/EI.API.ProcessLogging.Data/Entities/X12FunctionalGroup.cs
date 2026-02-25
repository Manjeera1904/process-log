using EI.API.Service.Data.Helpers.Model;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace EI.API.ProcessLogging.Data.Entities;

public class X12FunctionalGroup : BaseDatabaseEntity
{
    public Guid X12InterchangeId { get; set; }

    [Required, MaxLength(50), Column("X12Status")]
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

    [ForeignKey(nameof(X12InterchangeId))]
    public X12Interchange X12Interchange { get; set; } = default!;
}