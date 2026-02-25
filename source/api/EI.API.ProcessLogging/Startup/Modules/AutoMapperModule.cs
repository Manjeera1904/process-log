using Autofac;
using AutoMapper;
using System.Reflection;

namespace EI.API.ProcessLogging.Startup.Modules;

public class AutoMapperModule : Autofac.Module
{
    protected override void Load(ContainerBuilder builder)
    {
        base.Load(builder);

        var mapperConfig = new MapperConfiguration(cfg =>
        {
            cfg.AddMaps(Assembly.GetExecutingAssembly());
        });

        IMapper mapper = new Mapper(mapperConfig);
        builder.RegisterInstance(mapper).As<IMapper>();
    }
}
