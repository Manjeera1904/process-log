using EI.API.ProcessLogging.Data;
using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.IntegrationTests.Data.Repository.FileProcessLogRepositoryTests;
using EI.API.ProcessLogging.IntegrationTests.Data.Repository.ProcessLogRepositoryTests;
using EI.API.ProcessLogging.IntegrationTests.Data.Repository.X12FunctionalGroupRepositoryTests;
using EI.API.ProcessLogging.IntegrationTests.Data.Repository.X12InterchangeRepositoryTests;
using EI.API.ProcessLogging.IntegrationTests.Data.Repository.X12TransactionSetRepositoryTests;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.X12MessageRepositoryTests;

public static class X12MessageTestHelpers
{
    public static X12MessageTestConfig BuildTestConfig(ProcessLogDbContext context)
    {
        var activityType = ProcessLogConstants.ActivityType.ReceiveFile;
        var processStatus = ProcessLogConstants.ProcessStatus.Duplicate;

        var processLog = context.ProcessLogs.Add(ProcessLogTestHelpers.BuildProcessLog(activityType, processStatus, "PL1")).Entity;
        var fileProcessLog = context.FileProcessLogs.Add(FileProcessLogRepositoryTestHelpers.BuildFileProcessLog(processLog, "FPL1")).Entity;
        var x12Interchange = context.X12Interchanges.Add(X12InterchangeRepositoryTestHelpers.BuildX12Interchange(fileProcessLog, ProcessLogConstants.X12Status.Accepted, "XI1")).Entity;
        var x12FunctionalGroup = context.X12FunctionalGroups.Add(X12FunctionalGroupRepositoryTestHelpers.BuildX12FunctionalGroup(x12Interchange, ProcessLogConstants.X12Status.Accepted, "XFG1")).Entity;
        var x12TransactionSet = context.X12TransactionSets.Add(X12TransactionSetRepositoryTestHelpers.BuildX12TransactionSet(x12FunctionalGroup, ProcessLogConstants.X12Status.Accepted, "XTS1")).Entity;

        context.SaveChanges();

        return new X12MessageTestConfig
        {
            ProcessLog = processLog,
            FileProcessLog = fileProcessLog,
            X12Interchange = x12Interchange,
            X12FunctionalGroup = x12FunctionalGroup,
            X12TransactionSet = x12TransactionSet,
        };
    }

    public static X12Message BuildX12Message(string label, X12Interchange interchange, X12FunctionalGroup? functionalGroup = null, X12TransactionSet? transactionSet = null) =>
        new()
        {
            Id = Guid.NewGuid(),
            Level = ProcessLogConstants.MessageLevel.Info,
            Message = $"Test Message {label}",
            MessageTimestamp = DateTime.UtcNow,
            X12InterchangeId = interchange.Id,
            X12FunctionalGroupId = functionalGroup?.Id,
            X12TransactionSetId = transactionSet?.Id,
            UpdatedBy = $"X12Message-UnitTest-{label}",
        };
}