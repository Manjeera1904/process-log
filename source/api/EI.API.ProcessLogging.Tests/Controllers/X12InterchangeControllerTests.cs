using AutoMapper;
using EI.API.ProcessLogging.Controllers;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.API.ProcessLogging.Model;
using EI.Data.TestHelpers.Controllers;
using EI.Data.TestHelpers.Controllers.Helper;
using Moq;

namespace EI.API.ProcessLogging.Tests.Controllers;

[TestClass]
public class X12InterchangeControllerTests
    : BaseControllerWithoutHistoryTests<IX12InterchangeRepository, X12InterchangeController, X12Interchange, X12InterchangeV1>
{
    /*
    protected override X12InterchangeController GetController(Mock<IX12InterchangeRepository> mockRepository, Mock<IMapper> mockMapper)
    {
        var mockServices = base.SetupBaseControllerServices<IX12InterchangeControllerServices>(mockRepository, mockMapper);

        var controller = new X12InterchangeController(mockServices.Object);
        return controller;
    }
    */

    [TestMethod]
    public async Task GetByProcessLog_ReturnsResults()
    {
        // Arrange
        var (dto1, entity1) = BuildModels();
        var (dto2, entity2) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();

        var searchId = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByProcessLogAsync(searchId)).ReturnsAsync([entity1, entity2]);

        mockMapper.Setup(mapper => mapper.Map<X12InterchangeV1>(entity1)).Returns(dto1);
        mockMapper.Setup(mapper => mapper.Map<X12InterchangeV1>(entity2)).Returns(dto2);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByProcessLog(searchId);

        // Assert
        var result = actionResult.GetOkList<X12InterchangeV1>();
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

        mockRepository.Setup(repo => repo.GetByProcessLogAsync(searchId)).ReturnsAsync([]);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByProcessLog(searchId);

        // Assert
        _ = actionResult.GetNoContent();
    }

    [TestMethod]
    public async Task GetByFileProcessLog_ReturnsResults()
    {
        // Arrange
        var (dto1, entity1) = BuildModels();
        var (dto2, entity2) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();

        var searchId = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByFileProcessLogAsync(searchId)).ReturnsAsync([entity1, entity2]);

        mockMapper.Setup(mapper => mapper.Map<X12InterchangeV1>(entity1)).Returns(dto1);
        mockMapper.Setup(mapper => mapper.Map<X12InterchangeV1>(entity2)).Returns(dto2);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByFileProcessLog(searchId);

        // Assert
        var result = actionResult.GetOkList<X12InterchangeV1>();
        Assert.AreEqual(2, result.Count);
        Assert.AreEqual(dto1.Id, result[0].Id);
        Assert.AreEqual(dto2.Id, result[1].Id);
    }

    [TestMethod]
    public async Task GetByFileProcessLog_ReturnsNoContent_WhenNoneFound()
    {
        // Arrange
        var (mockRepository, mockMapper) = GetMocks();

        var searchId = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByFileProcessLogAsync(searchId)).ReturnsAsync([]);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByFileProcessLog(searchId);

        // Assert
        _ = actionResult.GetNoContent();
    }
}
