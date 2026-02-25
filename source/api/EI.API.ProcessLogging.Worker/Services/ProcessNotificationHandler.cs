using EI.API.Cloud.Clients;
using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Worker.Model;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;

namespace EI.API.ProcessLogging.Worker.Services;

public interface IProcessNotificationHandler
{
    Task HandleAsync(MessageHeader header, ProcessNotificationMessage message, Guid clientId, Guid processLogId);
}

public class ProcessNotificationHandler : IProcessNotificationHandler
{
    private readonly IMessageReceiverServices _services;
    private readonly IProcessLogService _processLogService;
    private readonly FileLogProcessor _fileProcessor;
    private readonly MessageLogProcessor _messageProcessor;
    private readonly ILogger<ProcessNotificationHandler> _logger;
    private readonly ProcessNotificationEventHelper _eventHelper;
    public ProcessNotificationHandler(
          IMessageReceiverServices services,
          IProcessLogService processLogService,
          FileLogProcessor fileProcessor,
          MessageLogProcessor messageProcessor,
          IApplicationEventPublisher eventPublisher,
          ILogger<ProcessNotificationHandler> logger,
          ProcessNotificationEventHelper eventHelper)
    {
        _services = services;
        _processLogService = processLogService;
        _fileProcessor = fileProcessor;
        _messageProcessor = messageProcessor;
        _logger = logger;
        _eventHelper = eventHelper;
    }

    public async Task HandleAsync(
        MessageHeader header,
        ProcessNotificationMessage message,
        Guid clientId,
        Guid processLogId)
    {
        await using var context = await _services.DatabaseClientFactory
            .GetDbContext<ProcessLogDbContext>(clientId, ProcessLogDbContext.ConnectionStringName);

        if (context == null)
        {
            throw new ArgumentNullException(nameof(context));
        }

        var timestamp = message.ReceiveTimestamp ?? DateTime.UtcNow;
        var createdBy = header.Requestor?.ToString()
            ?? header.SendingApplication
            ?? "System";

        _logger.LogInformation(
            "Processing notification for ProcessLogId={ProcessLogId}, ClientId={ClientId}, Status={Status}, Source={Source}, Timestamp={Timestamp}",
            processLogId, clientId, header.MessageStatus, header.MessageSource, timestamp);

        using var tx = await context.Database.BeginTransactionAsync();

        try
        {
            var processLog = await _processLogService.GetOrCreateProcessLogAsync(context, processLogId, header, timestamp)
                ?? throw new InvalidOperationException($"ProcessLog {processLogId} not found.");

            if (!string.IsNullOrEmpty(header.MessageStatus) && timestamp > processLog.LastUpdatedTimestamp)
            {
                processLog.Status = header.MessageStatus;
                processLog.LastUpdatedTimestamp = timestamp;
                processLog.UpdatedBy = createdBy;
                context.ProcessLogs.Update(processLog);
            }

            await _messageProcessor.AddMessagesAsync(context, processLog, message.Messages, timestamp, createdBy);
            await _fileProcessor.AddFilesAsync(context, processLog.Id, message.Files, timestamp, createdBy);

            await context.SaveChangesAsync();
            await tx.CommitAsync();

            try
            {
                await _eventHelper.PublishEventIfNeededAsync(
                    header,
                    message,
                    clientId,
                    processLogId
                );
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to publish application event for ProcessLogId={ProcessLogId}", processLogId);
            }

            _logger.LogInformation("Processed ProcessNotification for {ProcessLogId}", processLogId);
        }
        catch (DbUpdateConcurrencyException ex)
        {
            await tx.RollbackAsync();
            _logger.LogWarning(ex, "Concurrency conflict while processing {ProcessLogId}. Changes discarded.", processLogId);
            throw;
        }
        catch (DbUpdateException ex)
        {
            await tx.RollbackAsync();
            _logger.LogError(ex, "Database update error while processing {ProcessLogId}.", processLogId);
            throw;
        }
        catch (Exception ex)
        {
            await tx.RollbackAsync();
            _logger.LogError(ex, "Unexpected error processing ProcessNotification for {ProcessLogId}", processLogId);
            throw;
        }
    }
}
