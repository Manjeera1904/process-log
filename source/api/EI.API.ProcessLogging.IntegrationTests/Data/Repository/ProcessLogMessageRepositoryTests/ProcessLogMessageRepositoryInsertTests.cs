using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.Data.TestHelpers.Repository;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.ProcessLogMessageRepositoryTests;

[TestClass]
public class ProcessLogMessageRepositoryInsertTests : BaseRepositoryInsertTests<ProcessLogDbContext, TestWriteableProcessLogMessageRepository, ProcessLogMessage>
{
    protected override string ConnectionStringName => ProcessLogDbContext.ConnectionStringName;

    protected ProcessLogMessageTestConfig _testConfig = default!;

    protected override void AdditionalTestSetup(ProcessLogDbContext context)
    {
        base.AdditionalTestSetup(context);

        _testConfig = ProcessLogMessageTestHelpers.BuildTestConfig(context);
    }

    protected override ProcessLogMessage BuildModel(string label) =>
        ProcessLogMessageTestHelpers.BuildProcessLogMessage(_testConfig.ProcessLog, label);
}