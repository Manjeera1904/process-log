using Autofac;
using Autofac.Extras.AggregateService;
using EI.API.Cloud.Clients.Azure.Messaging.Versioning;
using EI.API.ProcessLogging.Worker.Messaging;
using EI.API.ProcessLogging.Worker.Model;
using EI.API.ProcessLogging.Worker.Services;
using EI.API.ProcessLogging.Worker.Tasks;

namespace EI.API.ProcessLogging.Worker.Startup;

public class WorkerModule : Module
{
    protected override void Load(ContainerBuilder builder)
    {
        builder.RegisterAggregateService<IMessageReceiverServices>();
        builder
            .RegisterType<ProcessLogService>()
            .As<IProcessLogService>()
            .InstancePerLifetimeScope();

        // Domain processors (pure logic)
        builder.RegisterType<MessageLogProcessor>().AsSelf().InstancePerDependency();
        builder.RegisterType<FileLogProcessor>().AsSelf().InstancePerDependency();

        builder.RegisterType<ServiceBusPublisher>()
       .As<IServiceBusPublisher>()
       .InstancePerLifetimeScope();

        builder.RegisterType<ApplicationEventPublisher>()
               .As<IApplicationEventPublisher>()
               .InstancePerDependency();

        builder.RegisterType<ProcessNotificationMessageDispatcher>()
        .As<IMessageBodyDispatcher<ProcessNotificationMessage>>()
        .SingleInstance();

        // Domain handlers (use cases)
        builder
            .RegisterType<ProcessNotificationHandler>()
            .As<IProcessNotificationHandler>()
            .InstancePerDependency();
        builder
            .RegisterType<ProcessNotificationEventHelper>()
            .AsSelf()
            .InstancePerDependency();
        // Message receivers (workers)
        builder
            .RegisterType<ProcessNotificationsMessageReceiver>()
            .As<IStartable>()
            .AsSelf()
            .SingleInstance();

        base.Load(builder);
    }
}
