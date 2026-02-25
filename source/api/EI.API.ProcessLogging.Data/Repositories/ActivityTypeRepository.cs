using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.Service.Data.Helpers.Platform;
using EI.API.Service.Data.Helpers.Repository;

namespace EI.API.ProcessLogging.Data.Repositories;
public interface IActivityTypeRepository : IReadRepositoryWithTranslation<ActivityType, ActivityTypeTranslation>
{
    Task<ActivityType?> GetAsync(string type, string cultureCode);
}

public class ActivityTypeRepository(IDatabaseClientFactory dbContextFactory, Guid clientId)
    : BaseReadRepositoryWithTranslation<ProcessLogDbContext, ActivityType, ActivityTypeTranslation>(dbContextFactory, clientId), IActivityTypeRepository
{
    public async Task<ActivityType?> GetAsync(string type, string cultureCode)
        => (await GetHelper(cultureCode, t => t.Type == type)).SingleOrDefault();

    protected override string DataSourceKey => ProcessLogDbContext.ConnectionStringName;
}
