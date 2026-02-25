using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.Data.TestHelpers.Repository;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.FileProcessLogRepositoryTests;

[TestClass]
public class FileProcessLogRepositoryUpdateTests : BaseRepositoryUpdateTests<ProcessLogDbContext, FileProcessLogRepository, FileProcessLog>
{
    protected override string ConnectionStringName => ProcessLogDbContext.ConnectionStringName;

    protected FileProcessLogTestConfig _testConfig = default!;

    protected override void AdditionalTestSetup(ProcessLogDbContext context)
    {
        base.AdditionalTestSetup(context);

        _testConfig = FileProcessLogRepositoryTestHelpers.BuildTestConfig(context);
    }

    protected override FileProcessLog BuildModel(string label) =>
        FileProcessLogRepositoryTestHelpers.BuildFileProcessLog(_testConfig.ProcessLog, label);
}