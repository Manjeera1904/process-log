using EI.API.ProcessLogging.Data.Entities;
using EI.API.Service.Data.Helpers;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.MessageLevelRepositoryTests;

public static class MessageLevelTestHelpers
{
    public static MessageLevel BuildMessageLevel(string label, string? cultureCode = null)
    {
        var id = Guid.NewGuid();
        var updatedBy = $"MessageLevel-UnitTest-{label}";

        return new MessageLevel
        {
            Id = id,
            Level = $"Test Level {Guid.NewGuid():N}",
            UpdatedBy = updatedBy,
            Translations =
                   [
                       new()
                       {
                           Id = id,
                           CultureCode = cultureCode ?? ServiceConstants.CultureCode.Default,
                           Name = $"MessageLevel-UnitTest-{label}",
                           Description = $"Description of MessageLevel-UnitTest-{label}",
                           UpdatedBy = updatedBy,
                       },
                   ]
        };
    }
}