using EI.API.ProcessLogging.Data;
using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.Data.TestHelpers.Repository;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.X12InterchangeRepositoryTests;

[TestClass]
public class X12InterchangeRepositoryTests : BaseRepositoryTests<ProcessLogDbContext, X12InterchangeRepository, X12Interchange>
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

    [TestMethod]
    public async Task GetByProcessLog_ReturnsResults()
    {
        // Arrange
        var entity1 = BuildModel("one");
        var entity2 = BuildModel("two");

        await _context.AddRangeAsync(entity1, entity2);
        await _context.SaveChangesAsync();

        // Act
        var result = (await _repository.GetByProcessLogAsync(_testConfig.ProcessLog.Id)).ToList();

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
        var result = (await _repository.GetByProcessLogAsync(Guid.NewGuid())).ToList();

        // Assert
        Assert.AreEqual(0, result.Count);
    }

    [TestMethod]
    public async Task GetByFileProcessLog_ReturnsResults()
    {
        // Arrange
        var entity1 = BuildModel("one");
        var entity2 = BuildModel("two");

        await _context.AddRangeAsync(entity1, entity2);
        await _context.SaveChangesAsync();

        // Act
        var result = (await _repository.GetByFileProcessLogAsync(_testConfig.FileProcessLog.Id)).ToList();

        // Assert
        Assert.AreEqual(2, result.Count);
        Assert.IsTrue(result.Any(e => e.Id == entity1.Id));
        Assert.IsTrue(result.Any(e => e.Id == entity2.Id));
    }

    [TestMethod]
    public async Task GetByFileProcessLog_ReturnsEmpty_WhenNoneFound()
    {
        // Arrange
        var entity1 = BuildModel("one");
        var entity2 = BuildModel("two");

        await _context.AddRangeAsync(entity1, entity2);
        await _context.SaveChangesAsync();

        // Act
        var result = (await _repository.GetByFileProcessLogAsync(Guid.NewGuid())).ToList();

        // Assert
        Assert.AreEqual(0, result.Count);
    }
}
