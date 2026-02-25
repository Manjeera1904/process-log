using EI.API.ProcessLogging.Data;
using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.API.Service.Data.Helpers;
using EI.Data.TestHelpers.Repository;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.ProcessStatusRepositoryTests;

[TestClass]
public class ProcessStatusRepositoryTests : BaseRepositoryReadWithTranslationTests<ProcessLogDbContext, ProcessStatusRepository, ProcessStatus, ProcessStatusTranslation>
{
    protected override string ConnectionStringName => ProcessLogDbContext.ConnectionStringName;

    protected override ProcessStatus BuildModel(string label, string? cultureCode = null)
        => ProcessStatusTestHelpers.BuildProcessStatus(label, cultureCode);

    [TestMethod]
    public async Task GetAsyncByType_ReturnsRecord()
    {
        // Arrange

        // Act
        var entity = await _repository.GetAsync(ProcessLogConstants.ProcessStatus.InProgress, ServiceConstants.CultureCode.Default);

        // Assert
        Assert.IsNotNull(entity);
        Assert.AreEqual(ProcessLogConstants.ProcessStatus.InProgress, entity.Status);
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