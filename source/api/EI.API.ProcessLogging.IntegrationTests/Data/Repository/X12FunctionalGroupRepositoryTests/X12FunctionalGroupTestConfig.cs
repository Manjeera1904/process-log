using EI.API.ProcessLogging.Data.Entities;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.X12FunctionalGroupRepositoryTests;

public class X12FunctionalGroupTestConfig
{
    public ProcessLog ProcessLog { get; set; } = default!;
    public FileProcessLog FileProcessLog { get; set; } = default!;
    public X12Interchange X12Interchange { get; set; } = default!;
}