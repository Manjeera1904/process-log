using EI.API.ProcessLogging.Data;
using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.IntegrationTests.Data.Repository.FileProcessLogRepositoryTests;
using EI.API.ProcessLogging.IntegrationTests.Data.Repository.ProcessLogRepositoryTests;
using EI.API.ProcessLogging.IntegrationTests.Data.Repository.X12FunctionalGroupRepositoryTests;
using EI.API.ProcessLogging.IntegrationTests.Data.Repository.X12InterchangeRepositoryTests;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.X12TransactionSetRepositoryTests;

public static class X12TransactionSetRepositoryTestHelpers
{
    public static X12TransactionSetTestConfig BuildTestConfig(ProcessLogDbContext context)
    {
        var activityType = ProcessLogConstants.ActivityType.ReceiveFile;
        var processStatus = ProcessLogConstants.ProcessStatus.Duplicate;
        var processLog = context.ProcessLogs.Add(ProcessLogTestHelpers.BuildProcessLog(activityType, processStatus, "PL1")).Entity;
        var fileProcessLog = context.FileProcessLogs.Add(FileProcessLogRepositoryTestHelpers.BuildFileProcessLog(processLog, "FPL1")).Entity;
        var x12Interchange = context.X12Interchanges.Add(X12InterchangeRepositoryTestHelpers.BuildX12Interchange(fileProcessLog, ProcessLogConstants.X12Status.Accepted, "XI1")).Entity;
        var x12FunctionalGroup = context.X12FunctionalGroups.Add(X12FunctionalGroupRepositoryTestHelpers.BuildX12FunctionalGroup(x12Interchange, ProcessLogConstants.X12Status.Accepted, "XI1")).Entity;

        context.SaveChanges();

        return new X12TransactionSetTestConfig
        {
            ProcessLog = processLog,
            FileProcessLog = fileProcessLog,
            X12Interchange = x12Interchange,
            X12FunctionalGroup = x12FunctionalGroup,
        };
    }

    public static X12TransactionSet BuildX12TransactionSet(X12FunctionalGroup x12FunctionalGroup, string x12Status, string label)
    {
        var id = Guid.NewGuid();
        var updatedBy = $"UnitTest-{label}";

        return new X12TransactionSet
        {
            Id = id,
            X12FunctionalGroupId = x12FunctionalGroup.Id,
            Status = x12Status,
            TransactionSetIdentifierCode = TestHelpers.GetRandom(3),
            TransactionSetControlNumber = TestHelpers.GetRandom(9),
            UpdatedBy = updatedBy,
        };
    }
}