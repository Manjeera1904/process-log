using EI.API.ProcessLogging.Data.Entities;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.ProcessLogRepositoryTests;

public class ProcessLogTestConfig
{
    public ActivityType ActivityType { get; set; } = default!;
    public ProcessStatus ProcessStatus { get; set; } = default!;
}