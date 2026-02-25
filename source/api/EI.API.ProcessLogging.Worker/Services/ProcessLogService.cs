using EI.API.Cloud.Clients;
using EI.API.ProcessLogging.Data;
using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;

namespace EI.API.ProcessLogging.Worker.Services;

public interface IProcessLogService
{
    Task<ProcessLog> GetOrCreateProcessLogAsync(
        ProcessLogDbContext context,
        Guid processLogId,
        MessageHeader header,
        DateTime messageTimestamp,
        Guid? createdBy = null,
        string? messageType = null,
        string? updatedByOverride = null
    );
}

public class ProcessLogService : IProcessLogService
{
    private readonly ILogger<ProcessLogService> _logger;
    private readonly Dictionary<Guid, ProcessLog> _processLogCache = new();

    public ProcessLogService(ILogger<ProcessLogService> logger)
    {
        _logger = logger;
    }

    public async Task<ProcessLog> GetOrCreateProcessLogAsync(
        ProcessLogDbContext context,
        Guid processLogId,
        MessageHeader header,
        DateTime messageTimestamp,
        Guid? createdBy = null,
        string? messageType = null,
        string? updatedByOverride = null
    )
    {
        // Check in-memory cache first
        if (_processLogCache.TryGetValue(processLogId, out var cachedProcessLog))
        {
            _logger.LogDebug("Returning cached ProcessLog {ProcessLogId}", processLogId);
            return cachedProcessLog;
        }

        _logger.LogDebug("GetOrCreateProcessLogAsync {CorrelationId}", processLogId);

        var processLog = await context.ProcessLogs.FirstOrDefaultAsync(p => p.Id == processLogId);

        Guid? applicationId = null;

        if (
            !string.IsNullOrWhiteSpace(header.SendingApplicationId)
            && Guid.TryParse(header.SendingApplicationId, out var parsedGuid)
        )
        {
            applicationId = parsedGuid;
        }

        if (processLog == null)
        {
            var updatedBy =
                !string.IsNullOrWhiteSpace(updatedByOverride) ? updatedByOverride
                : !string.IsNullOrWhiteSpace(header.SendingApplication) ? header.SendingApplication
                : "Unknown";

            var activityTypeToUse =
                !string.IsNullOrWhiteSpace(messageType) ? messageType
                : !string.IsNullOrWhiteSpace(header.MessageType) ? header.MessageType
                : ProcessLogConstants.ActivityType.PayorContractAnalysis;

            processLog = new ProcessLog
            {
                Id = processLogId,
                Type = activityTypeToUse,
                Status = header.MessageStatus ?? ProcessLogConstants.ProcessStatus.New,
                StartTimestamp = messageTimestamp,
                LastUpdatedTimestamp = messageTimestamp,
                CreatedBy = updatedBy,
                UpdatedBy = updatedBy,
                CreatedByUserId = createdBy,
                ApplicationId = applicationId,
            };

            _logger.LogInformation(
                "Creating ProcessLog {ProcessLogId} with activityTypeToUse = {activityTypeToUse} ActivityType={ActivityType} MessageType={MessageType}",
                processLogId,
                activityTypeToUse,
                processLog.Type,
                header.MessageType
            );

            await context.ProcessLogs.AddAsync(processLog);
            //save immediately if it was just created (avoids FK violations from concurrent messages)
            await context.SaveChangesAsync();
            _logger.LogInformation("Created and saved new ProcessLog {ProcessLogId}", processLogId);
        }
        else
        {
            if (
                !string.IsNullOrEmpty(header.MessageStatus)
                && (messageTimestamp > processLog.LastUpdatedTimestamp)
            )
            {
                processLog.Status = header.MessageStatus;
                processLog.LastUpdatedTimestamp = messageTimestamp;
                processLog.UpdatedBy = header.SendingApplication ?? processLog.UpdatedBy;
                processLog.ApplicationId = applicationId;
                context.ProcessLogs.Update(processLog);
                _logger.LogInformation(
                    "Updated existing ProcessLog {ProcessLogId} status to {Status}",
                    processLogId,
                    processLog.Status
                );
            }
            else
            {
                _logger.LogInformation(
                    "Skipped updating ProcessLog {ProcessLogId} because incoming message timestamp {MessageTimestamp} is not newer than existing {ExistingTimestamp}",
                    processLogId,
                    messageTimestamp,
                    processLog.LastUpdatedTimestamp
                );
            }
        }

        _processLogCache[processLogId] = processLog;
        return processLog;
    }
}
