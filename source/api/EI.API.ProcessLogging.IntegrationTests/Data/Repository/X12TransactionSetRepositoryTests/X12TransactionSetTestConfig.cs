using EI.API.ProcessLogging.Data.Entities;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.X12TransactionSetRepositoryTests;

public class X12TransactionSetTestConfig
{
    public ProcessLog ProcessLog { get; set; } = default!;
    public FileProcessLog FileProcessLog { get; set; } = default!;
    public X12Interchange X12Interchange { get; set; } = default!;
    public X12FunctionalGroup X12FunctionalGroup { get; set; } = default!;
}