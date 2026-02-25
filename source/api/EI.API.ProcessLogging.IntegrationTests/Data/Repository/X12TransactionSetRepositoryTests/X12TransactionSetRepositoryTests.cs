using EI.API.ProcessLogging.Data;
using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.Data.TestHelpers.Repository;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.X12TransactionSetRepositoryTests;

[TestClass]
public class X12TransactionSetRepositoryTests : BaseRepositoryTests<ProcessLogDbContext, X12TransactionSetRepository, X12TransactionSet>
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

    [TestMethod]
    public async Task GetByProcessLog_ReturnsResults()
    {
        // Arrange
        var entity1 = BuildModel("one");
        var entity2 = BuildModel("two");

        await _context.AddRangeAsync(entity1, entity2);
        await _context.SaveChangesAsync();

        // Act
        var result = (await _repository.GetByFunctionalGroup(_testConfig.X12FunctionalGroup.Id)).ToList();

        // Assert
        Assert.AreEqual(2, result.Count);
        Assert.IsTrue(result.Any(e => e.Id == entity1.Id));
        Assert.IsTrue(result.Any(e => e.Id == entity2.Id));
    }

    [TestMethod]
    public async Task GetByProcessLog_ReturnsEmpty_WhenNoneFound()
    {
        // Arrange
        var entity1 = BuildModel("one");
        var entity2 = BuildModel("two");

        await _context.AddRangeAsync(entity1, entity2);
        await _context.SaveChangesAsync();

        // Act
        var result = (await _repository.GetByFunctionalGroup(Guid.NewGuid())).ToList();

        // Assert
        Assert.AreEqual(0, result.Count);
    }
}
