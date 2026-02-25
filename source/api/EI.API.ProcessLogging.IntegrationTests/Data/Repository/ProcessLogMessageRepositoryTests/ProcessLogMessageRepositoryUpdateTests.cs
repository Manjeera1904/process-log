using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.Data.TestHelpers.Repository;
using Microsoft.EntityFrameworkCore;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.ProcessLogMessageRepositoryTests;

[TestClass]
public class ProcessLogMessageRepositoryUpdateTests : BaseRepositoryTests<ProcessLogDbContext, TestWriteableProcessLogMessageRepository, ProcessLogMessage>
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
    [ExpectedException(typeof(NotSupportedException))]
    public async Task UpdateAsync_IsNotImplemented()
    {
        // Arrange
        var entity = BuildModel("1");
        await DbSet.AddAsync(entity);
        await _context.SaveChangesAsync();

        var updatedBy = nameof(UpdateAsync_IsNotImplemented);
        entity.UpdatedBy = updatedBy;

        // Act
        await _repository.UpdateAsync(entity);
        _ = await DbSet.FindAsync(entity.Id);

        // Assert
        Assert.Fail($"Should have thrown a ${nameof(DbUpdateConcurrencyException)}");
    }
}