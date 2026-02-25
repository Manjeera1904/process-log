using EI.API.ProcessLogging.Data.Context;
using EI.Data.TestHelpers.Repository;
using Microsoft.Extensions.Configuration;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository;

[TestClass, TestCategory("Integration")]
public static class AssemblySetup_MemoryDatabase
{
    internal static (IConfiguration Configuration, ProcessLogDbContext DbContext) Setup()
    {
        return AssemblySetupHelpers.Setup<ProcessLogDbContext>(ProcessLogDbContext.ConnectionStringName);
    }

    [AssemblyInitialize, TestCategory("Integration")]
    public static void AssemblyInit(TestContext context)
    {
        AssemblySetupHelpers.AssemblyInit<ProcessLogDbContext>(ProcessLogDbContext.ConnectionStringName);
    }

    [AssemblyCleanup, TestCategory("Integration")]
    public static void AssemblyCleanup()
    {
        AssemblySetupHelpers.AssemblyCleanup<ProcessLogDbContext>(ProcessLogDbContext.ConnectionStringName);
    }
}
