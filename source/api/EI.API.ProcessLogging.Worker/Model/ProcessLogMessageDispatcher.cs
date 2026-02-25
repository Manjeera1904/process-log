using EI.API.Cloud.Clients.Azure.Messaging.Versioning;
using System.Text.Json;

namespace EI.API.ProcessLogging.Worker.Model;

public sealed class ProcessNotificationMessageDispatcher
    : IMessageBodyDispatcher<ProcessNotificationMessage>
{

    public IReadOnlyCollection<string> SupportedVersions =>
        new[] { "2.0", "3.0" };

    /// <summary>
    /// Deserialize 
    /// </summary>
    /// <param name="body"></param>
    /// <param name="version"></param>
    /// <returns></returns>
    /// <exception cref="NotSupportedException"></exception>
    /// <exception cref="InvalidOperationException"></exception>
    public ProcessNotificationMessage Deserialize(string body, string version)
    {
        if (!SupportedVersions.Contains(version))
        {
            throw new NotSupportedException(
                $"Message body version '{version}' is not supported by ProcessLogging Worker");
        }

        if (string.IsNullOrWhiteSpace(body))
        {
            throw new InvalidOperationException(
                "Message body cannot be empty.");
        }

        try
        {
            return JsonSerializer.Deserialize<ProcessNotificationMessage>(body)
                   ?? throw new InvalidOperationException(
                       $"Failed to deserialize ProcessNotificationMessage for version {version}");
        }
        catch (JsonException ex)
        {
            throw new InvalidOperationException(
                $"Invalid JSON payload for ProcessNotificationMessage version {version}",
                ex);
        }
    }
}