using EI.API.Cloud.Clients;
using EI.API.Service.Data.Helpers.Platform;
using Microsoft.Extensions.Configuration;

public interface IMessageReceiverServices
{
    IConfiguration Configuration { get; }
    IMessageClientFactory MessageClientFactory { get; }
    IDatabaseClientFactory DatabaseClientFactory { get; set; }
}
