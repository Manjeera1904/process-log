using EI.API.Cloud.Clients;
using Microsoft.Extensions.Logging;

namespace EI.API.ProcessLogging.Worker.Messaging;
/// <summary>
/// Defines the contract for publishing messages to a service bus topic.
/// </summary>
public interface IServiceBusPublisher
{
    /// <summary>
    /// Publishes a message of type <typeparamref name="T"/> to the specified topic.
    /// </summary>
    /// <typeparam name="T">The type of the message to publish</typeparam>
    /// <param name="topicName">The name of the topic where the message will be sent</param>
    /// <param name="header">The message header containing metadata such as correlation ID</param>
    /// <param name="message">The message payload to send</param>
    /// <param name="cancellationToken">Optional cancellation token to stop the operation</param>
    Task PublishAsync<T>(
        string topicName,
        MessageHeader header,
        T message,
        CancellationToken cancellationToken = default
    )
        where T : class;
}

/// <summary>
/// Default implementation of <see cref="IServiceBusPublisher"/> that uses an <see cref="IMessageClientFactory"/>
/// to create message senders and publish messages to service bus topics.
/// Provides logging of success and failure scenarios.
/// </summary>
public class ServiceBusPublisher : IServiceBusPublisher
{
    private readonly IMessageClientFactory _messageClientFactory;
    private readonly ILogger<ServiceBusPublisher> _logger;

    /// <summary>
    /// Initializes a new instance of the <see cref="ServiceBusPublisher"/> class.
    /// </summary>
    /// <param name="messageClientFactory">Factory responsible for creating message senders.</param>
    /// <param name="logger">Logger for capturing diagnostic and error information.</param>
    public ServiceBusPublisher(
        IMessageClientFactory messageClientFactory,
        ILogger<ServiceBusPublisher> logger
    )
    {
        _messageClientFactory = messageClientFactory;
        _logger = logger;
    }

    /// <summary>
    /// Publishes a message of type <typeparamref name="T"/> to the specified topic.
    /// Logs both successful delivery and any exceptions encountered.
    /// </summary>
    /// <typeparam name="T">The type of the message to publish.</typeparam>
    /// <param name="topicName">The name of the topic where the message will be sent.</param>
    /// <param name="header">The message header containing metadata such as correlation ID.</param>
    /// <param name="message">The message payload to send.</param>
    /// <param name="cancellationToken">Optional cancellation token to stop the operation.</param>
    public async Task PublishAsync<T>(
        string topicName,
        MessageHeader header,
        T message,
        CancellationToken cancellationToken = default
    )
        where T : class
    {
        cancellationToken.ThrowIfCancellationRequested();
        try
        {
            var sender = await _messageClientFactory.CreateMessageSenderAsync(
                topicName,
                cancellationToken
            );
            await sender.SendMessageAsync(header, message, cancellationToken);

            _logger.LogInformation(
                "Message published successfully to topic {Topic}. CorrelationId: {CorrelationId}",
                topicName,
                header.CorrelationId
            );
        }
        catch (Exception ex)
        {
            _logger.LogError(
                ex,
                "Failed to publish message to topic {Topic}. CorrelationId: {CorrelationId}",
                topicName,
                header.CorrelationId
            );
            throw;
        }
    }
}
