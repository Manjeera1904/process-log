using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.Service.Data.Helpers.Platform;
using EI.API.Service.Data.Helpers.Repository;
using Microsoft.EntityFrameworkCore;

namespace EI.API.ProcessLogging.Data.Repositories;

public interface IX12TransactionSetRepository : IReadWriteRepository<X12TransactionSet>
{
    Task<IEnumerable<X12TransactionSet>> GetByFunctionalGroup(Guid x12FunctionalGroupId);
}

public class X12TransactionSetRepository(IDatabaseClientFactory dbContextFactory, Guid clientId)
    : BaseRepository<ProcessLogDbContext, X12TransactionSet>(dbContextFactory, clientId), IX12TransactionSetRepository
{
    public async Task<IEnumerable<X12TransactionSet>> GetByFunctionalGroup(Guid x12FunctionalGroupId)
        => await Exec(async (_, entitySet) =>
                          await entitySet.Where(entity => entity.X12FunctionalGroupId == x12FunctionalGroupId).ToListAsync());
    protected override string DataSourceKey => ProcessLogDbContext.ConnectionStringName;
}
