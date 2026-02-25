using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.Data.TestHelpers.Repository;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.X12StatusRepositoryTests;

[TestClass]
public class X12StatusRepositoryReadTests : BaseRepositoryReadWithTranslationTests<ProcessLogDbContext, X12StatusRepository, X12Status, X12StatusTranslation>
{
    protected override string ConnectionStringName => ProcessLogDbContext.ConnectionStringName;

    protected override X12Status BuildModel(string label, string? cultureCode = null) =>
        X12StatusTestHelpers.BuildX12Status(label);
}