using System.Net;
using System.Text.Json;

namespace EI.API.ProcessLogging.Middlewares;

public class ExceptionHandlingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<ExceptionHandlingMiddleware> _logger;

    public ExceptionHandlingMiddleware(
        RequestDelegate next,
        ILogger<ExceptionHandlingMiddleware> logger
    )
    {
        _next = next;
        _logger = logger;
    }

    public async Task Invoke(HttpContext context)
    {
        try
        {
            await _next(context);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "An unexpected error occurred. Please try again later.");

            context.Response.StatusCode = (int) HttpStatusCode.InternalServerError;
            context.Response.ContentType = "application/json";

            var problem = new
            {
                status = context.Response.StatusCode,
                title = "An unexpected error occurred. Please try again later.",
                detail = ex.Message,
            };

            await context.Response.WriteAsync(JsonSerializer.Serialize(problem));
        }
    }
}
