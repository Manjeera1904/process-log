using EI.API.ProcessLogging.Data;
using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.IntegrationTests.Data.Repository.FileProcessLogRepositoryTests;
using EI.API.ProcessLogging.IntegrationTests.Data.Repository.ProcessLogRepositoryTests;
using static EI.API.ProcessLogging.IntegrationTests.Data.Repository.TestHelpers;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.X12InterchangeRepositoryTests;

public static class X12InterchangeRepositoryTestHelpers
{
    public static X12InterchangeTestConfig BuildTestConfig(ProcessLogDbContext context)
    {
        var activityType = ProcessLogConstants.ActivityType.ReceiveFile;
        var processStatus = ProcessLogConstants.ProcessStatus.Duplicate;
        var processLog = context.ProcessLogs.Add(ProcessLogTestHelpers.BuildProcessLog(activityType, processStatus, "PL1")).Entity;
        var fileProcessLog = context.FileProcessLogs.Add(FileProcessLogRepositoryTestHelpers.BuildFileProcessLog(processLog, "FPL1")).Entity;

        context.SaveChanges();

        return new X12InterchangeTestConfig
        {
            ProcessLog = processLog,
            FileProcessLog = fileProcessLog,
        };
    }

    public static X12Interchange BuildX12Interchange(FileProcessLog fileProcessLog, string x12Status, string label)
    {
        var id = Guid.NewGuid();
        var updatedBy = $"UnitTest-{label}";

        return new X12Interchange
        {
            Id = id,
            FileProcessLogId = fileProcessLog.Id,
            Status = x12Status,
            InterchangeSenderIdQualifier = GetRandom(10),
            InterchangeSenderId = GetRandom(15),
            InterchangeReceiverIdQualifier = GetRandom(10),
            InterchangeReceiverId = GetRandom(15),
            InterchangeDate = GetRandom(6),
            InterchangeTime = GetRandom(4),
            RepetitionSeparator = GetRandom(4),
            InterchangeControlVersionNumber = GetRandom(5),
            InterchangeControlNumber = GetRandom(9),
            AcknowledgementRequested = GetRandom(1),
            UsageIndicator = GetRandom(1),
            ComponentElementSeparator = GetRandom(1),
            UpdatedBy = updatedBy,
        };
    }
}