using EI.API.Cloud.Clients;
using EI.API.ProcessLogging.Worker.Messaging;
using Microsoft.Extensions.Logging;

namespace EI.API.ProcessLogging.Worker.Services;

public interface IApplicationEventPublisher
{
    Task PublishAsync(MessageHeader header, object body, string topic = "application-events");
}
public class ApplicationEventPublisher : IApplicationEventPublisher
{
    private readonly IServiceBusPublisher _publisher;

    private readonly ILogger<ApplicationEventPublisher> _logger;

    public ApplicationEventPublisher(IServiceBusPublisher publisher, ILogger<ApplicationEventPublisher> logger)
    {
        _publisher = publisher;
        _logger = logger;
    }

    public async Task PublishAsync(MessageHeader header, object body, string topic = "application-events")
    {
        _logger.LogInformation("Publishing event to topic {Topic}", topic);
        await _publisher.PublishAsync(
           topic,
           header,
           body
       );
    }
}
