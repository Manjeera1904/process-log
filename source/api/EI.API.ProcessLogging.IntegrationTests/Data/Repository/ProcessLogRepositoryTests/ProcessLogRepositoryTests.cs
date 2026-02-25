using EI.API.ProcessLogging.Data;
using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Models;
using EI.API.ProcessLogging.Data.Repositories;
using EI.API.ProcessLogging.IntegrationTests.Data.Repository.ActivityTypeRepositoryTests;
using EI.Data.TestHelpers.Repository;
using Moq;

namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository.ProcessLogRepositoryTests;

[TestClass]
public class ProcessLogRepositoryTests : BaseRepositoryTests<ProcessLogDbContext, ProcessLogRepository, ProcessLog>
{
    protected override string ConnectionStringName => ProcessLogDbContext.ConnectionStringName;

    protected ProcessLogTestConfig _testConfig = default!;

    protected override void AdditionalTestSetup(ProcessLogDbContext context)
    {
        base.AdditionalTestSetup(context);

        _testConfig = ProcessLogTestHelpers.BuildTestConfig(context);
    }

    protected override ProcessLog BuildModel(string label) =>
        ProcessLogTestHelpers.BuildProcessLog(ProcessLogConstants.ActivityType.ReceiveFile, ProcessLogConstants.ProcessStatus.Duplicate, label);

    protected override ProcessLogTestHelpers.MockProcessLogRepository BuildRepo(ProcessLogDbContext context)
        => ProcessLogTestHelpers.BuildRepo(context);

    [TestMethod]
    public async Task UpdateStatus_LogsProcessLogMessage()
    {
        // Arrange
        var entity = BuildModel("1");
        entity.Status = ProcessLogConstants.ProcessStatus.InProgress;
        await DbSet.AddAsync(entity);
        await _context.SaveChangesAsync();

        var originalRowVersion = entity.RowVersion;

        // Act
        var updatedBy = Guid.NewGuid().ToString("N");
        ProcessLog result;
        Mock<IProcessLogMessageRepository> _mockMessageRepo;
        await using var updateContext = MakeContext();
        await using var updateRepo = BuildRepo(updateContext);
        {
            entity.UpdatedBy = updatedBy;
            entity.Status = ProcessLogConstants.ProcessStatus.Duplicate;
            result = await updateRepo.UpdateAsync(entity);
            _mockMessageRepo = updateRepo.MockMessageRepo;
        }

        // Assert
        Assert.IsNotNull(result);
        Assert.AreEqual(updatedBy, result.UpdatedBy);
        Assert.AreNotEqual(originalRowVersion, result.RowVersion);

        _mockMessageRepo.Verify(m => m.InsertAsync(It.IsAny<ProcessLogMessage>()), Times.Once);
        var invocation = _mockMessageRepo.Invocations.Single();
        var loggedMessage = invocation.Arguments.Single() as ProcessLogMessage;
        Assert.IsNotNull(loggedMessage);
        Assert.AreEqual(entity.Id, loggedMessage.ProcessLogId);
        Assert.AreEqual(ProcessLogConstants.MessageLevel.Status, loggedMessage.Level);
        Assert.AreEqual(updatedBy, loggedMessage.UpdatedBy);
        Assert.IsTrue(loggedMessage.Message.Contains(ProcessLogConstants.ProcessStatus.InProgress));
        Assert.IsTrue(loggedMessage.Message.Contains(ProcessLogConstants.ProcessStatus.Duplicate));
        Assert.IsTrue(loggedMessage.MessageTimestamp >= DateTime.UtcNow.AddSeconds(-1));
    }

    [TestMethod]
    public async Task UpdateWithoutStatusChange_DoesNotLogProcessLogMessage()
    {
        // Arrange
        var entity = BuildModel("1");
        entity.Status = ProcessLogConstants.ProcessStatus.InProgress;
        await DbSet.AddAsync(entity);
        await _context.SaveChangesAsync();

        var originalRowVersion = entity.RowVersion;

        var updatedBy = nameof(UpdateStatus_LogsProcessLogMessage);
        entity.UpdatedBy = updatedBy;

        // Act
        await _repository.UpdateAsync(entity);
        var result = await DbSet.FindAsync(entity.Id);

        // Assert
        Assert.IsNotNull(result);
        Assert.AreEqual(updatedBy, result.UpdatedBy);
        Assert.AreNotEqual(originalRowVersion, result.RowVersion);

        var mockMessageRepo = (_repository as ProcessLogTestHelpers.MockProcessLogRepository)!.MockMessageRepo;
        mockMessageRepo.Verify(
                                x => x.InsertAsync(It.IsAny<ProcessLogMessage>()),
                                Times.Never
                               );
    }
    [TestMethod]
    public async Task SearchAsync_ReturnsResults()
    {
        // Arrange
        var request = new ProcessLogSearch
        {
            ActivityType = "DOES NOT EXIST",
            DateRange = "Last30Days",
            TimeZone = "UTC",
            PageNumber = 1,
            PageSize = 10
        };

        // Act
        var result = await _repository.SearchAsync(request);

        // Assert
        Assert.IsNotNull(result);
        Assert.AreEqual(0, result.Items.Count);
        Assert.AreEqual(0, result.TotalCount);
    }

    [TestMethod]
    public async Task SearchAsync_ReturnsEmpty_WhenNoneFound()
    {
        // Arrange
        var activityType = ActivityTypeTestHelpers.BuildActivityType("PLT");
        await _context.AddAsync(activityType);

        // Use current UTC time minus 31 days to ensure they're outside "Last30Days"
        var rangeStart = DateTime.UtcNow.AddDays(-31);
        var entity1 = BuildModel("1");
        entity1.Type = activityType.Type;
        entity1.StartTimestamp = rangeStart;
        entity1.LastUpdatedTimestamp = rangeStart;

        var entity2 = BuildModel("2");
        entity2.Type = activityType.Type;
        entity2.StartTimestamp = rangeStart.AddSeconds(15);
        entity2.LastUpdatedTimestamp = rangeStart.AddSeconds(15);

        await DbSet.AddRangeAsync(entity1, entity2);
        await _context.SaveChangesAsync();

        var request = new ProcessLogSearch
        {
            ActivityType = activityType.Type,
            DateRange = "Last30Days",  // This looks for records from today-30 to today
            TimeZone = "UTC",
            PageNumber = 1,
            PageSize = 10
        };

        // Act
        var result = await _repository.SearchAsync(request);

        // Assert
        Assert.IsNotNull(result);
        Assert.AreEqual(0, result.Items.Count);  // This should now pass
        Assert.AreEqual(0, result.TotalCount);
    }
    [TestMethod]
    public async Task SearchAsync_ReturnsMatchingResults()
    {
        // Arrange
        var activityType = ActivityTypeTestHelpers.BuildActivityType("PLT");
        await _context.AddAsync(activityType);

        var rangeStart = DateTime.UtcNow.AddDays(-5); // within Last7Days
        var entity = BuildModel("1");
        entity.Type = activityType.Type;
        entity.StartTimestamp = rangeStart;
        entity.LastUpdatedTimestamp = rangeStart;

        await DbSet.AddAsync(entity);
        await _context.SaveChangesAsync();

        var request = new ProcessLogSearch
        {
            ActivityType = activityType.Type,
            DateRange = "Last7Days",
            TimeZone = "UTC",
            PageNumber = 1,
            PageSize = 10
        };

        // Act
        var result = await _repository.SearchAsync(request);

        // Assert
        Assert.IsNotNull(result);
        Assert.AreEqual(1, result.Items.Count);
        Assert.AreEqual(entity.Type, result.Items[0].Type);
    }
    [TestMethod]
    public async Task SearchAsync_ReturnsResultsWithStatusFilter()
    {
        // Arrange
        var entity = BuildModel("1");
        entity.Status = "Completed";
        entity.StartTimestamp = DateTime.UtcNow.AddDays(-1);
        entity.LastUpdatedTimestamp = entity.StartTimestamp;

        await DbSet.AddAsync(entity);
        await _context.SaveChangesAsync();

        var request = new ProcessLogSearch
        {
            Statuses = new List<string> { "Completed" },
            DateRange = "Last7Days",
            TimeZone = "UTC",
            PageNumber = 1,
            PageSize = 10
        };

        // Act
        var result = await _repository.SearchAsync(request);

        // Assert
        Assert.IsNotNull(result);
        Assert.AreEqual(1, result.Items.Count);
        Assert.AreEqual("Completed", result.Items[0].Status);
    }
}
