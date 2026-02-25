using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.Data.TestHelpers.Repository;
using Microsoft.EntityFrameworkCore;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.X12MessageRepositoryTests;

[TestClass]
public class X12MessageRepositoryUpdateTests : BaseRepositoryTests<ProcessLogDbContext, X12MessageRepository, X12Message>
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