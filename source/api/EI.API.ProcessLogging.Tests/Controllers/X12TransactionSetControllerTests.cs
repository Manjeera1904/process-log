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
public class X12TransactionSetControllerTests
    : BaseControllerWithoutHistoryTests<IX12TransactionSetRepository, X12TransactionSetController, X12TransactionSet, X12TransactionSetV1>
{
    /*
    protected override X12TransactionSetController GetController(Mock<IX12TransactionSetRepository> mockRepository, Mock<IMapper> mockMapper)
    {
        var mockServices = base.SetupBaseControllerServices<IX12TransactionSetControllerServices>(mockRepository, mockMapper);

        var controller = new X12TransactionSetController(mockServices.Object);
        return controller;
    }
    */

    [TestMethod]
    public async Task GetByX12FunctionalGroup_ReturnsResults()
    {
        // Arrange
        var (dto1, entity1) = BuildModels();
        var (dto2, entity2) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();

        var searchId = Guid.NewGuid();

        mockRepository.Setup(repo => repo.GetByFunctionalGroup(searchId)).ReturnsAsync([entity1, entity2]);

        mockMapper.Setup(mapper => mapper.Map<X12TransactionSetV1>(entity1)).Returns(dto1);
        mockMapper.Setup(mapper => mapper.Map<X12TransactionSetV1>(entity2)).Returns(dto2);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByX12FunctionalGroup(searchId);

        // Assert
        var result = actionResult.GetOkList<X12TransactionSetV1>();
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

        mockRepository.Setup(repo => repo.GetByFunctionalGroup(searchId)).ReturnsAsync([]);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByX12FunctionalGroup(searchId);

        // Assert
        _ = actionResult.GetNoContent();
    }
}
