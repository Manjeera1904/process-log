using Autofac;
using EI.API.ProcessLogging.Data.Context;
using EI.API.Service.Data.Helpers.Startup;

namespace EI.API.ProcessLogging.Data.Startup;

public class ProcessLogDataModule : BaseDataModule<ProcessLogDbContext>
{
    protected override void Load(ContainerBuilder builder)
    {
        base.Load(builder);

        var assembly = GetType().Assembly;
        var repos = assembly.GetTypes()
                            .Where(type => type.Name.EndsWith("Repository"))
                            .Where(type => !type.IsInterface)
                            .Where(type => !type.IsAbstract)
                            .ToList();

        foreach (var repo in repos)
        {
            builder.RegisterType(repo)
                   .AsImplementedInterfaces()
                   .InstancePerLifetimeScope()
                   // .WithParameter(ClientIdParameterSelector, ClientIdValueSelector)
                   ;
        }
    }
}