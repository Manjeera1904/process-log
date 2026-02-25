using EI.API.ProcessLogging.Data.Entities;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.ProcessLogMessageRepositoryTests;

public class ProcessLogMessageTestConfig
{
    public ActivityType ActivityType { get; set; } = default!;
    public ProcessStatus ProcessStatus { get; set; } = default!;
    public ProcessLog ProcessLog { get; set; } = default!;
}