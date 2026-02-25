using EI.API.Cloud.Clients.Azure;
using EI.API.ProcessLogging.Data.App;
using EI.API.ProcessLogging.Documentation;
using EI.API.ProcessLogging.Middlewares;
using EI.API.ProcessLogging.Startup;

var builder = WebApplication.CreateBuilder(args);

builder.AddKeyVaultConfiguration();

// Wire up common .NET Aspire App Builder basics
builder.AddServiceDefaults(
    addSwaggerGen: true,
    swaggerDocs: () =>
        DocumentationLoader.GetXmlDocs()
        ?? throw new InvalidOperationException("XML documentation not found."),
    useApiAuthentication: true,
    permissions: Permissions.AllPermissions,
    applicationName: "ProcessLogging"
);

if (builder.Environment.IsDevelopment())
{
    builder.Logging.AddConsole();
}

// Add HTTP Filter that requires a Client ID header
// TODO: builder.Services.AddClientIdFiltering();

// .NET Aspire Service Discovery:
// builder.AddSqlServerDbContext<ProcessLogDbContext>(ProcessLogDbContext.ConnectionStringName);

// Add this services' dependencies to the container.
DependencyInjection.Bootstrap(builder.Configuration, builder);

var app = builder.Build();

// Middlewares handle exceptions
app.UseMiddleware<ExceptionHandlingMiddleware>();

// Wire up common .NET Aspire App basics
app.AddApplicationDefaults();

await DatabaseMigrations.Migrate(app);

app.Run();
