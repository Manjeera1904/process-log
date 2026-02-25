using EI.API.ProcessLogging.Data.Entities;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.X12InterchangeRepositoryTests;

public class X12InterchangeTestConfig
{
    public ProcessLog ProcessLog { get; set; } = default!;
    public FileProcessLog FileProcessLog { get; set; } = default!;
}