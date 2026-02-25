using EI.API.ProcessLogging.Data.Entities;
using EI.API.Service.Data.Helpers;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.ActivityTypeRepositoryTests;

public static class ActivityTypeTestHelpers
{
    public static ActivityType BuildActivityType(string label, string? cultureCode = null)
    {
        var id = Guid.NewGuid();
        var updatedBy = $"ActivityType-UnitTest-{label}";

        return new ActivityType
        {
            Id = id,
            Type = $"Test Type {Guid.NewGuid():N}",
            UpdatedBy = updatedBy,
            Translations =
                   [
                       new()
                       {
                           Id = id,
                           CultureCode = cultureCode ?? ServiceConstants.CultureCode.Default,
                           Name = $"ActivityType-UnitTest-{label}",
                           Description = $"Description of ActivityType-UnitTest-{label}",
                           UpdatedBy = updatedBy,
                       },
                   ]
        };
    }
}