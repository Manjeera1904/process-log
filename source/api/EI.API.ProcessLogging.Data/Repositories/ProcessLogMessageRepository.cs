using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.Service.Data.Helpers.Platform;
using EI.API.Service.Data.Helpers.Repository;
using Microsoft.EntityFrameworkCore;

namespace EI.API.ProcessLogging.Data.Repositories;

public interface IProcessLogMessageRepository : IReadWriteRepository<ProcessLogMessage>
{
    Task<IEnumerable<ProcessLogMessage>> GetByProcessLogAsync(Guid processLogId);
    Task<IEnumerable<ProcessLogMessage>> GetByProcessLogAsync(Guid processLogId, string messageLevel);
    Task<List<ProcessLogMessage>> GetAllAsync();
    Task<ProcessLogMessage?> GetByIdAsync(Guid id);
}

public class ProcessLogMessageRepository(IDatabaseClientFactory dbContextFactory, Guid clientId)
    : BaseRepository<ProcessLogDbContext, ProcessLogMessage>(dbContextFactory, clientId),
      IProcessLogMessageRepository
{
    public async Task<List<ProcessLogMessage>> GetAllAsync()
        => await Exec(async (_, entitySet) =>
            await entitySet
                .ToListAsync());

    public async Task<ProcessLogMessage?> GetByIdAsync(Guid id)
        => await Exec(async (_, entitySet) =>
            await entitySet
                .FirstOrDefaultAsync(m => m.Id == id));

    public async Task<IEnumerable<ProcessLogMessage>> GetByProcessLogAsync(Guid processLogId)
        => await Exec(async (_, entitySet) =>
                          await entitySet.Where(entity => entity.ProcessLogId == processLogId).ToListAsync());

    public async Task<IEnumerable<ProcessLogMessage>> GetByProcessLogAsync(Guid processLogId, string messageLevel)
        => await Exec(async (_, entitySet) =>
                          await entitySet.Where(entity => entity.ProcessLogId == processLogId && entity.Level == messageLevel).ToListAsync());

    // Disallow updates -- they're not exposed in the interface, so this is just a safety net
    public override Task<ProcessLogMessage> UpdateAsync(ProcessLogMessage entity)
        => Task.FromException<ProcessLogMessage>(
            new NotSupportedException("Event Messages are insert-only"));

    protected override string DataSourceKey => ProcessLogDbContext.ConnectionStringName;
}
