using EI.API.ProcessLogging.Data;
using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.Data.TestHelpers.Repository;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.ProcessLogRepositoryTests;

[TestClass]
public class ProcessLogRepositoryInsertTests : BaseRepositoryInsertTests<ProcessLogDbContext, ProcessLogRepository, ProcessLog>
{
    protected override string ConnectionStringName => ProcessLogDbContext.ConnectionStringName;

    protected ProcessLogTestConfig _testConfig = default!;

    protected override void AdditionalTestSetup(ProcessLogDbContext context)
    {
        base.AdditionalTestSetup(context);

        _testConfig = ProcessLogTestHelpers.BuildTestConfig(context);
    }

    protected override ProcessLog BuildModel(string label) =>
        ProcessLogTestHelpers.BuildProcessLog(ProcessLogConstants.ActivityType.ReceiveFile, ProcessLogConstants.ProcessStatus.Duplicate, label);

    protected override ProcessLogRepository BuildRepo(ProcessLogDbContext context)
        => ProcessLogTestHelpers.BuildRepo(context);
}