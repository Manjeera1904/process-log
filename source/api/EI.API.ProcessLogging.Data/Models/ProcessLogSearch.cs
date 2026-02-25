using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace EI.API.ProcessLogging.Data.Models;
public class ProcessLogSearch
{
    [MaxLength(50)]
    public string? ActivityType { get; set; }
    public List<string> Statuses { get; set; } = new();
    public string DateRange { get; set; } = "Today";
    public string SortBy { get; set; } = "StartTimestamp";
    public string SortDirection { get; set; } = "desc";
    [Range(1, int.MaxValue)]
    public int PageNumber { get; set; } = 1;
    [Range(1, 100)]
    public int PageSize { get; set; } = 20;
    [MaxLength(50)]
    public string TimeZone { get; set; } = "UTC";
}

public class PagedResult<T>
{
    public List<T>? Items { get; set; }
    public int TotalCount { get; set; }
    public int PageNumber { get; set; }
    public int PageSize { get; set; }
}
