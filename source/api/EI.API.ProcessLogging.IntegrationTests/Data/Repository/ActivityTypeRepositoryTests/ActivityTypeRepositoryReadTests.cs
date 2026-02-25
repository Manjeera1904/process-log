using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.Data.TestHelpers.Repository;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.ActivityTypeRepositoryTests;

[TestClass]
public class ActivityTypeRepositoryReadTests : BaseRepositoryReadWithTranslationTests<ProcessLogDbContext, ActivityTypeRepository, ActivityType, ActivityTypeTranslation>
{
    protected override string ConnectionStringName => ProcessLogDbContext.ConnectionStringName;

    protected override ActivityType BuildModel(string label, string? cultureCode = null) =>
        ActivityTypeTestHelpers.BuildActivityType(label);
}