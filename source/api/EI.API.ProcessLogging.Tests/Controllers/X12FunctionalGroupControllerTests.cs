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
public class X12FunctionalGroupControllerTests
    : BaseControllerWithoutHistoryTests<IX12FunctionalGroupRepository, X12FunctionalGroupController, X12FunctionalGroup, X12FunctionalGroupV1>
{
    /*
    protected override X12FunctionalGroupController GetController(Mock<IX12FunctionalGroupRepository> mockRepository, Mock<IMapper> mockMapper)
    {
        var mockServices = base.SetupBaseControllerServices<IX12FunctionalGroupControllerServices>(mockRepository, mockMapper);

        var controller = new X12FunctionalGroupController(mockServices.Object);
        return controller;
    }
    */

    [TestMethod]
    public async Task GetByX12Interchange_ReturnsResults()
    {
        // Arrange
        var (dto1, entity1) = BuildModels();
        var (dto2, entity2) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();

        var searchId = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByInterchangeAsync(searchId)).ReturnsAsync([entity1, entity2]);

        mockMapper.Setup(mapper => mapper.Map<X12FunctionalGroupV1>(entity1)).Returns(dto1);
        mockMapper.Setup(mapper => mapper.Map<X12FunctionalGroupV1>(entity2)).Returns(dto2);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByX12Interchange(searchId);

        // Assert
        var result = actionResult.GetOkList<X12FunctionalGroupV1>();
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
}
