using EI.API.ProcessLogging.Data;
using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.Data.TestHelpers.Repository;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.X12TransactionSetRepositoryTests;

[TestClass]
public class X12TransactionSetRepositoryInsertTests : BaseRepositoryInsertTests<ProcessLogDbContext, X12TransactionSetRepository, X12TransactionSet>
{
    protected override string ConnectionStringName => ProcessLogDbContext.ConnectionStringName;

    protected X12TransactionSetTestConfig _testConfig = default!;

    protected override void AdditionalTestSetup(ProcessLogDbContext context)
    {
        base.AdditionalTestSetup(context);

        _testConfig = X12TransactionSetRepositoryTestHelpers.BuildTestConfig(context);
    }

    protected override X12TransactionSet BuildModel(string label) =>
        X12TransactionSetRepositoryTestHelpers.BuildX12TransactionSet(_testConfig.X12FunctionalGroup, ProcessLogConstants.X12Status.Duplicate, label);
}