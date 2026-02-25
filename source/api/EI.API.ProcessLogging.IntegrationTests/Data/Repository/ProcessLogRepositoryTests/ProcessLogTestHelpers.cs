using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.API.Service.Data.Helpers.Platform;
using Moq;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.ProcessLogRepositoryTests;

public static class ProcessLogTestHelpers
{
    public static ProcessLogTestConfig BuildTestConfig(ProcessLogDbContext context)
    {
        var activityTypeId = Guid.NewGuid();
        var activityTypeType = ((ulong) DateTime.Now.ToBinary()).ToString();

        var activityType = context.ActivityTypes.Add(new ActivityType
        {
            Id = activityTypeId,
            Type = activityTypeType,
            UpdatedBy = "ProcessLog-UnitTest",
            IsInbound = Random.Shared.Next() % 2 == 0,
            IsOutbound = Random.Shared.Next() % 2 == 0,
            Translations =
                                                         [
                                                             new ActivityTypeTranslation
                                                             {
                                                                 Id = activityTypeId,
                                                                 CultureCode = Service.Data.Helpers.ServiceConstants.CultureCode.Default,
                                                                 Name = $"Unit Test {activityTypeType}",
                                                                 Description = $"Unit Test {activityTypeType}",
                                                                 UpdatedBy = "ProcessLog-UnitTest",
                                                             }
                                                         ]
        }).Entity;

        var processStatusId = Guid.NewGuid();
        var processStatusStatus = ((ulong) DateTime.Now.ToBinary()).ToString();

        var processStatus = context.ProcessStatuses.Add(new ProcessStatus
        {
            Id = processStatusId,
            Status = processStatusStatus,
            UpdatedBy = "ProcessLog-UnitTest",
            Translations =
                                                            [
                                                                new ProcessStatusTranslation
                                                                {
                                                                    Id = processStatusId,
                                                                    CultureCode = Service.Data.Helpers.ServiceConstants.CultureCode.Default,
                                                                    Name = $"Unit Test {processStatusStatus}",
                                                                    Description = $"Unit Test {processStatusStatus}",
                                                                    UpdatedBy = "ProcessLog-UnitTest",
                                                                }
                                                            ]
        }).Entity;

        context.SaveChanges();

        return new ProcessLogTestConfig
        {
            ActivityType = activityType,
            ProcessStatus = processStatus,
        };
    }

    public static ProcessLog BuildProcessLog(string activityType, string processStatus, string label) =>
        new()
        {
            Id = Guid.NewGuid(),
            Status = processStatus,
            Type = activityType,
            StartTimestamp = DateTime.UtcNow,
            LastUpdatedTimestamp = DateTime.UtcNow,
            UpdatedBy = $"ProcessLog-UnitTest-{label}",
        };

    public static MockProcessLogRepository BuildRepo(ProcessLogDbContext context)
    {
        var mockFactory = new Mock<IDatabaseClientFactory>();
        mockFactory.Setup(f => f.GetDbContext<ProcessLogDbContext>(It.IsAny<Guid>(), It.IsAny<string>())).ReturnsAsync(context);
        var factory = mockFactory.Object;

        return new MockProcessLogRepository(factory, Guid.NewGuid());
    }

    public class MockProcessLogRepository(IDatabaseClientFactory dbContextFactory, Guid clientId)
        : ProcessLogRepository(dbContextFactory, clientId)
    {
        public Mock<IProcessLogMessageRepository> MockMessageRepo { get; } = new();

        protected override IProcessLogMessageRepository GetMessageRepository()
            => MockMessageRepo.Object;
    }
}