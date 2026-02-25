using EI.API.ProcessLogging.Data;
using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.IntegrationTests.Data.Repository.ProcessLogRepositoryTests;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.FileProcessLogRepositoryTests;

public static class FileProcessLogRepositoryTestHelpers
{
    public static FileProcessLogTestConfig BuildTestConfig(ProcessLogDbContext context)
    {
        var activityType = ProcessLogConstants.ActivityType.ReceiveFile;
        var processStatus = ProcessLogConstants.ProcessStatus.Duplicate;
        var processLog = context.ProcessLogs.Add(ProcessLogTestHelpers.BuildProcessLog(activityType, processStatus, "PL1")).Entity;

        context.SaveChanges();

        return new FileProcessLogTestConfig
        {
            ProcessLog = processLog,
        };
    }

    public static FileProcessLog BuildFileProcessLog(ProcessLog processLog, string label)
    {
        var id = Guid.NewGuid();
        var updatedBy = $"UnitTest-{label}";

        return new FileProcessLog
        {
            Id = id,
            ProcessLogId = processLog.Id,
            FileName = $"UnitTest-{label}.TXT",
            FilePath = $"https://blobstorage.azure.example.com/some/weird/location/{label}/UnitTest-{label}.TXT",
            FileSize = 47047,
            FileHash = Guid.NewGuid().ToString(),
            UpdatedBy = updatedBy,
        };
    }
}