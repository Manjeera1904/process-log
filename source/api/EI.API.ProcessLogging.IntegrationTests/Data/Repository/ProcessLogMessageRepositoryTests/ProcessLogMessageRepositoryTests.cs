using EI.API.ProcessLogging.Data;
using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.Data.TestHelpers.Repository;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.ProcessLogMessageRepositoryTests;

[TestClass]
public class ProcessLogMessageRepositoryTests : BaseRepositoryTests<ProcessLogDbContext, ProcessLogMessageRepository, ProcessLogMessage>
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

    [TestMethod]
    public async Task GetByProcessLog_ReturnsResults_V1()
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
    public async Task GetByProcessLog_ReturnsEmpty_WhenNotFound()
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
    public async Task GetByProcessLogAndType_ReturnsResults_V1()
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
        var result = (await _repository.GetByProcessLogAsync(_testConfig.ProcessLog.Id, ProcessLogConstants.MessageLevel.Info)).ToList();

        // Assert
        Assert.AreEqual(2, result.Count);
        Assert.IsTrue(result.Any(e => e.Id == entity2.Id));
        Assert.IsTrue(result.Any(e => e.Id == entity3.Id));
    }

    [TestMethod]
    public async Task GetByProcessLogAndType_ReturnsEmpty_WhenNotFound()
    {
        // Arrange
        var entity1 = BuildModel("one");
        var entity2 = BuildModel("two");

        await _context.AddRangeAsync(entity1, entity2);
        await _context.SaveChangesAsync();

        // Act
        var result = (await _repository.GetByProcessLogAsync(Guid.NewGuid(), ProcessLogConstants.MessageLevel.Info)).ToList();

        // Assert
        Assert.AreEqual(0, result.Count);
    }
    [TestMethod]
    public async Task GetAllAsync_ReturnsAll_V2()
    {
        var entity1 = BuildModel("one");
        entity1.FileProcessLogId = Guid.NewGuid();
        var entity2 = BuildModel("two");
        entity2.FileProcessLogId = Guid.NewGuid();

        await _context.AddRangeAsync(entity1, entity2);
        await _context.SaveChangesAsync();

        var result = (await _repository.GetAllAsync()).ToList();

        Assert.AreEqual(2, result.Count);
        Assert.IsTrue(result.All(e => e.FileProcessLogId != null));
    }

    [TestMethod]
    public async Task GetByIdAsync_ReturnsEntity_V2()
    {
        var entity = BuildModel("one");
        entity.FileProcessLogId = Guid.NewGuid();
        await _context.AddAsync(entity);
        await _context.SaveChangesAsync();

        var result = await _repository.GetByIdAsync(entity.Id);

        Assert.IsNotNull(result);
        Assert.AreEqual(entity.Id, result!.Id);
        Assert.AreEqual(entity.FileProcessLogId, result.FileProcessLogId);
    }

    [TestMethod]
    [ExpectedException(typeof(NotSupportedException))]
    public async Task UpdateAsync_IsNotSupported()
    {
        var entity = BuildModel("one");
        await _context.AddAsync(entity);
        await _context.SaveChangesAsync();

        entity.UpdatedBy = "test-update";
        await _repository.UpdateAsync(entity);
    }
}
