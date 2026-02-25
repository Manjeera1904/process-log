using EI.API.ProcessLogging.Data;
using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.API.Service.Data.Helpers;
using EI.Data.TestHelpers.Repository;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.X12StatusRepositoryTests;

[TestClass]
public class X12StatusRepositoryTests : BaseRepositoryReadWithTranslationTests<ProcessLogDbContext, X12StatusRepository, X12Status, X12StatusTranslation>
{
    protected override string ConnectionStringName => ProcessLogDbContext.ConnectionStringName;

    protected override X12Status BuildModel(string label, string? cultureCode = null)
        => X12StatusTestHelpers.BuildX12Status(label, cultureCode);

    [TestMethod]
    public async Task GetAsyncByType_ReturnsRecord()
    {
        // Arrange

        // Act
        var entity = await _repository.GetAsync(ProcessLogConstants.X12Status.Accepted, ServiceConstants.CultureCode.Default);

        // Assert
        Assert.IsNotNull(entity);
        Assert.AreEqual(ProcessLogConstants.X12Status.Accepted, entity.Status);
        Assert.IsNotNull(entity.Translations);
        Assert.AreEqual(1, entity.Translations.Count);
    }

    [TestMethod]
    public async Task GetAsyncByType_NotExistingReturnsNull()
    {
        // Arrange

        // Act
        var entity = await _repository.GetAsync("DOES NOT EXIST", "ALSO DOES NOT EXIST");

        // Assert
        Assert.IsNull(entity);
    }
}