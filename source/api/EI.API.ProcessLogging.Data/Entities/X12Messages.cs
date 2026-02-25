using EI.API.Service.Data.Helpers.Model;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace EI.API.ProcessLogging.Data.Entities;

public class X12Message : BaseDatabaseEntity
{
    public Guid X12InterchangeId { get; set; }
    public Guid? X12FunctionalGroupId { get; set; }
    public Guid? X12TransactionSetId { get; set; }

    [Required, MaxLength(50), Column("MessageLevel")]
    public string Level { get; set; } = default!;

    [Required, MaxLength(8192)]
    public string Message { get; set; } = default!;

    public DateTime MessageTimestamp { get; set; } = default!;

    [ForeignKey(nameof(X12InterchangeId))]
    public X12Interchange X12Interchange { get; set; } = default!;

    [ForeignKey(nameof(X12FunctionalGroupId))]
    public X12FunctionalGroup X12FunctionalGroup { get; set; } = default!;

    [ForeignKey(nameof(X12TransactionSetId))]
    public X12TransactionSet X12TransactionSet { get; set; } = default!;
}
