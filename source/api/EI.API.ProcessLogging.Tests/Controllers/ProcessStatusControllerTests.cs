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
public class ProcessStatusControllerTests
    : BaseReadTranslationControllerWithoutHistoryTests<IProcessStatusRepository, ProcessStatusController, ProcessStatus, ProcessStatusTranslation, ProcessStatusV1>
{
    /*
    protected override ProcessStatusController GetController(Mock<IProcessStatusRepository> mockRepository, Mock<IMapper> mockMapper)
    {
        var mockServices = base.SetupBaseControllerServices<IProcessStatusControllerServices>(mockRepository, mockMapper);

        var controller = new ProcessStatusController(mockServices.Object);
        return controller;
    }

    */
    [TestMethod]
    public async Task GetByStatus_ReturnsProcessStatus_WithCultureCode()
    {
        // Arrange
        const string testCultureCode = "ABC";
        const string searchName = "TestProcessStatus";
        var (dto1, entity1) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();
        mockRepository.Setup(repo => repo.GetAsync(searchName, testCultureCode)).ReturnsAsync(entity1);

        mockMapper.Setup(mapper => mapper.Map<ProcessStatusV1>(entity1)).Returns(dto1);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByStatus(searchName, testCultureCode);

        // Assert
        var result = actionResult.GetOkResult<ProcessStatusV1>();
        Assert.AreEqual(entity1.Id, result.Id);
    }

    [TestMethod]
    public async Task GetByStatus_ReturnsProcessStatus_WithoutCultureCode()
    {
        // Arrange
        const string searchName = "TestProcessStatus";
        var (dto1, entity1) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();
        mockRepository.Setup(repo => repo.GetAsync(searchName, ServiceConstants.CultureCode.Default)).ReturnsAsync(entity1);

        mockMapper.Setup(mapper => mapper.Map<ProcessStatusV1>(entity1)).Returns(dto1);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByStatus(searchName);

        // Assert
        var result = actionResult.GetOkResult<ProcessStatusV1>();
        Assert.AreEqual(entity1.Id, result.Id);
    }

    [TestMethod]
    public async Task GetByStatus_ReturnsNotFound()
    {
        // Arrange
        const string searchName = "TestProcessStatus";

        var (mockRepository, mockMapper) = GetMocks();
        mockRepository.Setup(repo => repo.GetAsync(searchName, ServiceConstants.CultureCode.Default)).ReturnsAsync((ProcessStatus?) null);

        mockMapper.Setup(mapper => mapper.Map<ProcessStatusV1>(null)).Returns((ProcessStatusV1?) null!);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByStatus(searchName);

        // Assert
        Assert.IsInstanceOfType<NotFoundResult>(actionResult);
    }
}
