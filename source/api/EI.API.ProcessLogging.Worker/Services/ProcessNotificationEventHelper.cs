using EI.API.Cloud.Clients;
using EI.API.ProcessLogging.Worker.Model;
using Microsoft.Extensions.Logging;

namespace EI.API.ProcessLogging.Worker.Services;

public class ProcessNotificationEventHelper
{
    private readonly IApplicationEventPublisher _eventPublisher;
    private readonly ILogger _logger;

    public ProcessNotificationEventHelper(
        IApplicationEventPublisher eventPublisher,
        ILogger<ProcessNotificationEventHelper> logger)
    {
        _eventPublisher = eventPublisher;
        _logger = logger;
    }

    public async Task PublishEventIfNeededAsync(
        MessageHeader header,
        ProcessNotificationMessage message,
        Guid clientId,
        Guid processLogId)
    {
        var status = header.MessageStatus;

        if (!string.IsNullOrWhiteSpace(status) &&
            (status.Equals("New", StringComparison.OrdinalIgnoreCase)
             || status.Equals("Completed", StringComparison.OrdinalIgnoreCase)
             || status.Equals("Failed", StringComparison.OrdinalIgnoreCase)))
        {
            _logger.LogInformation(
                "Publishing application event for ProcessLogId={ProcessLogId} with status {Status}",
                processLogId, status);

            var eventHeader = new MessageHeader
            {
                MessageId = Guid.NewGuid().ToString(),
                MessageVersion = header.MessageVersion,
                CorrelationId = processLogId.ToString(),
                ClientIdentifier = clientId.ToString(),
                MessageType = header.MessageType,
                MessageStatus = status,
                SendingApplication = "process-log",
                MessageSource = header.MessageSource,
                Requestor = header.Requestor
            };
            //TODO:we need to change this in future based on the requirement
            var eventBody = new
            {
                message,
                Timestamp = DateTime.UtcNow,
            };

            await _eventPublisher.PublishAsync(eventHeader, eventBody);

            _logger.LogInformation(
                "Application event successfully sent for {ProcessLogId}",
                processLogId);
        }
    }
}
