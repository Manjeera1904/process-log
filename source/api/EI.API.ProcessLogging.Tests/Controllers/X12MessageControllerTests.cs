using AutoMapper;
using EI.API.ProcessLogging.Controllers;
using EI.API.ProcessLogging.Data;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.API.ProcessLogging.Model;
using EI.Data.TestHelpers.Controllers;
using EI.Data.TestHelpers.Controllers.Helper;
using Moq;

namespace EI.API.ProcessLogging.Tests.Controllers;

[TestClass]
public class X12MessageControllerTests
    : BaseControllerWithoutHistoryTests<IX12MessageRepository, X12MessageController, X12Message, X12MessageV1>
{
    /*
    protected override X12MessageController GetController(Mock<IX12MessageRepository> mockRepository, Mock<IMapper> mockMapper)
    {
        var mockServices = new Mock<IX12MessageControllerServices>(MockBehavior.Strict);
        mockServices.Setup(s => s.Repository).Returns(mockRepository.Object);
        mockServices.Setup(s => s.Mapper).Returns(mockMapper.Object);

        var controller = new X12MessageController(mockServices.Object);
        return controller;
    }
    */

    #region Ensure PUT always returns BAD REQUEST

    protected override IList<(int, Type?)> PutResponseStatusCodes { get; } = [];

    [TestMethod]
    public override async Task Put_ReturnsOk_WhenDtoIsValid()
    {
        // Arrange
        var (dto, _) = BuildModels();

        // Required properties for update
        dto.UpdatedBy = "unit-test@example.com";
        dto.RowVersion = [0x01, 0x02];

        var (mockRepository, mockMapper) = GetMocks();

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.Put(dto.Id!.Value, dto);

        // Assert
        // Special entity: Messages can not be updated, only inserted
        _ = actionResult.GetBadRequestResultWithMessage();
    }

    // Disable test - no PUT allowed -- [TestMethod]
    public override Task Put_ReturnsNotFound_WhenNotFoundInRepo()
    {
        Assert.Fail("PUT not allowed for X12Message");
        return Task.FromException(new InvalidOperationException("PUT not allowed for X12Message"));
    }

    // Disable test - no PUT allowed -- [TestMethod]
    public override Task Put_ReturnsNotFound_WhenNotFoundInRepoAlt()
    {
        Assert.Fail("PUT not allowed for X12Message");
        return Task.FromException(new InvalidOperationException("PUT not allowed for X12Message"));
    }

    // Disable test - no PUT allowed -- [TestMethod]
    public override Task Put_ReturnsBadRequest_WhenUriIdMissing()
    {
        Assert.Fail("PUT not allowed for X12Message");
        return Task.FromException(new InvalidOperationException("PUT not allowed for X12Message"));
    }

    // Disable test - no PUT allowed -- [TestMethod]
    public override Task Put_ReturnsBadRequest_WhenDtoIdMissing()
    {
        Assert.Fail("PUT not allowed for X12Message");
        return Task.FromException(new InvalidOperationException("PUT not allowed for X12Message"));
    }

    // Disable test - no PUT allowed -- [TestMethod]
    public override Task Put_ReturnsBadRequest_WhenUriIdAndDtoIdMismatch()
    {
        Assert.Fail("PUT not allowed for X12Message");
        return Task.FromException(new InvalidOperationException("PUT not allowed for X12Message"));
    }

    // Disable test - no PUT allowed -- [TestMethod]
    public override Task Put_ReturnsBadRequest_WhenRowVersionIsMissing()
    {
        Assert.Fail("PUT not allowed for X12Message");
        return Task.FromException(new InvalidOperationException("PUT not allowed for X12Message"));
    }

    // Disable test - no PUT allowed -- [TestMethod]
    public override Task Put_ReturnsBadRequest_WhenRowVersionIsEmpty()
    {
        Assert.Fail("PUT not allowed for X12Message");
        return Task.FromException(new InvalidOperationException("PUT not allowed for X12Message"));
    }

    // Disable test - no PUT allowed -- [TestMethod]
    public override Task Put_ReturnsConflict_WhenUniqueKeyConflict()
    {
        Assert.Fail("PUT not allowed for X12Message");
        return Task.FromException(new InvalidOperationException("PUT not allowed for X12Message"));
    }

    // Disable test - no PUT allowed -- [TestMethod]
    public override Task Put_ReturnsBadRequest_WhenForeignKeyMissing()
    {
        Assert.Fail("PUT not allowed for X12Message");
        return Task.FromException(new InvalidOperationException("PUT not allowed for X12Message"));
    }

    public override void Put_DefinesResponseType()
    {
        Assert.Fail("PUT not allowed for ProcessLogMessage");
    }

    public override Task Put_ReturnsOk_AndAssignsUpdatedBy()
    {
        Assert.Fail("PUT not allowed for ProcessLogMessage");
        return Task.FromException(new InvalidOperationException("PUT not allowed for ProcessLogMessage"));
    }

    public override Task Put_ReturnsUnauthorized_WhenAuthTokenMissing()
    {
        Assert.Fail("PUT not allowed for ProcessLogMessage");
        return Task.FromException(new InvalidOperationException("PUT not allowed for ProcessLogMessage"));
    }

    public override Task Put_ReturnsUnauthorized_WhenAuthTokenMissingUserId()
    {
        Assert.Fail("PUT not allowed for ProcessLogMessage");
        return Task.FromException(new InvalidOperationException("PUT not allowed for ProcessLogMessage"));
    }

    public override Task Put_ReturnsUnauthorized_WhenAuthTokenMissingUsername()
    {
        Assert.Fail("PUT not allowed for ProcessLogMessage");
        return Task.FromException(new InvalidOperationException("PUT not allowed for ProcessLogMessage"));
    }

    #endregion Ensure PUT always returns BAD REQUEST

    #region Get By X12Interchange
    [TestMethod]
    public async Task GetByX12Interchange_ReturnsResults()
    {
        // Arrange
        var (dto1, entity1) = BuildModels();
        var (dto2, entity2) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();

        var searchId = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByInterchangeAsync(searchId)).ReturnsAsync([entity1, entity2]);

        mockMapper.Setup(mapper => mapper.Map<X12MessageV1>(entity1)).Returns(dto1);
        mockMapper.Setup(mapper => mapper.Map<X12MessageV1>(entity2)).Returns(dto2);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByX12Interchange(searchId);

        // Assert
        var result = actionResult.GetOkList<X12MessageV1>();
        Assert.AreEqual(2, result.Count);
        Assert.AreEqual(dto1.Id, result[0].Id);
        Assert.AreEqual(dto2.Id, result[1].Id);
    }

    [TestMethod]
    public async Task GetByX12Interchange_ReturnsNoContent_WhenNoneFound()
    {
        // Arrange
        var (mockRepository, mockMapper) = GetMocks();

        var searchId = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByInterchangeAsync(searchId)).ReturnsAsync([]);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByX12Interchange(searchId);

        // Assert
        _ = actionResult.GetNoContent();
    }

    [TestMethod]
    public async Task GetByX12InterchangeAndLevel_ReturnsResults()
    {
        // Arrange
        var (dto1, entity1) = BuildModels();
        var (dto2, entity2) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();

        var searchId = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByInterchangeAsync(searchId, ProcessLogConstants.MessageLevel.Fatal)).ReturnsAsync([entity1, entity2]);

        mockMapper.Setup(mapper => mapper.Map<X12MessageV1>(entity1)).Returns(dto1);
        mockMapper.Setup(mapper => mapper.Map<X12MessageV1>(entity2)).Returns(dto2);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByX12Interchange(searchId, ProcessLogConstants.MessageLevel.Fatal);

        // Assert
        var result = actionResult.GetOkList<X12MessageV1>();
        Assert.AreEqual(2, result.Count);
        Assert.AreEqual(dto1.Id, result[0].Id);
        Assert.AreEqual(dto2.Id, result[1].Id);
    }

    [TestMethod]
    public async Task GetByX12InterchangeLevel_ReturnsNoContent_WhenNoneFound()
    {
        // Arrange
        var (mockRepository, mockMapper) = GetMocks();

        var searchId = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByInterchangeAsync(searchId, ProcessLogConstants.MessageLevel.Fatal)).ReturnsAsync([]);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByX12Interchange(searchId, ProcessLogConstants.MessageLevel.Fatal);

        // Assert
        _ = actionResult.GetNoContent();
    }
    #endregion Get By X12Interchange

    #region Get By X12FunctionalGroup
    [TestMethod]
    public async Task GetByX12FunctionalGroup_ReturnsResults()
    {
        // Arrange
        var (dto1, entity1) = BuildModels();
        var (dto2, entity2) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();

        var searchId = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByFunctionalGroupAsync(searchId)).ReturnsAsync([entity1, entity2]);

        mockMapper.Setup(mapper => mapper.Map<X12MessageV1>(entity1)).Returns(dto1);
        mockMapper.Setup(mapper => mapper.Map<X12MessageV1>(entity2)).Returns(dto2);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByX12FunctionalGroup(searchId);

        // Assert
        var result = actionResult.GetOkList<X12MessageV1>();
        Assert.AreEqual(2, result.Count);
        Assert.AreEqual(dto1.Id, result[0].Id);
        Assert.AreEqual(dto2.Id, result[1].Id);
    }

    [TestMethod]
    public async Task GetByX12FunctionalGroup_ReturnsNoContent_WhenNoneFound()
    {
        // Arrange
        var (mockRepository, mockMapper) = GetMocks();

        var searchId = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByFunctionalGroupAsync(searchId)).ReturnsAsync([]);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByX12FunctionalGroup(searchId);

        // Assert
        _ = actionResult.GetNoContent();
    }

    [TestMethod]
    public async Task GetByX12FunctionalGroupAndLevel_ReturnsResults()
    {
        // Arrange
        var (dto1, entity1) = BuildModels();
        var (dto2, entity2) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();

        var searchId = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByFunctionalGroupAsync(searchId, ProcessLogConstants.MessageLevel.Fatal)).ReturnsAsync([entity1, entity2]);

        mockMapper.Setup(mapper => mapper.Map<X12MessageV1>(entity1)).Returns(dto1);
        mockMapper.Setup(mapper => mapper.Map<X12MessageV1>(entity2)).Returns(dto2);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByX12FunctionalGroup(searchId, ProcessLogConstants.MessageLevel.Fatal);

        // Assert
        var result = actionResult.GetOkList<X12MessageV1>();
        Assert.AreEqual(2, result.Count);
        Assert.AreEqual(dto1.Id, result[0].Id);
        Assert.AreEqual(dto2.Id, result[1].Id);
    }

    [TestMethod]
    public async Task GetByX12FunctionalGroupLevel_ReturnsNoContent_WhenNoneFound()
    {
        // Arrange
        var (mockRepository, mockMapper) = GetMocks();

        var searchId = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByFunctionalGroupAsync(searchId, ProcessLogConstants.MessageLevel.Fatal)).ReturnsAsync([]);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByX12FunctionalGroup(searchId, ProcessLogConstants.MessageLevel.Fatal);

        // Assert
        _ = actionResult.GetNoContent();
    }
    #endregion Get By X12FunctionalGroup

    #region Get By X12TransactionSet
    [TestMethod]
    public async Task GetByX12TransactionSet_ReturnsResults()
    {
        // Arrange
        var (dto1, entity1) = BuildModels();
        var (dto2, entity2) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();

        var searchId = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByTransactionSetAsync(searchId)).ReturnsAsync([entity1, entity2]);

        mockMapper.Setup(mapper => mapper.Map<X12MessageV1>(entity1)).Returns(dto1);
        mockMapper.Setup(mapper => mapper.Map<X12MessageV1>(entity2)).Returns(dto2);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByX12TransactionSet(searchId);

        // Assert
        var result = actionResult.GetOkList<X12MessageV1>();
        Assert.AreEqual(2, result.Count);
        Assert.AreEqual(dto1.Id, result[0].Id);
        Assert.AreEqual(dto2.Id, result[1].Id);
    }

    [TestMethod]
    public async Task GetByX12TransactionSet_ReturnsNoContent_WhenNoneFound()
    {
        // Arrange
        var (mockRepository, mockMapper) = GetMocks();

        var searchId = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByTransactionSetAsync(searchId)).ReturnsAsync([]);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByX12TransactionSet(searchId);

        // Assert
        _ = actionResult.GetNoContent();
    }

    [TestMethod]
    public async Task GetByX12TransactionSetAndLevel_ReturnsResults()
    {
        // Arrange
        var (dto1, entity1) = BuildModels();
        var (dto2, entity2) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();

        var searchId = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByTransactionSetAsync(searchId, ProcessLogConstants.MessageLevel.Fatal)).ReturnsAsync([entity1, entity2]);

        mockMapper.Setup(mapper => mapper.Map<X12MessageV1>(entity1)).Returns(dto1);
        mockMapper.Setup(mapper => mapper.Map<X12MessageV1>(entity2)).Returns(dto2);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByX12TransactionSet(searchId, ProcessLogConstants.MessageLevel.Fatal);

        // Assert
        var result = actionResult.GetOkList<X12MessageV1>();
        Assert.AreEqual(2, result.Count);
        Assert.AreEqual(dto1.Id, result[0].Id);
        Assert.AreEqual(dto2.Id, result[1].Id);
    }

    [TestMethod]
    public async Task GetByX12TransactionSetLevel_ReturnsNoContent_WhenNoneFound()
    {
        // Arrange
        var (mockRepository, mockMapper) = GetMocks();

        var searchId = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByTransactionSetAsync(searchId, ProcessLogConstants.MessageLevel.Fatal)).ReturnsAsync([]);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByX12TransactionSet(searchId, ProcessLogConstants.MessageLevel.Fatal);

        // Assert
        _ = actionResult.GetNoContent();
    }
    #endregion Get By X12TransactionSet
}
