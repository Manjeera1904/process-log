using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.Service.Data.Helpers.Platform;
using EI.API.Service.Data.Helpers.Repository;
using Microsoft.EntityFrameworkCore;

namespace EI.API.ProcessLogging.Data.Repositories;

public interface IFileProcessLogRepository : IReadWriteRepository<FileProcessLog>
{
    Task<IEnumerable<FileProcessLog>> GetByProcessLogAsync(Guid processLogId);
    Task<List<FileProcessLog>> GetAllAsync();
    Task<FileProcessLog?> GetByIdAsync(Guid id);
}

public class FileProcessLogRepository(
    IDatabaseClientFactory dbContextFactory,
    Guid clientId)
    : BaseRepository<ProcessLogDbContext, FileProcessLog>(dbContextFactory, clientId),
      IFileProcessLogRepository
{
    public async Task<List<FileProcessLog>> GetAllAsync()
        => await Exec(async (_, entitySet) =>
        {
            var list = await entitySet
                .ToListAsync();

            return list;
        });

    public async Task<FileProcessLog?> GetByIdAsync(Guid id)
        => await Exec(async (_, entitySet) =>
        {
            var entity = await entitySet
                .FirstOrDefaultAsync(f => f.Id == id);

            return entity;
        });

    public async Task<IEnumerable<FileProcessLog>> GetByProcessLogAsync(Guid processLogId)
        => await Exec(async (_, entitySet) =>
                          await entitySet.Where(entity => entity.ProcessLogId == processLogId).ToListAsync());

    protected override string DataSourceKey => ProcessLogDbContext.ConnectionStringName;
}
