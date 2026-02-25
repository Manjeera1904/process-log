using AutoMapper;
using EI.API.ProcessLogging.Controllers;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.API.ProcessLogging.Model;
using EI.API.Service.Data.Helpers;
using EI.Data.TestHelpers.Controllers;
using EI.Data.TestHelpers.Controllers.Helper;
using Microsoft.AspNetCore.Mvc;
using Moq;

namespace EI.API.ProcessLogging.Tests.Controllers;

[TestClass]
public class X12StatusControllerTests
    : BaseReadTranslationControllerWithoutHistoryTests<IX12StatusRepository, X12StatusController, X12Status, X12StatusTranslation, X12StatusV1>
{
    /*
    protected override X12StatusController GetController(Mock<IX12StatusRepository> mockRepository, Mock<IMapper> mockMapper)
    {
        var mockServices = base.SetupBaseControllerServices<IX12StatusControllerServices>(mockRepository, mockMapper);

        var controller = new X12StatusController(mockServices.Object);
        return controller;
    }
    */

    [TestMethod]
    public async Task GetByStatus_ReturnsX12Status_WithCultureCode()
    {
        // Arrange
        const string testCultureCode = "ABC";
        const string searchName = "TestX12Status";
        var (dto1, entity1) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();
        mockRepository.Setup(repo => repo.GetAsync(searchName, testCultureCode)).ReturnsAsync(entity1);

        mockMapper.Setup(mapper => mapper.Map<X12StatusV1>(entity1)).Returns(dto1);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByStatus(searchName, testCultureCode);

        // Assert
        var result = actionResult.GetOkResult<X12StatusV1>();
        Assert.AreEqual(entity1.Id, result.Id);
    }

    [TestMethod]
    public async Task GetByStatus_ReturnsX12Status_WithoutCultureCode()
    {
        // Arrange
        const string searchName = "TestX12Status";
        var (dto1, entity1) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();
        mockRepository.Setup(repo => repo.GetAsync(searchName, ServiceConstants.CultureCode.Default)).ReturnsAsync(entity1);

        mockMapper.Setup(mapper => mapper.Map<X12StatusV1>(entity1)).Returns(dto1);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByStatus(searchName);

        // Assert
        var result = actionResult.GetOkResult<X12StatusV1>();
        Assert.AreEqual(entity1.Id, result.Id);
    }

    [TestMethod]
    public async Task GetByStatus_ReturnsNotFound()
    {
        // Arrange
        const string searchName = "TestX12Status";

        var (mockRepository, mockMapper) = GetMocks();
        mockRepository.Setup(repo => repo.GetAsync(searchName, ServiceConstants.CultureCode.Default)).ReturnsAsync((X12Status?) null);

        mockMapper.Setup(mapper => mapper.Map<X12StatusV1>(null)).Returns((X12StatusV1?) null!);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByStatus(searchName);

        // Assert
        Assert.IsInstanceOfType<NotFoundResult>(actionResult);
    }
}
