using EI.API.ProcessLogging.Worker.Model;
using System.Text.Json;

namespace EI.API.ProcessLogging.Tests.WorkerTests;

[TestClass]
public class ProcessNotificationMessageDispatcherTests
{
    private ProcessNotificationMessageDispatcher _sut = null!;

    [TestInitialize]
    public void Setup()
    {
        _sut = new ProcessNotificationMessageDispatcher();
    }

    [TestMethod]
    public void SupportedVersions_ShouldContainOnlyVersion_3_0()
    {
        // Act
        var supportedVersions = _sut.SupportedVersions;

        // Assert
        CollectionAssert.AreEquivalent(
            new[] { "3.0" },
            supportedVersions.ToArray()
        );
    }

    [TestMethod]
    public void Deserialize_WithSupportedVersion_ShouldReturnMessage()
    {
        // Arrange
        var json = JsonSerializer.Serialize(new
        {
            EventId = Guid.NewGuid(),
            EventType = "TestEvent",
            Timestamp = DateTime.UtcNow
        });

        // Act
        var result = _sut.Deserialize(json, "3.0");

        // Assert
        Assert.IsNotNull(result);
        Assert.IsInstanceOfType(result, typeof(ProcessNotificationMessage));
    }

    [TestMethod]
    public void Deserialize_WithUnsupportedVersion_ShouldThrowNotSupportedException()
    {
        // Arrange
        var json = JsonSerializer.Serialize(new
        {
            EventId = Guid.NewGuid(),
            EventType = "TestEvent"
        });

        // Act & Assert
        Assert.ThrowsException<NotSupportedException>(() =>
            _sut.Deserialize(json, "2.0")
        );
    }

    [TestMethod]
    public void Deserialize_WithNullVersion_ShouldThrowNotSupportedException()
    {
        // Arrange
        var json = JsonSerializer.Serialize(new
        {
            EventId = Guid.NewGuid(),
            EventType = "TestEvent"
        });

        // Act & Assert
        Assert.ThrowsException<NotSupportedException>(() =>
            _sut.Deserialize(json, null!)
        );
    }

    [TestMethod]
    public void Deserialize_WithInvalidJson_ShouldThrowInvalidOperationException()
    {
        // Arrange
        var invalidJson = "{ this-is-not-valid-json }";

        // Act & Assert
        Assert.ThrowsException<InvalidOperationException>(() =>
            _sut.Deserialize(invalidJson, "3.0")
        );
    }

    [TestMethod]
    public void Deserialize_WithEmptyBody_ShouldThrowInvalidOperationException()
    {
        // Arrange
        var emptyJson = string.Empty;

        // Act & Assert
        Assert.ThrowsException<InvalidOperationException>(() =>
            _sut.Deserialize(emptyJson, "3.0")
        );
    }
}
