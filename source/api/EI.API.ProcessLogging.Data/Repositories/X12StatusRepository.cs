using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.Service.Data.Helpers.Platform;
using EI.API.Service.Data.Helpers.Repository;

namespace EI.API.ProcessLogging.Data.Repositories;

public interface IX12StatusRepository : IReadRepositoryWithTranslation<X12Status, X12StatusTranslation>
{
    Task<X12Status?> GetAsync(string type, string cultureCode);
}

public class X12StatusRepository(IDatabaseClientFactory dbContextFactory, Guid clientId)
    : BaseReadRepositoryWithTranslation<ProcessLogDbContext, X12Status, X12StatusTranslation>(dbContextFactory, clientId), IX12StatusRepository
{
    public async Task<X12Status?> GetAsync(string status, string cultureCode)
        => (await GetHelper(cultureCode, t => t.Status == status)).SingleOrDefault();
    protected override string DataSourceKey => ProcessLogDbContext.ConnectionStringName;
}
