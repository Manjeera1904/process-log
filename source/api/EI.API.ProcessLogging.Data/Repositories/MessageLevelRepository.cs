using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.Service.Data.Helpers.Platform;
using EI.API.Service.Data.Helpers.Repository;

namespace EI.API.ProcessLogging.Data.Repositories;

public interface IMessageLevelRepository : IReadRepositoryWithTranslation<MessageLevel, MessageLevelTranslation>
{
    Task<MessageLevel?> GetAsync(string type, string cultureCode);
}

public class MessageLevelRepository(IDatabaseClientFactory dbContextFactory, Guid clientId)
    : BaseReadRepositoryWithTranslation<ProcessLogDbContext, MessageLevel, MessageLevelTranslation>(dbContextFactory, clientId), IMessageLevelRepository
{
    public async Task<MessageLevel?> GetAsync(string level, string cultureCode)
        => (await GetHelper(cultureCode, t => t.Level == level)).SingleOrDefault();
    protected override string DataSourceKey => ProcessLogDbContext.ConnectionStringName;
}
