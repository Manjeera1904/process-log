using EI.API.ProcessLogging.Data;
using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.Data.TestHelpers.Repository;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.X12FunctionalGroupRepositoryTests;

[TestClass]
public class X12FunctionalGroupRepositoryUpdateTests : BaseRepositoryUpdateTests<ProcessLogDbContext, X12FunctionalGroupRepository, X12FunctionalGroup>
{
    protected override string ConnectionStringName => ProcessLogDbContext.ConnectionStringName;

    protected X12FunctionalGroupTestConfig _testConfig = default!;

    protected override void AdditionalTestSetup(ProcessLogDbContext context)
    {
        base.AdditionalTestSetup(context);

        _testConfig = X12FunctionalGroupRepositoryTestHelpers.BuildTestConfig(context);
    }

    protected override X12FunctionalGroup BuildModel(string label) =>
        X12FunctionalGroupRepositoryTestHelpers.BuildX12FunctionalGroup(_testConfig.X12Interchange, ProcessLogConstants.X12Status.Invalid, label);
}