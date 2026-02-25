using EI.API.ProcessLogging.Data.Context;
using Microsoft.Data.SqlClient;
using Microsoft.EntityFrameworkCore;
using Polly;

namespace EI.API.ProcessLogging.Startup;

public static class DatabaseMigrations
{
    public static Task Migrate(WebApplication context)
    {
        return Task.CompletedTask;
        /*
        var retryPolicy = Policy
                          .Handle<InvalidOperationException>()
                          .Or<SqlException>()
                          .WaitAndRetryAsync(retryCount: 5, sleepDurationProvider: attemptNumber => TimeSpan.FromSeconds(attemptNumber));

        await retryPolicy.ExecuteAsync(async () =>
                                       {
                                           using var scope = context.Services.CreateScope();
                                           var dbContext = scope.ServiceProvider.GetRequiredService<ProcessLogDbContext>();
                                           await dbContext.Database.MigrateAsync();
                                       });
        */
    }
}