using EI.API.ProcessLogging.Data;
using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.API.Service.Data.Helpers;
using EI.Data.TestHelpers.Repository;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.MessageLevelRepositoryTests;

[TestClass]
public class MessageLevelRepositoryTests : BaseRepositoryReadWithTranslationTests<ProcessLogDbContext, MessageLevelRepository, MessageLevel, MessageLevelTranslation>
{
    protected override string ConnectionStringName => ProcessLogDbContext.ConnectionStringName;

    protected override MessageLevel BuildModel(string label, string? cultureCode = null)
        => MessageLevelTestHelpers.BuildMessageLevel(label, cultureCode);

    [TestMethod]
    public async Task GetAsyncByType_ReturnsRecord()
    {
        // Arrange

        // Act
        var entity = await _repository.GetAsync(ProcessLogConstants.MessageLevel.Fatal, ServiceConstants.CultureCode.Default);

        // Assert
        Assert.IsNotNull(entity);
        Assert.AreEqual(ProcessLogConstants.MessageLevel.Fatal, entity.Level);
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