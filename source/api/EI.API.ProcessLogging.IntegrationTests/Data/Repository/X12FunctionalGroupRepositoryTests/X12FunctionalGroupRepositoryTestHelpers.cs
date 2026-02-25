using EI.API.ProcessLogging.Data;
using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.IntegrationTests.Data.Repository.FileProcessLogRepositoryTests;
using EI.API.ProcessLogging.IntegrationTests.Data.Repository.ProcessLogRepositoryTests;
using EI.API.ProcessLogging.IntegrationTests.Data.Repository.X12InterchangeRepositoryTests;
using static EI.API.ProcessLogging.IntegrationTests.Data.Repository.TestHelpers;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.X12FunctionalGroupRepositoryTests;

public static class X12FunctionalGroupRepositoryTestHelpers
{
    public static X12FunctionalGroupTestConfig BuildTestConfig(ProcessLogDbContext context)
    {
        var activityType = ProcessLogConstants.ActivityType.ReceiveFile;
        var processStatus = ProcessLogConstants.ProcessStatus.Duplicate;
        var processLog = context.ProcessLogs.Add(ProcessLogTestHelpers.BuildProcessLog(activityType, processStatus, "PL1")).Entity;
        var fileProcessLog = context.FileProcessLogs.Add(FileProcessLogRepositoryTestHelpers.BuildFileProcessLog(processLog, "FPL1")).Entity;
        var x12Interchange = context.X12Interchanges.Add(X12InterchangeRepositoryTestHelpers.BuildX12Interchange(fileProcessLog, ProcessLogConstants.X12Status.Accepted, "XI1")).Entity;

        context.SaveChanges();

        return new X12FunctionalGroupTestConfig
        {
            ProcessLog = processLog,
            FileProcessLog = fileProcessLog,
            X12Interchange = x12Interchange,
        };
    }

    public static X12FunctionalGroup BuildX12FunctionalGroup(X12Interchange x12Interchange, string x12Status, string label)
    {
        var id = Guid.NewGuid();
        var updatedBy = $"UnitTest-{label}";

        return new X12FunctionalGroup
        {
            Id = id,
            X12InterchangeId = x12Interchange.Id,
            Status = x12Status,
            FunctionalIdentifierCode = GetRandom(02),
            ApplicationSenderCode = GetRandom(15),
            ApplicationReceiverCode = GetRandom(15),
            Date = GetRandom(08),
            Time = GetRandom(08),
            GroupControlNumber = GetRandom(09),
            ResponsibleAgencyCode = GetRandom(02),
            VersionReleaseIndustryIdentifierCode = GetRandom(12),
            UpdatedBy = updatedBy,
        };
    }
}
