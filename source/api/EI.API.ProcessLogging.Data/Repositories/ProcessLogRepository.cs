using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Models;
using EI.API.Service.Data.Helpers.Platform;
using EI.API.Service.Data.Helpers.Repository;
using Microsoft.EntityFrameworkCore;

namespace EI.API.ProcessLogging.Data.Repositories;

public interface IProcessLogRepository : IReadWriteRepository<ProcessLog>
{
    Task<PagedResult<ProcessLog>> SearchAsync(ProcessLogSearch request);
}

public class ProcessLogRepository(IDatabaseClientFactory dbContextFactory, Guid clientId)
    : BaseRepository<ProcessLogDbContext, ProcessLog>(dbContextFactory, clientId), IProcessLogRepository
{
    public async Task<PagedResult<ProcessLog>> SearchAsync(ProcessLogSearch request)
    {
        return await Exec(async (_, entitySet) =>
        {
            var query = entitySet
    .Include(x => x.FileProcessLogs) // Include files
    .AsQueryable();

            // Activity Type Filter (case-insensitive)
            if (!string.IsNullOrWhiteSpace(request.ActivityType))
            {
                var typeFilter = request.ActivityType.ToLower();
                query = query.Where(x => x.Type.ToLower() == typeFilter);
            }

            // Status Filter (case-insensitive, only if provided)
            if (request.Statuses != null && request.Statuses.Any())
            {
                var statusFilter = request.Statuses.Select(s => s.ToLower()).ToList();
                query = query.Where(x => statusFilter.Contains(x.Status.ToLower()));
            }

            // Date Range (only apply if request.DateRange is given)
            if (!string.IsNullOrWhiteSpace(request.DateRange))
            {
                var (fromDate, toDate) = GetDateRange(request.DateRange, request.TimeZone);

                query = query.Where(x =>
                    (x.StartTimestamp >= fromDate && x.StartTimestamp <= toDate) ||
                    (x.LastUpdatedTimestamp >= fromDate && x.LastUpdatedTimestamp <= toDate));
            }

            // Sorting
            query = request.SortBy switch
            {
                "Type" => request.SortDirection == "asc"
                    ? query.OrderBy(x => x.Type)
                    : query.OrderByDescending(x => x.Type),
                _ => request.SortDirection == "asc"
                    ? query.OrderBy(x => x.StartTimestamp)
                    : query.OrderByDescending(x => x.StartTimestamp)
            };

            // Total Count (after filters)
            var totalCount = await query.CountAsync();

            // Pagination 
            var items = await query
                .Skip(Math.Max(0, (request.PageNumber - 1) * request.PageSize))
                .Take(request.PageSize)
                .ToListAsync();

            return new PagedResult<ProcessLog>
            {
                Items = items,
                TotalCount = totalCount,
                PageNumber = request.PageNumber,
                PageSize = request.PageSize
            };
        });
    }

    // Add this helper method to the same class
    private (DateTime fromDate, DateTime toDate) GetDateRange(string dateRange, string timeZone)
    {
        // Ignore time zone and always use UTC
        var nowUtc = DateTime.UtcNow;

        return dateRange switch
        {
            "Last7Days" => (nowUtc.AddDays(-7), nowUtc),
            "Last14Days" => (nowUtc.AddDays(-14), nowUtc),
            "Last30Days" => (nowUtc.AddDays(-30), nowUtc),
            _ => (nowUtc.Date, nowUtc)
        };
    }

    public override async Task<ProcessLog> UpdateAsync(ProcessLog entity)
    {
        var (isStatusChange, existing) = await IsStatusChangeUpdate(entity);
        if (isStatusChange)
        {
            await LogStatusChange(entity, existing!);
        }

        return await base.UpdateAsync(entity);
    }

    protected virtual async Task<(bool IsStatusChange, ProcessLog? Existing)> IsStatusChangeUpdate(ProcessLog entity)
        => await Exec(async (dbContext, entitySet) =>
        {
            // If the entity is attached, get the original value, otherwise go to the database for the "original"
            var entry = dbContext.ChangeTracker.Entries<ProcessLog>().FirstOrDefault(e => e.Entity.Id == entity.Id);
            if (entry == null)
            {
                // The entry is detached, so read it from the database
                var existing = await entitySet.AsNoTracking().FirstOrDefaultAsync(e => e.Id == entity.Id);
                var isStatusChange = existing != null && existing.Status != entity.Status;
                return (isStatusChange, existing);
            }
            else
            {
                var originalStatus = entry.OriginalValues[nameof(ProcessLog.Status)]?.ToString();
                var currentStatus = entity.Status;
                var isStatusChange = originalStatus != currentStatus;
                return (isStatusChange, entry.Entity);
            }
        });

    protected virtual async Task LogStatusChange(ProcessLog entity, ProcessLog existing)
    {
        var statusLog = new ProcessLogMessage
        {
            Id = Guid.NewGuid(),
            ProcessLogId = entity.Id,
            Level = ProcessLogConstants.MessageLevel.Status,
            Message = $"Status changed from {existing.Status} to {entity.Status}",
            UpdatedBy = entity.UpdatedBy,
            MessageTimestamp = DateTime.UtcNow,
        };

        var messageRepository = GetMessageRepository();
        _ = await messageRepository.InsertAsync(statusLog);
    }

    protected virtual IProcessLogMessageRepository GetMessageRepository()
    {
        var messageRepository = new ProcessLogMessageRepository(_dbContextFactory, _clientId);
        return messageRepository;
    }

    protected override string DataSourceKey => ProcessLogDbContext.ConnectionStringName;
}