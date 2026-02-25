using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.API.Service.Data.Helpers.Platform;
using EI.API.Service.Data.Helpers.Repository;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.ProcessLogMessageRepositoryTests;

public class TestWriteableProcessLogMessageRepository(IDatabaseClientFactory dbContextFactory, Guid clientId)
    : ProcessLogMessageRepository(dbContextFactory, clientId), IReadWriteRepository<ProcessLogMessage>
{
    // Class that forces the Insert/Update methods to be "available" for testing
}