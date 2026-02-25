using EI.API.Service.Data.Helpers.Model;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace EI.API.ProcessLogging.Data.Entities;

public class X12Status : BaseDatabaseEntityWithTranslation<X12StatusTranslation>
{
    [Required, MaxLength(50), Column("X12Status")]
    public string Status { get; set; } = default!;
}

public class X12StatusTranslation : BaseDatabaseTranslationsEntity<X12Status>
{
    [Required]
    [MaxLength(250)]
    public string Name { get; set; } = default!;

    [MaxLength(8192)]
    public string? Description { get; set; }
}
