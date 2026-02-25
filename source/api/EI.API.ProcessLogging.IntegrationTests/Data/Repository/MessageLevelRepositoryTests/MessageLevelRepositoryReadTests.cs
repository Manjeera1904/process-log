using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.Data.TestHelpers.Repository;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.MessageLevelRepositoryTests;

[TestClass]
public class MessageLevelRepositoryReadTests : BaseRepositoryReadWithTranslationTests<ProcessLogDbContext, MessageLevelRepository, MessageLevel, MessageLevelTranslation>
{
    protected override string ConnectionStringName => ProcessLogDbContext.ConnectionStringName;

    protected override MessageLevel BuildModel(string label, string? cultureCode = null) =>
        MessageLevelTestHelpers.BuildMessageLevel(label);
}