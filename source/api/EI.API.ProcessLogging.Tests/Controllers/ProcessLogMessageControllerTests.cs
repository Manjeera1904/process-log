using AutoMapper;
using EI.API.ProcessLogging.Controllers;
using EI.API.ProcessLogging.Data;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.API.ProcessLogging.Model;
using EI.Data.TestHelpers.Controllers;
using EI.Data.TestHelpers.Controllers.Helper;
using Microsoft.AspNetCore.Mvc;
using Moq;

namespace EI.API.ProcessLogging.Tests.Controllers;

[TestClass]
public class ProcessLogMessageControllerTests
    : BaseControllerWithoutHistoryTests<IProcessLogMessageRepository, ProcessLogMessageController, ProcessLogMessage, ProcessLogMessageV1>
{
    /*
    protected override ProcessLogMessageController GetController(Mock<IProcessLogMessageRepository> mockRepository, Mock<IMapper> mockMapper)
    {
        var mockServices = base.SetupBaseControllerServices<IProcessLogMessageControllerServices>(mockRepository, mockMapper);

        var controller = new ProcessLogMessageController(mockServices.Object);
        return controller;
    }
    */

    #region Helper Methods

    private (ProcessLogMessageV2, ProcessLogMessage) BuildV2Models()
    {
        var id = Guid.NewGuid();
        var entity = new ProcessLogMessage
        {
            Id = id,
            ProcessLogId = Guid.NewGuid(),
            Level = ProcessLogConstants.MessageLevel.Fatal,
            Message = "Test message",
            MessageTimestamp = DateTime.UtcNow,
            FileProcessLogId = Guid.NewGuid()
        };

        var dto = new ProcessLogMessageV2
        {
            Id = id,
            ProcessLogId = entity.ProcessLogId,
            Level = entity.Level,
            Message = entity.Message,
            MessageTimestamp = entity.MessageTimestamp,
            FileProcessLogId = entity.FileProcessLogId
        };

        return (dto, entity);
    }

    #endregion

    protected override bool SupportsPut => false;

    //TODO : Remove these overrides once all the tests are verified
    //#region Ensure PUT always returns BAD REQUEST

    //protected override IList<(int, Type?)> PutResponseStatusCodes { get; } = [];

    //[TestMethod]
    //public override async Task Put_ReturnsOk_WhenDtoIsValid()
    //{
    //    // Arrange
    //    var (dto, _) = BuildModels();

    //    // Required properties for update
    //    dto.UpdatedBy = "unit-test@example.com";
    //    dto.RowVersion = [0x01, 0x02];

    //    var (mockRepository, mockMapper) = GetMocks();

    //    var controller = GetController(mockRepository, mockMapper);

    //    // Act
    //    var actionResult = await controller.Put(dto.Id!.Value, dto);

    //    // Assert
    //    var badRequestResult = actionResult as BadRequestObjectResult;
    //    Assert.IsNotNull(badRequestResult);
    //    Assert.AreEqual(400, badRequestResult.StatusCode);
    //}

    //// Disable test - no PUT allowed -- [TestMethod]
    //public override Task Put_ReturnsConflict_WhenUniqueKeyConflict()
    //{
    //    Assert.Fail("PUT not allowed for ProcessLogMessage");
    //    return Task.FromException(new InvalidOperationException("PUT not allowed for ProcessLogMessage"));
    //}

    //// Disable test - no PUT allowed -- [TestMethod]
    //public override Task Put_ReturnsBadRequest_WhenForeignKeyMissing()
    //{
    //    Assert.Fail("PUT not allowed for ProcessLogMessage");
    //    return Task.FromException(new InvalidOperationException("PUT not allowed for ProcessLogMessage"));
    //}

    //public override void Put_DefinesResponseType()
    //{
    //    Assert.Fail("PUT not allowed for ProcessLogMessage");
    //}

    //public override Task Put_ReturnsOk_AndAssignsUpdatedBy()
    //{
    //    Assert.Fail("PUT not allowed for ProcessLogMessage");
    //    return Task.FromException(new InvalidOperationException("PUT not allowed for ProcessLogMessage"));
    //}

    //public override Task Put_ReturnsUnauthorized_WhenAuthTokenMissing()
    //{
    //    Assert.Fail("PUT not allowed for ProcessLogMessage");
    //    return Task.FromException(new InvalidOperationException("PUT not allowed for ProcessLogMessage"));
    //}

    //public override Task Put_ReturnsUnauthorized_WhenAuthTokenMissingUserId()
    //{
    //    Assert.Fail("PUT not allowed for ProcessLogMessage");
    //    return Task.FromException(new InvalidOperationException("PUT not allowed for ProcessLogMessage"));
    //}

    //public override Task Put_ReturnsUnauthorized_WhenAuthTokenMissingUsername()
    //{
    //    Assert.Fail("PUT not allowed for ProcessLogMessage");
    //    return Task.FromException(new InvalidOperationException("PUT not allowed for ProcessLogMessage"));
    //}

    //#endregion Ensure PUT always returns BAD REQUEST

    #region V1

    [TestMethod]
    public async Task Get_ReturnsAllRecords()
    {
        // Arrange
        var (dto1, entity1) = BuildModels();
        var (dto2, entity2) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();

        mockRepository.Setup(repo => repo.GetAllAsync()).ReturnsAsync([entity1, entity2]);
        mockMapper.Setup(mapper => mapper.Map<ProcessLogMessageV1>(entity1)).Returns(dto1);
        mockMapper.Setup(mapper => mapper.Map<ProcessLogMessageV1>(entity2)).Returns(dto2);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.Get();

        // Assert
        var result = actionResult.GetOkList<ProcessLogMessageV1>();
        Assert.AreEqual(2, result.Count);
        Assert.AreEqual(dto1.Id, result[0].Id);
        Assert.AreEqual(dto2.Id, result[1].Id);
    }

    [TestMethod]
    public async Task Get_ReturnsNoContent_WhenNoRecordsExist()
    {
        // Arrange
        var (mockRepository, mockMapper) = GetMocks();

        mockRepository.Setup(repo => repo.GetAllAsync()).ReturnsAsync([]);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.Get();

        // Assert
        _ = actionResult.GetNoContent();
    }

    [TestMethod]
    public async Task GetById_ReturnsRecord_WhenFound()
    {
        // Arrange
        var (dto, entity) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();

        mockRepository.Setup(repo => repo.GetByIdAsync(It.IsAny<Guid>())).ReturnsAsync(entity);
        mockMapper.Setup(mapper => mapper.Map<ProcessLogMessageV1>(entity)).Returns(dto);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.Get(dto.Id!.Value);

        // Assert
        var okResult = actionResult as OkObjectResult;
        Assert.IsNotNull(okResult);
        var result = okResult.Value as ProcessLogMessageV1;
        Assert.IsNotNull(result);
        Assert.AreEqual(dto.Id, result.Id);
    }

    [TestMethod]
    public async Task GetById_ReturnsNotFound_WhenRecordDoesNotExist()
    {
        // Arrange
        var (mockRepository, mockMapper) = GetMocks();
        var id = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByIdAsync(It.IsAny<Guid>())).ReturnsAsync((ProcessLogMessage?) null);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.Get(id);

        // Assert
        _ = actionResult.GetNotFound();
    }

    [TestMethod]
    public async Task GetByProcessLog_ReturnsResults()
    {
        // Arrange
        var (dto1, entity1) = BuildModels();
        var (dto2, entity2) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();

        var searchId = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByProcessLogAsync(It.Is<Guid>(id => id == searchId))).ReturnsAsync([entity1, entity2]);

        mockMapper.Setup(mapper => mapper.Map<ProcessLogMessageV1>(entity1)).Returns(dto1);
        mockMapper.Setup(mapper => mapper.Map<ProcessLogMessageV1>(entity2)).Returns(dto2);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByProcessLog(searchId);

        // Assert
        var result = actionResult.GetOkList<ProcessLogMessageV1>();
        Assert.AreEqual(2, result.Count);
        Assert.AreEqual(dto1.Id, result[0].Id);
        Assert.AreEqual(dto2.Id, result[1].Id);
    }

    [TestMethod]
    public async Task GetByProcessLog_ReturnsNoContent_WhenNoneFound()
    {
        // Arrange
        var (mockRepository, mockMapper) = GetMocks();

        var searchId = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByProcessLogAsync(It.Is<Guid>(id => id == searchId))).ReturnsAsync([]);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByProcessLog(searchId);

        // Assert
        _ = actionResult.GetNoContent();
    }

    [TestMethod]
    public async Task GetByProcessLogAndLevel_ReturnsResults()
    {
        // Arrange
        var (dto1, entity1) = BuildModels();
        var (dto2, entity2) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();

        var searchId = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByProcessLogAsync(It.Is<Guid>(id => id == searchId), ProcessLogConstants.MessageLevel.Fatal)).ReturnsAsync([entity1, entity2]);

        mockMapper.Setup(mapper => mapper.Map<ProcessLogMessageV1>(entity1)).Returns(dto1);
        mockMapper.Setup(mapper => mapper.Map<ProcessLogMessageV1>(entity2)).Returns(dto2);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByProcessLog(searchId, ProcessLogConstants.MessageLevel.Fatal);

        // Assert
        var result = actionResult.GetOkList<ProcessLogMessageV1>();
        Assert.AreEqual(2, result.Count);
        Assert.AreEqual(dto1.Id, result[0].Id);
        Assert.AreEqual(dto2.Id, result[1].Id);
    }

    [TestMethod]
    public async Task GetByProcessLogLevel_ReturnsNoContent_WhenNoneFound()
    {
        // Arrange
        var (mockRepository, mockMapper) = GetMocks();

        var searchId = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByProcessLogAsync(It.Is<Guid>(id => id == searchId), ProcessLogConstants.MessageLevel.Fatal)).ReturnsAsync([]);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByProcessLog(searchId, ProcessLogConstants.MessageLevel.Fatal);

        // Assert
        _ = actionResult.GetNoContent();
    }

    [TestMethod]
    public async Task Post_CreatesNewRecord()
    {
        // Arrange
        var (dto, entity) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();

        mockMapper.Setup(mapper => mapper.Map<ProcessLogMessage>(dto)).Returns(entity);
        mockRepository.Setup(repo => repo.InsertAsync(It.IsAny<ProcessLogMessage>())).ReturnsAsync(entity);
        mockMapper.Setup(mapper => mapper.Map<ProcessLogMessageV1>(entity)).Returns(dto);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.Post(dto);

        // Assert
        var result = actionResult as CreatedAtActionResult;
        Assert.IsNotNull(result);
        Assert.AreEqual(201, result.StatusCode);
        var returnedDto = result.Value as ProcessLogMessageV1;
        Assert.IsNotNull(returnedDto);
        Assert.AreEqual(dto.Id, returnedDto.Id);
    }

    #endregion

    #region V2

    [TestMethod]
    public async Task GetV2_ReturnsAllRecordsWithNavigationProperties()
    {
        // Arrange
        var (dto1, entity1) = BuildV2Models();
        var (dto2, entity2) = BuildV2Models();

        var (mockRepository, mockMapper) = GetMocks();

        mockRepository.Setup(repo => repo.GetAllAsync()).ReturnsAsync([entity1, entity2]);
        mockMapper.Setup(mapper => mapper.Map<IEnumerable<ProcessLogMessageV2>>(It.IsAny<List<ProcessLogMessage>>()))
            .Returns(new List<ProcessLogMessageV2> { dto1, dto2 });

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetV2();

        // Assert
        var okResult = actionResult as OkObjectResult;
        Assert.IsNotNull(okResult);
        var result = okResult.Value as IEnumerable<ProcessLogMessageV2>;
        Assert.IsNotNull(result);
        var resultList = result.ToList();
        Assert.AreEqual(2, resultList.Count);
        Assert.AreEqual(dto1.FileProcessLogId, resultList[0].FileProcessLogId);
    }

    [TestMethod]
    public async Task GetV2_ReturnsNoContent_WhenNoRecordsExist()
    {
        // Arrange
        var (mockRepository, mockMapper) = GetMocks();

        mockRepository.Setup(repo => repo.GetAllAsync()).ReturnsAsync(new List<ProcessLogMessage>());

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetV2();

        // Assert
        var result = actionResult as NoContentResult;
        Assert.IsNotNull(result);
        Assert.AreEqual(204, result.StatusCode);
    }

    [TestMethod]
    public async Task GetV2_ById_ReturnsRecordWithNavigationProperties()
    {
        // Arrange
        var (dto, entity) = BuildV2Models();

        var (mockRepository, mockMapper) = GetMocks();

        mockRepository.Setup(repo => repo.GetByIdAsync(It.IsAny<Guid>())).ReturnsAsync(entity);
        mockMapper.Setup(mapper => mapper.Map<ProcessLogMessageV2>(entity)).Returns(dto);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetV2(dto.Id!.Value);

        // Assert
        var okResult = actionResult as OkObjectResult;
        Assert.IsNotNull(okResult);
        var result = okResult.Value as ProcessLogMessageV2;
        Assert.IsNotNull(result);
        Assert.AreEqual(dto.Id, result.Id);
        Assert.AreEqual(dto.FileProcessLogId, result.FileProcessLogId);
    }

    [TestMethod]
    public async Task GetV2_ById_ReturnsNotFound_WhenRecordDoesNotExist()
    {
        // Arrange
        var (mockRepository, mockMapper) = GetMocks();
        var id = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByIdAsync(It.IsAny<Guid>())).ReturnsAsync((ProcessLogMessage?) null);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetV2(id);

        // Assert
        var result = actionResult as NotFoundResult;
        Assert.IsNotNull(result);
        Assert.AreEqual(404, result.StatusCode);
    }

    [TestMethod]
    public async Task GetByProcessLogV2_ReturnsResultsWithNavigationProperties()
    {
        // Arrange
        var (dto1, entity1) = BuildV2Models();
        var (dto2, entity2) = BuildV2Models();

        var (mockRepository, mockMapper) = GetMocks();

        var searchId = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByProcessLogAsync(It.Is<Guid>(id => id == searchId)))
            .ReturnsAsync(new List<ProcessLogMessage> { entity1, entity2 });
        mockMapper.Setup(mapper => mapper.Map<IEnumerable<ProcessLogMessageV2>>(It.IsAny<List<ProcessLogMessage>>()))
            .Returns(new List<ProcessLogMessageV2> { dto1, dto2 });

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByProcessLogV2(searchId);

        // Assert
        var okResult = actionResult as OkObjectResult;
        Assert.IsNotNull(okResult);
        var result = okResult.Value as IEnumerable<ProcessLogMessageV2>;
        Assert.IsNotNull(result);
        var resultList = result.ToList();
        Assert.AreEqual(2, resultList.Count);
        Assert.AreEqual(dto1.Id, resultList[0].Id);
        Assert.AreEqual(dto1.FileProcessLogId, resultList[0].FileProcessLogId);
    }

    [TestMethod]
    public async Task GetByProcessLogV2_ReturnsNoContent_WhenNoneFound()
    {
        // Arrange
        var (mockRepository, mockMapper) = GetMocks();

        var searchId = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByProcessLogAsync(It.Is<Guid>(id => id == searchId)))
            .ReturnsAsync(new List<ProcessLogMessage>());

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByProcessLogV2(searchId);

        // Assert
        var result = actionResult as NoContentResult;
        Assert.IsNotNull(result);
        Assert.AreEqual(204, result.StatusCode);
    }

    [TestMethod]
    public async Task GetByProcessLogAndLevelV2_ReturnsResultsWithNavigationProperties()
    {
        // Arrange
        var (dto1, entity1) = BuildV2Models();
        var (dto2, entity2) = BuildV2Models();

        var (mockRepository, mockMapper) = GetMocks();

        var searchId = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByProcessLogAsync(It.Is<Guid>(id => id == searchId), ProcessLogConstants.MessageLevel.Fatal))
            .ReturnsAsync(new List<ProcessLogMessage> { entity1, entity2 });
        mockMapper.Setup(mapper => mapper.Map<IEnumerable<ProcessLogMessageV2>>(It.IsAny<List<ProcessLogMessage>>()))
            .Returns(new List<ProcessLogMessageV2> { dto1, dto2 });

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByProcessLogV2(searchId, ProcessLogConstants.MessageLevel.Fatal);

        // Assert
        var okResult = actionResult as OkObjectResult;
        Assert.IsNotNull(okResult);
        var result = okResult.Value as IEnumerable<ProcessLogMessageV2>;
        Assert.IsNotNull(result);
        var resultList = result.ToList();
        Assert.AreEqual(2, resultList.Count);
        Assert.AreEqual(dto1.FileProcessLogId, resultList[0].FileProcessLogId);
    }

    [TestMethod]
    public async Task GetByProcessLogAndLevelV2_ReturnsNoContent_WhenNoneFound()
    {
        // Arrange
        var (mockRepository, mockMapper) = GetMocks();

        var searchId = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByProcessLogAsync(It.Is<Guid>(id => id == searchId), ProcessLogConstants.MessageLevel.Fatal))
            .ReturnsAsync(new List<ProcessLogMessage>());

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByProcessLogV2(searchId, ProcessLogConstants.MessageLevel.Fatal);

        // Assert
        var result = actionResult as NoContentResult;
        Assert.IsNotNull(result);
        Assert.AreEqual(204, result.StatusCode);
    }

    [TestMethod]
    public async Task PostV2_CreatesNewRecordWithNavigationProperties()
    {
        // Arrange
        var (dto, entity) = BuildV2Models();

        var (mockRepository, mockMapper) = GetMocks();

        mockMapper.Setup(mapper => mapper.Map<ProcessLogMessage>(dto)).Returns(entity);
        mockRepository.Setup(repo => repo.InsertAsync(It.IsAny<ProcessLogMessage>())).ReturnsAsync(entity);
        mockRepository.Setup(repo => repo.GetByIdAsync(It.IsAny<Guid>())).ReturnsAsync(entity);
        mockMapper.Setup(mapper => mapper.Map<ProcessLogMessageV2>(entity)).Returns(dto);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.PostV2(dto);

        // Assert
        var result = actionResult as CreatedAtActionResult;
        Assert.IsNotNull(result);
        Assert.AreEqual(201, result.StatusCode);
        Assert.AreEqual(nameof(controller.GetV2), result.ActionName);
        var returnedDto = result.Value as ProcessLogMessageV2;
        Assert.IsNotNull(returnedDto);
        Assert.AreEqual(dto.Id, returnedDto.Id);
        Assert.AreEqual(dto.FileProcessLogId, returnedDto.FileProcessLogId);
    }

    [TestMethod]
    public async Task PostV2_ReturnsInternalServerError_WhenEntityNotFoundAfterInsert()
    {
        // Arrange
        var (dto, entity) = BuildV2Models();

        var (mockRepository, mockMapper) = GetMocks();

        mockMapper.Setup(mapper => mapper.Map<ProcessLogMessage>(dto)).Returns(entity);
        mockRepository.Setup(repo => repo.InsertAsync(It.IsAny<ProcessLogMessage>())).ReturnsAsync(entity);
        mockRepository.Setup(repo => repo.GetByIdAsync(It.IsAny<Guid>())).ReturnsAsync((ProcessLogMessage?) null);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.PostV2(dto);

        // Assert
        var result = actionResult as ObjectResult;
        Assert.IsNotNull(result);
        Assert.AreEqual(500, result.StatusCode);
        Assert.AreEqual("Failed to retrieve saved entity", result.Value);
    }

    #endregion
}