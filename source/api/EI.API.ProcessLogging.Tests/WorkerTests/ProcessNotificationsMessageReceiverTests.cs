using EI.API.Cloud.Clients;
using EI.API.Cloud.Clients.Azure.Messaging.Versioning;
using EI.API.ProcessLogging.Worker.Model;
using EI.API.ProcessLogging.Worker.Services;
using EI.API.ProcessLogging.Worker.Tasks;
using Microsoft.Extensions.Logging;
using Moq;

namespace EI.API.ProcessLogging.Tests.WorkerTests.Tasks;

[TestClass]
public class ProcessNotificationsMessageReceiverTests
{
    private Mock<IMessageReceiverServices> _servicesMock = null!;
    private Mock<IMessageBodyDispatcher<ProcessNotificationMessage>> _dispatcher = null!;
    private Mock<IProcessNotificationHandler> _handlerMock = null!;
    private Mock<ILogger<ProcessNotificationsMessageReceiver>> _loggerMock = null!;
    private ProcessNotificationsMessageReceiver _sut = null!;

    [TestInitialize]
    public void Setup()
    {
        _servicesMock = new Mock<IMessageReceiverServices>();
        _dispatcher = new Mock<IMessageBodyDispatcher<ProcessNotificationMessage>>();
        _handlerMock = new Mock<IProcessNotificationHandler>();
        _loggerMock = new Mock<ILogger<ProcessNotificationsMessageReceiver>>();
        _sut = new ProcessNotificationsMessageReceiver(
            _servicesMock.Object,
            _dispatcher.Object,
            _handlerMock.Object,
            _loggerMock.Object
        );
    }

    [TestMethod]
    public void TopicName_ShouldBeExpected()
    {
        var topic = typeof(ProcessNotificationsMessageReceiver)
            .GetProperty(
                "TopicName",
                System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance
            )!
            .GetValue(_sut);
        Assert.AreEqual("process-logging", topic);
    }

    [TestMethod]
    public async Task HandleMessageAsync_ShouldInvokeHandler()
    {
        var header = new MessageHeader();
        var msg = new ProcessNotificationMessage();
        var clientId = Guid.NewGuid();
        var corrId = Guid.NewGuid();

        await _sut.InvokeHandle(header, msg, clientId, corrId);

        _handlerMock.Verify(h => h.HandleAsync(header, msg, clientId, corrId), Times.Once);
    }
}

internal static class ReceiverExtensions
{
    public static Task InvokeHandle(
        this ProcessNotificationsMessageReceiver sut,
        MessageHeader header,
        ProcessNotificationMessage msg,
        Guid c,
        Guid p
    ) =>
        (Task)
            typeof(ProcessNotificationsMessageReceiver)
                .GetMethod(
                    "HandleMessageAsync",
                    System.Reflection.BindingFlags.NonPublic
                        | System.Reflection.BindingFlags.Instance
                )!
                .Invoke(sut, new object[] { header, msg, c, p })!;
}
