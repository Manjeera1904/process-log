using EI.API.ProcessLogging.Data;
using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.Data.TestHelpers.Repository;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.X12InterchangeRepositoryTests;

[TestClass]
public class X12InterchangeRepositoryReadTests : BaseRepositoryReadTests<ProcessLogDbContext, X12InterchangeRepository, X12Interchange>
{
    protected override string ConnectionStringName => ProcessLogDbContext.ConnectionStringName;

    protected X12InterchangeTestConfig _testConfig = default!;

    protected override void AdditionalTestSetup(ProcessLogDbContext context)
    {
        base.AdditionalTestSetup(context);

        _testConfig = X12InterchangeRepositoryTestHelpers.BuildTestConfig(context);
    }

    protected override X12Interchange BuildModel(string label) =>
        X12InterchangeRepositoryTestHelpers.BuildX12Interchange(_testConfig.FileProcessLog, ProcessLogConstants.X12Status.Duplicate, label);
}