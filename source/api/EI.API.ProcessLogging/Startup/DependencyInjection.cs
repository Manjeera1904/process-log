using Autofac;
using Autofac.Extensions.DependencyInjection;
using EI.API.Cloud.Clients.Azure;
using EI.API.Platform.Sdk.Startup;
using EI.API.ProcessLogging.Data.Startup;
using EI.API.ProcessLogging.Startup.Modules;
using EI.API.ProcessLogging.Worker.Startup;

namespace EI.API.ProcessLogging.Startup;

public static class DependencyInjection
{
    public static void Bootstrap(IConfigurationRoot configuration, WebApplicationBuilder builder)
    {
        builder.Host
               .UseServiceProviderFactory(new AutofacServiceProviderFactory())
               .ConfigureContainer<ContainerBuilder>(ConfigureDependencies);
    }

    public static void ConfigureDependencies(ContainerBuilder containerBuilder)
    {
        // Register data access types:
        containerBuilder.RegisterModule<ProcessLogDataModule>();

        // Register background workers:
        containerBuilder.RegisterModule<WorkerModule>();

        // Register other services here
        containerBuilder.RegisterModule<AutoMapperModule>();
        containerBuilder.RegisterModule<ControllersModule>();

        // Register Platform SDK client
        containerBuilder.RegisterModule<PlatformClientModule>();

        // Cloud clients:
        containerBuilder.RegisterModule<AzureModule>();
    }
}
