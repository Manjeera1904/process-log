using EI.API.ProcessLogging.Data.Entities;
using EI.API.Service.Data.Helpers;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.X12StatusRepositoryTests;

public static class X12StatusTestHelpers
{
    public static X12Status BuildX12Status(string label, string? cultureCode = null)
    {
        var id = Guid.NewGuid();
        var updatedBy = $"X12Status-UnitTest-{label}";

        return new X12Status
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
                           Name = $"X12Status-UnitTest-{label}",
                           Description = $"Description of X12Status-UnitTest-{label}",
                           UpdatedBy = updatedBy,
                       },
                   ]
        };
    }
}