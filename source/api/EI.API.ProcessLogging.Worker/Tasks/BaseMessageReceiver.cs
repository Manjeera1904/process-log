using Autofac;
using EI.API.Cloud.Clients;
using EI.API.Cloud.Clients.Azure.Messaging.Versioning;
using Microsoft.Extensions.Logging;
using Polly;
using System.Collections.Concurrent;

namespace EI.API.ProcessLogging.Worker.Tasks;

public abstract class BaseMessageReceiver<TMessage> : IStartable, IAsyncDisposable
    where TMessage : class
{
    private readonly IMessageReceiverServices _services;
    private readonly IMessageBodyDispatcher<TMessage> _dispatcher;
    private readonly ILogger _logger;
    private IMessageReceiver? _receiver;
    private readonly ConcurrentDictionary<Guid, SemaphoreSlim> _locks = new();

    protected abstract string TopicName { get; }
    protected abstract string SubscriptionName { get; }

    protected BaseMessageReceiver(IMessageReceiverServices services, IMessageBodyDispatcher<TMessage> dispatcher, ILogger logger)
    {
        _services = services ?? throw new ArgumentNullException(nameof(services));
        _dispatcher = dispatcher ?? throw new ArgumentNullException(nameof(dispatcher));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    }

    /// <summary>
    /// Implemented in the concrete class: handles the processing logic of the received message.
    /// </summary>
    protected abstract Task HandleMessageAsync(
        MessageHeader header,
        TMessage message,
        Guid clientId,
        Guid correlationId
    );

    public void Start()
    {
        _receiver = _services
            .MessageClientFactory.CreateMessageReceiverAsync(TopicName, SubscriptionName)
            .GetAwaiter()
            .GetResult();

        _receiver.StartListeningAsync<TMessage>(OnReceiveMessage, _dispatcher).GetAwaiter().GetResult();

        _logger.LogInformation(
            "Listening on topic '{TopicName}', subscription '{SubscriptionName}'",
            TopicName,
            SubscriptionName
        );
    }

    private async Task OnReceiveMessage(MessageHeader header, TMessage message)
    {
        _logger.LogDebug(
            "Received message on {Topic}/{Sub} with CorrelationId={CorrelationId}",
            TopicName,
            SubscriptionName,
            header.CorrelationId
        );

        if (!Guid.TryParse(header.CorrelationId, out var correlationId))
        {
            _logger.LogWarning(
                "Invalid CorrelationId in message header: {CorrelationId}",
                header.CorrelationId
            );
            return;
        }

        if (!Guid.TryParse(header.ClientIdentifier, out var clientId))
        {
            _logger.LogWarning(
                "Invalid ClientIdentifier in message header: {ClientIdentifier}",
                header.ClientIdentifier
            );
            return;
        }

        var sem = _locks.GetOrAdd(correlationId, _ => new SemaphoreSlim(1, 1));
        await sem.WaitAsync();

        try
        {
            var retryPolicy = Policy
                .Handle<Exception>()
                .WaitAndRetryAsync(
                    retryCount: 1,
                    sleepDurationProvider: attempt => TimeSpan.FromMilliseconds(200 * attempt),
                    onRetry: (ex, ts, retryCount, _) =>
                    {
                        _logger.LogWarning(
                            ex,
                            "Retry {RetryCount} for CorrelationId {CorrelationId} after {Delay}ms due to {ErrorType}",
                            retryCount,
                            correlationId,
                            ts.TotalMilliseconds,
                            ex.GetType().Name
                        );
                    }
                );

            await retryPolicy.ExecuteAsync(
                () => HandleMessageAsync(header, message, clientId, correlationId)
            );
        }
        catch (Exception ex)
        {
            _logger.LogError(
                ex,
                "Fatal error processing message for CorrelationId={CorrelationId} on Topic={TopicName}, Subscription={SubscriptionName}",
                correlationId,
                TopicName,
                SubscriptionName
            );
            throw; // rethrow so Service Bus can retry or dead-letter
        }
        finally
        {
            sem.Release();
        }
    }

    public async ValueTask DisposeAsync()
    {
        if (_receiver != null)
        {
            await _receiver.DisposeAsync();
            _receiver = null;
        }

        foreach (var (_, semaphore) in _locks)
            semaphore.Dispose();

        _locks.Clear();
    }
}
