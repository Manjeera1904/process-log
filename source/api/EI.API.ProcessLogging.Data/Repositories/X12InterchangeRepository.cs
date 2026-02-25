using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.Service.Data.Helpers.Platform;
using EI.API.Service.Data.Helpers.Repository;
using Microsoft.EntityFrameworkCore;

namespace EI.API.ProcessLogging.Data.Repositories;

public interface IX12InterchangeRepository : IReadWriteRepository<X12Interchange>
{
    Task<IEnumerable<X12Interchange>> GetByProcessLogAsync(Guid processLogId);
    Task<IEnumerable<X12Interchange>> GetByFileProcessLogAsync(Guid fileProcessLogId);
}

public class X12InterchangeRepository(IDatabaseClientFactory dbContextFactory, Guid clientId)
    : BaseRepository<ProcessLogDbContext, X12Interchange>(dbContextFactory, clientId), IX12InterchangeRepository
{
    public async Task<IEnumerable<X12Interchange>> GetByProcessLogAsync(Guid processLogId)
        => await Exec(async (dbContext, _) =>
                          await
                              (
                                  from interchange in dbContext.X12Interchanges
                                  join fileProcessLog in dbContext.FileProcessLogs on interchange.FileProcessLogId equals fileProcessLog.Id
                                  where fileProcessLog.ProcessLogId == processLogId
                                  select interchange
                              ).ToListAsync());

    public async Task<IEnumerable<X12Interchange>> GetByFileProcessLogAsync(Guid fileProcessLogId)
        => await Exec(async (_, entitySet) =>
                          await entitySet.Where(entity => entity.FileProcessLogId == fileProcessLogId).ToListAsync());

    protected override string DataSourceKey => ProcessLogDbContext.ConnectionStringName;
}
