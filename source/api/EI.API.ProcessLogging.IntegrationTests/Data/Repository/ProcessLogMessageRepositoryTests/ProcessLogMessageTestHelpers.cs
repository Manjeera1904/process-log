using EI.API.ProcessLogging.Data;
using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.IntegrationTests.Data.Repository.ProcessLogRepositoryTests;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.ProcessLogMessageRepositoryTests;

public static class ProcessLogMessageTestHelpers
{
    public static ProcessLogMessageTestConfig BuildTestConfig(ProcessLogDbContext context)
    {
        var activityType = ProcessLogConstants.ActivityType.ReceiveFile;
        var processStatus = ProcessLogConstants.ProcessStatus.Duplicate;
        var processLog = context.ProcessLogs.Add(ProcessLogTestHelpers.BuildProcessLog(activityType, processStatus, "PL1")).Entity;

        context.SaveChanges();

        return new ProcessLogMessageTestConfig
        {
            ProcessLog = processLog,
        };
    }

    public static ProcessLogMessage BuildProcessLogMessage(ProcessLog processLog, string label) =>
        new()
        {
            Id = Guid.NewGuid(),
            Level = ProcessLogConstants.MessageLevel.Info,
            Message = $"Test Message {label}",
            MessageTimestamp = DateTime.UtcNow,
            ProcessLogId = processLog.Id,
            UpdatedBy = $"ProcessLogMessage-UnitTest-{label}",
        };
}