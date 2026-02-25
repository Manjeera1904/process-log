using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.Service.Data.Helpers.Platform;
using EI.API.Service.Data.Helpers.Repository;
using Microsoft.EntityFrameworkCore;

namespace EI.API.ProcessLogging.Data.Repositories;

public interface IX12MessageRepository : IReadWriteRepository<X12Message>
{
    Task<IEnumerable<X12Message>> GetByInterchangeAsync(Guid x12InterchangeId);
    Task<IEnumerable<X12Message>> GetByInterchangeAsync(Guid x12InterchangeId, string messageLevel);
    Task<IEnumerable<X12Message>> GetByFunctionalGroupAsync(Guid x12FunctionalGroupId);
    Task<IEnumerable<X12Message>> GetByFunctionalGroupAsync(Guid x12FunctionalGroupId, string messageLevel);
    Task<IEnumerable<X12Message>> GetByTransactionSetAsync(Guid x12TransactionSetId);
    Task<IEnumerable<X12Message>> GetByTransactionSetAsync(Guid x12TransactionSetId, string messageLevel);
}

public class X12MessageRepository(IDatabaseClientFactory dbContextFactory, Guid clientId)
    : BaseRepository<ProcessLogDbContext, X12Message>(dbContextFactory, clientId), IX12MessageRepository
{
    public async Task<IEnumerable<X12Message>> GetByInterchangeAsync(Guid x12InterchangeId)
        => await Exec(async (_, entitySet) => await entitySet.Where(entity => entity.X12InterchangeId == x12InterchangeId).ToListAsync());

    public async Task<IEnumerable<X12Message>> GetByInterchangeAsync(Guid x12InterchangeId, string messageLevel)
        => await Exec(async (_, entitySet) => await entitySet.Where(entity => entity.X12InterchangeId == x12InterchangeId && entity.Level == messageLevel).ToListAsync());

    public async Task<IEnumerable<X12Message>> GetByFunctionalGroupAsync(Guid x12FunctionalGroupId)
        => await Exec(async (_, entitySet) => await entitySet.Where(entity => entity.X12FunctionalGroupId == x12FunctionalGroupId).ToListAsync());

    public async Task<IEnumerable<X12Message>> GetByFunctionalGroupAsync(Guid x12FunctionalGroupId, string messageLevel)
        => await Exec(async (_, entitySet) => await entitySet.Where(entity => entity.X12FunctionalGroupId == x12FunctionalGroupId && entity.Level == messageLevel).ToListAsync());

    public async Task<IEnumerable<X12Message>> GetByTransactionSetAsync(Guid x12TransactionSetId)
        => await Exec(async (_, entitySet) => await entitySet.Where(entity => entity.X12TransactionSetId == x12TransactionSetId).ToListAsync());

    public async Task<IEnumerable<X12Message>> GetByTransactionSetAsync(Guid x12TransactionSetId, string messageLevel)
        => await Exec(async (_, entitySet) => await entitySet.Where(entity => entity.X12TransactionSetId == x12TransactionSetId && entity.Level == messageLevel).ToListAsync());

    // Disallow updates
    public override Task<X12Message> UpdateAsync(X12Message entity)
        => Task.FromException<X12Message>(new NotSupportedException("Event Messages are insert-only"));

    protected override string DataSourceKey => ProcessLogDbContext.ConnectionStringName;
}
