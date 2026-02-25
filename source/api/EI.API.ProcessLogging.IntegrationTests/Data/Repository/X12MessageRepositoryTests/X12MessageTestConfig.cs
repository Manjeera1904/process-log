using EI.API.ProcessLogging.Data.Entities;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.X12MessageRepositoryTests;

public class X12MessageTestConfig
{
    public ActivityType ActivityType { get; set; } = default!;
    public ProcessStatus ProcessStatus { get; set; } = default!;
    public ProcessLog ProcessLog { get; set; } = default!;
    public FileProcessLog FileProcessLog { get; set; } = default!;
    public X12Interchange X12Interchange { get; set; } = default!;
    public X12FunctionalGroup X12FunctionalGroup { get; set; } = default!;
    public X12TransactionSet X12TransactionSet { get; set; } = default!;
}