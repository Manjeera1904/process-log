using EI.API.ProcessLogging.Data;
using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.Data.TestHelpers.Repository;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.X12MessageRepositoryTests;

[TestClass]
public class X12MessageRepositoryTests : BaseRepositoryTests<ProcessLogDbContext, X12MessageRepository, X12Message>
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

    [TestMethod]
    public async Task GetByInterchange_ReturnsResults()
    {
        // Arrange
        var entity1 = BuildModel("one");
        var entity2 = BuildModel("two");

        await _context.AddRangeAsync(entity1, entity2);
        await _context.SaveChangesAsync();

        // Act
        var result = (await _repository.GetByInterchangeAsync(_testConfig.X12Interchange.Id)).ToList();

        // Assert
        Assert.AreEqual(2, result.Count);
        Assert.IsTrue(result.Any(e => e.Id == entity1.Id));
        Assert.IsTrue(result.Any(e => e.Id == entity2.Id));
    }

    [TestMethod]
    public async Task GetByInterchange_ReturnsEmpty_WhenNotFound()
    {
        // Arrange
        var entity1 = BuildModel("one");
        var entity2 = BuildModel("two");

        await _context.AddRangeAsync(entity1, entity2);
        await _context.SaveChangesAsync();

        // Act
        var result = (await _repository.GetByInterchangeAsync(Guid.NewGuid())).ToList();

        // Assert
        Assert.AreEqual(0, result.Count);
    }

    [TestMethod]
    public async Task GetByInterchangeAndLevel_ReturnsResults()
    {
        // Arrange
        var entity1 = BuildModel("one");
        entity1.Level = ProcessLogConstants.MessageLevel.Error;

        var entity2 = BuildModel("two");
        entity2.Level = ProcessLogConstants.MessageLevel.Info;

        var entity3 = BuildModel("three");
        entity3.Level = ProcessLogConstants.MessageLevel.Info;

        await _context.AddRangeAsync(entity1, entity2, entity3);
        await _context.SaveChangesAsync();

        // Act
        var result = (await _repository.GetByInterchangeAsync(_testConfig.X12Interchange.Id, ProcessLogConstants.MessageLevel.Info)).ToList();

        // Assert
        Assert.AreEqual(2, result.Count);
        Assert.IsTrue(result.Any(e => e.Id == entity2.Id));
        Assert.IsTrue(result.Any(e => e.Id == entity3.Id));
    }

    [TestMethod]
    public async Task GetByInterchangeAndLevel_ReturnsEmpty_WhenNotFound()
    {
        // Arrange
        var entity1 = BuildModel("one");
        var entity2 = BuildModel("two");

        await _context.AddRangeAsync(entity1, entity2);
        await _context.SaveChangesAsync();

        // Act
        var result = (await _repository.GetByInterchangeAsync(Guid.NewGuid(), ProcessLogConstants.MessageLevel.Info)).ToList();

        // Assert
        Assert.AreEqual(0, result.Count);
    }

    [TestMethod]
    public async Task GetByFunctionalGroup_ReturnsResults()
    {
        // Arrange
        var entity1 = BuildModel("one");
        entity1.X12FunctionalGroupId = _testConfig.X12FunctionalGroup.Id;

        var entity2 = BuildModel("two");
        entity2.X12FunctionalGroupId = _testConfig.X12FunctionalGroup.Id;

        await _context.AddRangeAsync(entity1, entity2);
        await _context.SaveChangesAsync();

        // Act
        var result = (await _repository.GetByFunctionalGroupAsync(_testConfig.X12FunctionalGroup.Id)).ToList();

        // Assert
        Assert.AreEqual(2, result.Count);
        Assert.IsTrue(result.Any(e => e.Id == entity1.Id));
        Assert.IsTrue(result.Any(e => e.Id == entity2.Id));
    }

    [TestMethod]
    public async Task GetByFunctionalGroup_ReturnsEmpty_WhenNotFound()
    {
        // Arrange
        var entity1 = BuildModel("one");
        entity1.X12FunctionalGroupId = _testConfig.X12FunctionalGroup.Id;

        var entity2 = BuildModel("two");
        entity2.X12FunctionalGroupId = _testConfig.X12FunctionalGroup.Id;

        await _context.AddRangeAsync(entity1, entity2);
        await _context.SaveChangesAsync();

        // Act
        var result = (await _repository.GetByFunctionalGroupAsync(Guid.NewGuid())).ToList();

        // Assert
        Assert.AreEqual(0, result.Count);
    }

    [TestMethod]
    public async Task GetByFunctionalGroupAndLevel_ReturnsResults()
    {
        // Arrange
        var entity1 = BuildModel("one");
        entity1.X12FunctionalGroupId = _testConfig.X12FunctionalGroup.Id;
        entity1.Level = ProcessLogConstants.MessageLevel.Error;

        var entity2 = BuildModel("two");
        entity2.X12FunctionalGroupId = _testConfig.X12FunctionalGroup.Id;
        entity2.Level = ProcessLogConstants.MessageLevel.Info;

        var entity3 = BuildModel("three");
        entity3.X12FunctionalGroupId = _testConfig.X12FunctionalGroup.Id;
        entity3.Level = ProcessLogConstants.MessageLevel.Info;

        await _context.AddRangeAsync(entity1, entity2, entity3);
        await _context.SaveChangesAsync();

        // Act
        var result = (await _repository.GetByFunctionalGroupAsync(_testConfig.X12FunctionalGroup.Id, ProcessLogConstants.MessageLevel.Info)).ToList();

        // Assert
        Assert.AreEqual(2, result.Count);
        Assert.IsTrue(result.Any(e => e.Id == entity2.Id));
        Assert.IsTrue(result.Any(e => e.Id == entity3.Id));
    }

    [TestMethod]
    public async Task GetByFunctionalGroupAndLevel_ReturnsEmpty_WhenNotFound()
    {
        // Arrange
        var entity1 = BuildModel("one");
        entity1.X12FunctionalGroupId = _testConfig.X12FunctionalGroup.Id;

        var entity2 = BuildModel("two");
        entity2.X12FunctionalGroupId = _testConfig.X12FunctionalGroup.Id;

        await _context.AddRangeAsync(entity1, entity2);
        await _context.SaveChangesAsync();

        // Act
        var result = (await _repository.GetByFunctionalGroupAsync(Guid.NewGuid(), ProcessLogConstants.MessageLevel.Info)).ToList();

        // Assert
        Assert.AreEqual(0, result.Count);
    }

    [TestMethod]
    public async Task GetByTransactionSet_ReturnsResults()
    {
        // Arrange
        var entity1 = BuildModel("one");
        entity1.X12FunctionalGroupId = _testConfig.X12FunctionalGroup.Id;
        entity1.X12TransactionSetId = _testConfig.X12TransactionSet.Id;

        var entity2 = BuildModel("two");
        entity2.X12FunctionalGroupId = _testConfig.X12FunctionalGroup.Id;
        entity2.X12TransactionSetId = _testConfig.X12TransactionSet.Id;

        await _context.AddRangeAsync(entity1, entity2);
        await _context.SaveChangesAsync();

        // Act
        var result = (await _repository.GetByTransactionSetAsync(_testConfig.X12TransactionSet.Id)).ToList();

        // Assert
        Assert.AreEqual(2, result.Count);
        Assert.IsTrue(result.Any(e => e.Id == entity1.Id));
        Assert.IsTrue(result.Any(e => e.Id == entity2.Id));
    }

    [TestMethod]
    public async Task GetByTransactionSet_ReturnsEmpty_WhenNotFound()
    {
        // Arrange
        var entity1 = BuildModel("one");
        entity1.X12FunctionalGroupId = _testConfig.X12FunctionalGroup.Id;
        entity1.X12TransactionSetId = _testConfig.X12TransactionSet.Id;

        var entity2 = BuildModel("two");
        entity2.X12FunctionalGroupId = _testConfig.X12FunctionalGroup.Id;
        entity2.X12TransactionSetId = _testConfig.X12TransactionSet.Id;

        await _context.AddRangeAsync(entity1, entity2);
        await _context.SaveChangesAsync();

        // Act
        var result = (await _repository.GetByTransactionSetAsync(Guid.NewGuid())).ToList();

        // Assert
        Assert.AreEqual(0, result.Count);
    }

    [TestMethod]
    public async Task GetByTransactionSetAndLevel_ReturnsResults()
    {
        // Arrange
        var entity1 = BuildModel("one");
        entity1.X12FunctionalGroupId = _testConfig.X12FunctionalGroup.Id;
        entity1.X12TransactionSetId = _testConfig.X12TransactionSet.Id;
        entity1.Level = ProcessLogConstants.MessageLevel.Error;

        var entity2 = BuildModel("two");
        entity2.X12FunctionalGroupId = _testConfig.X12FunctionalGroup.Id;
        entity2.X12TransactionSetId = _testConfig.X12TransactionSet.Id;
        entity2.Level = ProcessLogConstants.MessageLevel.Info;

        var entity3 = BuildModel("three");
        entity3.X12FunctionalGroupId = _testConfig.X12FunctionalGroup.Id;
        entity3.X12TransactionSetId = _testConfig.X12TransactionSet.Id;
        entity3.Level = ProcessLogConstants.MessageLevel.Info;

        await _context.AddRangeAsync(entity1, entity2, entity3);
        await _context.SaveChangesAsync();

        // Act
        var result = (await _repository.GetByTransactionSetAsync(_testConfig.X12TransactionSet.Id, ProcessLogConstants.MessageLevel.Info)).ToList();

        // Assert
        Assert.AreEqual(2, result.Count);
        Assert.IsTrue(result.Any(e => e.Id == entity2.Id));
        Assert.IsTrue(result.Any(e => e.Id == entity3.Id));
    }

    [TestMethod]
    public async Task GetByTransactionSetAndLevel_ReturnsEmpty_WhenNotFound()
    {
        // Arrange
        var entity1 = BuildModel("one");
        entity1.X12FunctionalGroupId = _testConfig.X12FunctionalGroup.Id;
        entity1.X12TransactionSetId = _testConfig.X12TransactionSet.Id;

        var entity2 = BuildModel("two");
        entity2.X12FunctionalGroupId = _testConfig.X12FunctionalGroup.Id;
        entity2.X12TransactionSetId = _testConfig.X12TransactionSet.Id;

        await _context.AddRangeAsync(entity1, entity2);
        await _context.SaveChangesAsync();

        // Act
        var result = (await _repository.GetByTransactionSetAsync(Guid.NewGuid(), ProcessLogConstants.MessageLevel.Info)).ToList();

        // Assert
        Assert.AreEqual(0, result.Count);
    }
}
