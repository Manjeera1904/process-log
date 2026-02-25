using AutoMapper;
using EI.API.ProcessLogging.Controllers;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.API.ProcessLogging.Model;
using EI.API.Service.Data.Helpers.Repository;
using EI.Data.TestHelpers.Controllers;
using EI.Data.TestHelpers.Controllers.Helper;
using Microsoft.AspNetCore.Mvc;
using Moq;

namespace EI.API.ProcessLogging.Tests.Controllers;

[TestClass]
public class FileProcessLogControllerTests
    : BaseControllerWithoutHistoryTests<IFileProcessLogRepository, FileProcessLogController, FileProcessLog, FileProcessLogV1>
{
    /*
    protected override FileProcessLogController GetController(Mock<IFileProcessLogRepository> mockRepository, Mock<IMapper> mockMapper)
    {
        var mockServices = base.SetupBaseControllerServices<IFileProcessLogControllerServices>(mockRepository, mockMapper);

        var controller = new FileProcessLogController(mockServices.Object);
        return controller;
    }
    */
    #region Helper Methods

    private (FileProcessLogV2, FileProcessLog) BuildV2Models()
    {
        var id = Guid.NewGuid();
        var entity = new FileProcessLog
        {
            Id = id,
            ProcessLogId = Guid.NewGuid(),
            FileName = "test-file.txt",
            FilePath = "https://storage.example.com/test-file.txt",
            FileSize = 1024,
            FileHash = "hash123",
            PurposeName = "Originating Contract",
            ProcessStatus = "New"
        };

        var dto = new FileProcessLogV2
        {
            Id = id,
            ProcessLogId = entity.ProcessLogId,
            FileName = entity.FileName,
            FilePath = entity.FilePath,
            FileSize = entity.FileSize,
            FileHash = entity.FileHash,
            PurposeName = entity.PurposeName,
            ProcessStatus = entity.ProcessStatus
        };

        return (dto, entity);
    }

    #endregion

    #region V1

    [TestMethod]
    public async Task Get_ReturnsAllRecords()
    {
        // Arrange
        var (dto1, entity1) = BuildModels();
        var (dto2, entity2) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();

        mockRepository.Setup(repo => repo.GetAllAsync()).ReturnsAsync([entity1, entity2]);
        mockMapper.Setup(mapper => mapper.Map<FileProcessLogV1>(entity1)).Returns(dto1);
        mockMapper.Setup(mapper => mapper.Map<FileProcessLogV1>(entity2)).Returns(dto2);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.Get();

        // Assert
        var result = actionResult.GetOkList<FileProcessLogV1>();
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
        mockMapper.Setup(mapper => mapper.Map<FileProcessLogV1>(entity)).Returns(dto);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.Get(dto.Id!.Value);

        // Assert
        var okResult = actionResult as OkObjectResult;
        Assert.IsNotNull(okResult);
        var result = okResult.Value as FileProcessLogV1;
        Assert.IsNotNull(result);
        Assert.AreEqual(dto.Id, result.Id);
    }

    [TestMethod]
    public async Task GetById_ReturnsNotFound_WhenRecordDoesNotExist()
    {
        // Arrange
        var (mockRepository, mockMapper) = GetMocks();
        var id = Guid.NewGuid();

        mockRepository
            .As<IReadRepository<FileProcessLog>>()
            .Setup(repo => repo.GetAsync(It.IsAny<Guid>()))
            .ReturnsAsync((FileProcessLog?) null);

        // IMPORTANT: base controller still calls mapper with null
        mockMapper
            .Setup(m => m.Map<FileProcessLogV1>((FileProcessLog?) null))
            .Returns((FileProcessLogV1?) null);

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

        mockMapper.Setup(mapper => mapper.Map<FileProcessLogV1>(entity1)).Returns(dto1);
        mockMapper.Setup(mapper => mapper.Map<FileProcessLogV1>(entity2)).Returns(dto2);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByProcessLog(searchId);

        // Assert
        var result = actionResult.GetOkList<FileProcessLogV1>();
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
    public async Task Post_CreatesNewRecord()
    {
        // Arrange
        var (dto, entity) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();

        mockMapper.Setup(mapper => mapper.Map<FileProcessLog>(dto)).Returns(entity);
        mockRepository.Setup(repo => repo.InsertAsync(It.IsAny<FileProcessLog>())).ReturnsAsync(entity);
        mockMapper.Setup(mapper => mapper.Map<FileProcessLogV1>(entity)).Returns(dto);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.Post(dto);

        // Assert
        var result = actionResult as CreatedAtActionResult;
        Assert.IsNotNull(result);
        Assert.AreEqual(201, result.StatusCode);
        var returnedDto = result.Value as FileProcessLogV1;
        Assert.IsNotNull(returnedDto);
        Assert.AreEqual(dto.Id, returnedDto.Id);
    }

    [TestMethod]
    public async Task Put_UpdatesExistingRecord()
    {
        // Arrange
        var (dto, entity) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();

        mockMapper.Setup(mapper => mapper.Map<FileProcessLog>(dto)).Returns(entity);
        mockRepository.Setup(repo => repo.UpdateAsync(It.IsAny<FileProcessLog>())).ReturnsAsync(entity);
        mockMapper.Setup(mapper => mapper.Map<FileProcessLogV1>(entity)).Returns(dto);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.Put(dto.Id!.Value, dto);

        // Assert
        var okResult = actionResult as OkObjectResult;
        Assert.IsNotNull(okResult);
        var result = okResult.Value as FileProcessLogV1;
        Assert.IsNotNull(result);
        Assert.AreEqual(dto.Id, result.Id);
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
        mockMapper.Setup(mapper => mapper.Map<IEnumerable<FileProcessLogV2>>(It.IsAny<List<FileProcessLog>>()))
            .Returns(new List<FileProcessLogV2> { dto1, dto2 });

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetV2();

        // Assert
        var okResult = actionResult as OkObjectResult;
        Assert.IsNotNull(okResult);
        var result = okResult.Value as IEnumerable<FileProcessLogV2>;
        Assert.IsNotNull(result);
        var resultList = result.ToList();
        Assert.AreEqual(2, resultList.Count);
        Assert.AreEqual(dto1.PurposeName, resultList[0].PurposeName);
        Assert.AreEqual(dto1.ProcessStatus, resultList[0].ProcessStatus);
    }

    [TestMethod]
    public async Task GetV2_ReturnsNoContent_WhenNoRecordsExist()
    {
        // Arrange
        var (mockRepository, mockMapper) = GetMocks();

        mockRepository.Setup(repo => repo.GetAllAsync()).ReturnsAsync(new List<FileProcessLog>());

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetV2();

        // Assert
        var result = actionResult as NoContentResult;
        Assert.IsNotNull(result);
        Assert.AreEqual(204, result.StatusCode);
    }

    [TestMethod]
    public async Task GetV2_ReturnsNoContent_WhenRepositoryReturnsNull()
    {
        // Arrange
        var (mockRepository, mockMapper) = GetMocks();

        mockRepository.Setup(repo => repo.GetAllAsync()).ReturnsAsync((List<FileProcessLog>?) null);

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
        mockMapper.Setup(mapper => mapper.Map<FileProcessLogV2>(entity)).Returns(dto);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetV2(dto.Id!.Value);

        // Assert
        var okResult = actionResult as OkObjectResult;
        Assert.IsNotNull(okResult);
        var result = okResult.Value as FileProcessLogV2;
        Assert.IsNotNull(result);
        Assert.AreEqual(dto.Id, result.Id);
        Assert.AreEqual(dto.PurposeName, result.PurposeName);
        Assert.AreEqual(dto.ProcessStatus, result.ProcessStatus);
    }

    [TestMethod]
    public async Task GetV2_ById_ReturnsNotFound_WhenRecordDoesNotExist()
    {
        // Arrange
        var (mockRepository, mockMapper) = GetMocks();
        var id = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByIdAsync(It.IsAny<Guid>())).ReturnsAsync((FileProcessLog?) null);

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
            .ReturnsAsync(new List<FileProcessLog> { entity1, entity2 });
        mockMapper.Setup(mapper => mapper.Map<IEnumerable<FileProcessLogV2>>(It.IsAny<List<FileProcessLog>>()))
            .Returns(new List<FileProcessLogV2> { dto1, dto2 });

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByProcessLogV2(searchId);

        // Assert
        var okResult = actionResult as OkObjectResult;
        Assert.IsNotNull(okResult);
        var result = okResult.Value as IEnumerable<FileProcessLogV2>;
        Assert.IsNotNull(result);
        var resultList = result.ToList();
        Assert.AreEqual(2, resultList.Count);
        Assert.AreEqual(dto1.Id, resultList[0].Id);
        Assert.AreEqual(dto1.PurposeName, resultList[0].PurposeName);
        Assert.AreEqual(dto2.Id, resultList[1].Id);
        Assert.AreEqual(dto2.ProcessStatus, resultList[1].ProcessStatus);
    }

    [TestMethod]
    public async Task GetByProcessLogV2_ReturnsNoContent_WhenNoneFound()
    {
        // Arrange
        var (mockRepository, mockMapper) = GetMocks();

        var searchId = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByProcessLogAsync(It.Is<Guid>(id => id == searchId)))
            .ReturnsAsync(new List<FileProcessLog>());

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByProcessLogV2(searchId);

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

        mockMapper.Setup(mapper => mapper.Map<FileProcessLog>(dto)).Returns(entity);
        mockRepository.Setup(repo => repo.InsertAsync(It.IsAny<FileProcessLog>())).ReturnsAsync(entity);
        mockRepository.Setup(repo => repo.GetByIdAsync(It.IsAny<Guid>())).ReturnsAsync(entity);
        mockMapper.Setup(mapper => mapper.Map<FileProcessLogV2>(entity)).Returns(dto);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.PostV2(dto);

        // Assert
        var result = actionResult as CreatedAtActionResult;
        Assert.IsNotNull(result);
        Assert.AreEqual(201, result.StatusCode);
        Assert.AreEqual(nameof(controller.GetV2), result.ActionName);
        var returnedDto = result.Value as FileProcessLogV2;
        Assert.IsNotNull(returnedDto);
        Assert.AreEqual(dto.Id, returnedDto.Id);
        Assert.AreEqual(dto.PurposeName, returnedDto.PurposeName);
        Assert.AreEqual(dto.ProcessStatus, returnedDto.ProcessStatus);
    }

    [TestMethod]
    public async Task PostV2_ReturnsInternalServerError_WhenEntityNotFoundAfterInsert()
    {
        // Arrange
        var (dto, entity) = BuildV2Models();

        var (mockRepository, mockMapper) = GetMocks();

        mockMapper.Setup(mapper => mapper.Map<FileProcessLog>(dto)).Returns(entity);
        mockRepository.Setup(repo => repo.InsertAsync(It.IsAny<FileProcessLog>())).ReturnsAsync(entity);
        mockRepository.Setup(repo => repo.GetByIdAsync(It.IsAny<Guid>())).ReturnsAsync((FileProcessLog?) null);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.PostV2(dto);

        // Assert
        var result = actionResult as ObjectResult;
        Assert.IsNotNull(result);
        Assert.AreEqual(500, result.StatusCode);
        Assert.AreEqual("Failed to retrieve saved entity", result.Value);
    }

    [TestMethod]
    public async Task PutV2_UpdatesExistingRecordWithNavigationProperties()
    {
        // Arrange
        var (dto, entity) = BuildV2Models();

        var (mockRepository, mockMapper) = GetMocks();

        mockMapper.Setup(mapper => mapper.Map<FileProcessLog>(dto)).Returns(entity);
        mockRepository.Setup(repo => repo.UpdateAsync(It.IsAny<FileProcessLog>())).ReturnsAsync(entity);
        mockRepository.Setup(repo => repo.GetByIdAsync(It.IsAny<Guid>())).ReturnsAsync(entity);
        mockMapper.Setup(mapper => mapper.Map<FileProcessLogV2>(entity)).Returns(dto);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.PutV2(dto.Id!.Value, dto);

        // Assert
        var okResult = actionResult as OkObjectResult;
        Assert.IsNotNull(okResult);
        var result = okResult.Value as FileProcessLogV2;
        Assert.IsNotNull(result);
        Assert.AreEqual(dto.Id, result.Id);
        Assert.AreEqual(dto.PurposeName, result.PurposeName);
        Assert.AreEqual(dto.ProcessStatus, result.ProcessStatus);
    }

    [TestMethod]
    public async Task PutV2_ReturnsBadRequest_WhenIdMismatch()
    {
        // Arrange
        var (dto, entity) = BuildV2Models();
        var differentId = Guid.NewGuid();

        var (mockRepository, mockMapper) = GetMocks();

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.PutV2(differentId, dto);

        // Assert
        var result = actionResult as BadRequestObjectResult;
        Assert.IsNotNull(result);
        Assert.AreEqual(400, result.StatusCode);
        Assert.AreEqual("ID mismatch", result.Value);
    }

    [TestMethod]
    public async Task PutV2_ReturnsNotFound_WhenRecordDoesNotExistAfterUpdate()
    {
        // Arrange
        var (dto, entity) = BuildV2Models();

        var (mockRepository, mockMapper) = GetMocks();

        mockMapper.Setup(mapper => mapper.Map<FileProcessLog>(dto)).Returns(entity);
        mockRepository.Setup(repo => repo.UpdateAsync(It.IsAny<FileProcessLog>())).ReturnsAsync(entity);
        mockRepository.Setup(repo => repo.GetByIdAsync(It.IsAny<Guid>())).ReturnsAsync((FileProcessLog?) null);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.PutV2(dto.Id!.Value, dto);

        // Assert
        var result = actionResult as NotFoundResult;
        Assert.IsNotNull(result);
        Assert.AreEqual(404, result.StatusCode);
    }

    #endregion
}