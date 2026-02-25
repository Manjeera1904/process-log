using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.Data.TestHelpers.Repository;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.X12MessageRepositoryTests;

[TestClass]
public class X12MessageRepositoryReadTests : BaseRepositoryReadTests<ProcessLogDbContext, X12MessageRepository, X12Message>
{
    protected override string ConnectionStringName => ProcessLogDbContext.ConnectionStringName;

    protected X12MessageTestConfig _testConfig = default!;

    protected override void AdditionalTestSetup(ProcessLogDbContext context)
    {
        base.AdditionalTestSetup(context);

        _testConfig = X12MessageTestHelpers.BuildTestConfig(context);
    }

    protected override X12Message BuildModel(string label) =>
        X12MessageTestHelpers.BuildX12Message(label, _testConfig.X12Interchange);
}