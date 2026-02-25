using EI.API.Service.Data.Helpers.Model;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace EI.API.ProcessLogging.Data.Entities;

public class X12TransactionSet : BaseDatabaseEntity
{
    public Guid X12FunctionalGroupId { get; set; }

    [Required, MaxLength(50), Column("X12Status")]
    public string Status { get; set; } = default!;

    [MaxLength(3)]
    public string? TransactionSetIdentifierCode { get; set; }

    [MaxLength(9)]
    public string? TransactionSetControlNumber { get; set; }

    [ForeignKey(nameof(X12FunctionalGroupId))]
    public X12FunctionalGroup X12FunctionalGroup { get; set; } = default!;
}
