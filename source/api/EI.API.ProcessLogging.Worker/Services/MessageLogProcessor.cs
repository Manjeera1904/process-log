using EI.API.ProcessLogging.Data;
using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Worker.Model;
using Microsoft.EntityFrameworkCore;

namespace EI.API.ProcessLogging.Worker.Services;

public class MessageLogProcessor
{
    public async Task AddMessagesAsync(
        ProcessLogDbContext context,
        ProcessLog processLog,
        IEnumerable<MessageEntry>? messages,
        DateTime timestamp,
        string createdBy
    )
    {
        if (messages == null)
            return;

        foreach (var msg in messages)
        {
            var exists = await context.ProcessLogMessages.AnyAsync(m =>
                m.ProcessLogId == processLog.Id
                && m.Message == msg.Message
                && m.Level == (msg.MessageLevel ?? ProcessLogConstants.MessageLevel.Info)
            );

            if (exists)
                continue;

            await context
                .ProcessLogMessages.AddAsync(
                    new ProcessLogMessage
                    {
                        ProcessLogId = processLog.Id,
                        Level = msg.MessageLevel ?? ProcessLogConstants.MessageLevel.Info,
                        Message = msg.Message ?? "Empty message",
                        MessageTimestamp = timestamp,
                        UpdatedBy = createdBy,
                    }
                )
                .ConfigureAwait(false);
        }
    }
}
