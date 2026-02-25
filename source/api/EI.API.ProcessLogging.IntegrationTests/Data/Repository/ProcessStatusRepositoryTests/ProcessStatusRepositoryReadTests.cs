using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.Data.TestHelpers.Repository;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.ProcessStatusRepositoryTests;

[TestClass]
public class ProcessStatusRepositoryReadTests : BaseRepositoryReadWithTranslationTests<ProcessLogDbContext, ProcessStatusRepository, ProcessStatus, ProcessStatusTranslation>
{
    protected override string ConnectionStringName => ProcessLogDbContext.ConnectionStringName;

    protected override ProcessStatus BuildModel(string label, string? cultureCode = null) =>
        ProcessStatusTestHelpers.BuildProcessStatus(label);
}