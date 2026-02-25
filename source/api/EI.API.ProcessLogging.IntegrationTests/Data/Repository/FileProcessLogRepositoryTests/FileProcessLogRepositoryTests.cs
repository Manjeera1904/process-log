using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.Data.TestHelpers.Repository;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.FileProcessLogRepositoryTests;

[TestClass]
public class FileProcessLogRepositoryTests : BaseRepositoryTests<ProcessLogDbContext, FileProcessLogRepository, FileProcessLog>
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
    public async Task GetByProcessLog_ReturnsEmpty_WhenNoneFound_V1()
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
    public async Task GetAllAsync_ReturnsAll_V2()
    {
        var entity1 = BuildModel("one");
        var entity2 = BuildModel("two");
        await _context.AddRangeAsync(entity1, entity2);
        await _context.SaveChangesAsync();

        var result = (await _repository.GetAllAsync()).ToList();

        Assert.AreEqual(2, result.Count);
        Assert.IsTrue(result.Any(e => e.Id == entity1.Id));
        Assert.IsTrue(result.Any(e => e.Id == entity2.Id));
    }

    [TestMethod]
    public async Task GetByIdAsync_ReturnsEntity_V2()
    {
        var entity = BuildModel("one");
        await _context.AddAsync(entity);
        await _context.SaveChangesAsync();

        var result = await _repository.GetByIdAsync(entity.Id);

        Assert.IsNotNull(result);
        Assert.AreEqual(entity.Id, result!.Id);
    }

    [TestMethod]
    public async Task GetByIdAsync_ReturnsNull_WhenNotFound_V2()
    {
        var result = await _repository.GetByIdAsync(Guid.NewGuid());
        Assert.IsNull(result);
    }

    [TestMethod]
    public async Task Defaults_AreApplied_WhenV1EntityCreated_V2()
    {
        var entity = BuildModel("defaultTest");
        entity.PurposeName = null!;
        entity.ProcessStatus = null!;
        await _context.AddAsync(entity);
        await _context.SaveChangesAsync();

        var result = await _repository.GetByIdAsync(entity.Id);
        Assert.IsNotNull(result);
        Assert.AreEqual("Originating Contract", result!.PurposeName);
        Assert.AreEqual("New", result.ProcessStatus);
    }
}
