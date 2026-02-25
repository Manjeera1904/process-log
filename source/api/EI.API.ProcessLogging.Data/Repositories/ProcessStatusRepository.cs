using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.Service.Data.Helpers.Platform;
using EI.API.Service.Data.Helpers.Repository;

namespace EI.API.ProcessLogging.Data.Repositories;

public interface IProcessStatusRepository : IReadRepositoryWithTranslation<ProcessStatus, ProcessStatusTranslation>
{
    Task<ProcessStatus?> GetAsync(string type, string cultureCode);
}

public class ProcessStatusRepository(IDatabaseClientFactory dbContextFactory, Guid clientId)
    : BaseReadRepositoryWithTranslation<ProcessLogDbContext, ProcessStatus, ProcessStatusTranslation>(dbContextFactory, clientId), IProcessStatusRepository
{
    public async Task<ProcessStatus?> GetAsync(string status, string cultureCode)
        => (await GetHelper(cultureCode, t => t.Status == status)).SingleOrDefault();
    protected override string DataSourceKey => ProcessLogDbContext.ConnectionStringName;
}
