using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.Service.Data.Helpers.Platform;
using EI.API.Service.Data.Helpers.Repository;
using Microsoft.EntityFrameworkCore;

namespace EI.API.ProcessLogging.Data.Repositories;

public interface IX12FunctionalGroupRepository : IReadWriteRepository<X12FunctionalGroup>
{
    Task<IEnumerable<X12FunctionalGroup>> GetByInterchangeAsync(Guid x12InterchangeId);
}

public class X12FunctionalGroupRepository(IDatabaseClientFactory dbContextFactory, Guid clientId)
    : BaseRepository<ProcessLogDbContext, X12FunctionalGroup>(dbContextFactory, clientId), IX12FunctionalGroupRepository
{
    public async Task<IEnumerable<X12FunctionalGroup>> GetByInterchangeAsync(Guid x12InterchangeId)
        => await Exec(async (_, entitySet) =>
                          await entitySet.Where(entity => entity.X12InterchangeId == x12InterchangeId).ToListAsync());
    protected override string DataSourceKey => ProcessLogDbContext.ConnectionStringName;
}
