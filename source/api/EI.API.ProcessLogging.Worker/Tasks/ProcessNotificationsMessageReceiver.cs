using EI.API.Cloud.Clients;
using EI.API.Cloud.Clients.Azure.Messaging.Versioning;
using EI.API.ProcessLogging.Worker.Model;
using EI.API.ProcessLogging.Worker.Services;
using Microsoft.Extensions.Logging;

namespace EI.API.ProcessLogging.Worker.Tasks;

public class ProcessNotificationsMessageReceiver : BaseMessageReceiver<ProcessNotificationMessage>
{
    private readonly IProcessNotificationHandler _handler;

    public ProcessNotificationsMessageReceiver(
        IMessageReceiverServices services,
        IMessageBodyDispatcher<ProcessNotificationMessage> dispatcher,
        IProcessNotificationHandler handler,
        ILogger<ProcessNotificationsMessageReceiver> logger
    )
        : base(services, dispatcher, logger)
    {
        _handler = handler;
    }

    protected override string TopicName => "process-logging";
    protected override string SubscriptionName => "process-notifications";

    protected override Task HandleMessageAsync(
        MessageHeader header,
        ProcessNotificationMessage message,
        Guid clientId,
        Guid correlationId
    )
    {
        return _handler.HandleAsync(header, message, clientId, correlationId);
    }
}
