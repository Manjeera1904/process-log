using EI.API.ProcessLogging.Data.Entities;
using EI.API.Service.Data.Helpers;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.ProcessStatusRepositoryTests;

public static class ProcessStatusTestHelpers
{
    public static ProcessStatus BuildProcessStatus(string label, string? cultureCode = null)
    {
        var id = Guid.NewGuid();
        var updatedBy = $"ProcessStatus-UnitTest-{label}";

        return new ProcessStatus
        {
            Id = id,
            Status = $"Test Status {Guid.NewGuid():N}",
            UpdatedBy = updatedBy,
            Translations =
                   [
                       new()
                       {
                           Id = id,
                           CultureCode = cultureCode ?? ServiceConstants.CultureCode.Default,
                           Name = $"ProcessStatus-UnitTest-{label}",
                           Description = $"Description of ProcessStatus-UnitTest-{label}",
                           UpdatedBy = updatedBy,
                       },
                   ]
        };
    }
}