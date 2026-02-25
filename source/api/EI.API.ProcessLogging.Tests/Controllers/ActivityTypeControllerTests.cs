using Autofac;
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
public class ActivityTypeControllerTests
    : BaseReadTranslationControllerWithoutHistoryTests<IActivityTypeRepository, ActivityTypeController, ActivityType, ActivityTypeTranslation, ActivityTypeV1>
{
    /*
    protected override ActivityTypeController GetController(Mock<IActivityTypeRepository> mockRepository, Mock<IMapper> mockMapper)
    {
        var mockServices = base.SetupBaseControllerServices<IActivityTypeControllerServices>(mockRepository, mockMapper);

        var controller = new ActivityTypeController(mockServices.Object);
        return controller;
    }
    */

    [TestMethod]
    public async Task GetByType_ReturnsActivityType_WithCultureCode()
    {
        // Arrange
        const string testCultureCode = "ABC";
        const string searchName = "TestActivityType";
        var (dto1, entity1) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();
        mockRepository.Setup(repo => repo.GetAsync(searchName, testCultureCode)).ReturnsAsync(entity1);

        mockMapper.Setup(mapper => mapper.Map<ActivityTypeV1>(entity1)).Returns(dto1);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByType(searchName, testCultureCode);

        // Assert
        var result = actionResult.GetOkResult<ActivityTypeV1>();
        Assert.AreEqual(entity1.Id, result.Id);
    }

    [TestMethod]
    public async Task GetByType_ReturnsActivityType_WithoutCultureCode()
    {
        // Arrange
        const string searchName = "TestActivityType";
        var (dto1, entity1) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();
        mockRepository.Setup(repo => repo.GetAsync(searchName, ServiceConstants.CultureCode.Default)).ReturnsAsync(entity1);

        mockMapper.Setup(mapper => mapper.Map<ActivityTypeV1>(entity1)).Returns(dto1);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByType(searchName);

        // Assert
        var result = actionResult.GetOkResult<ActivityTypeV1>();
        Assert.AreEqual(entity1.Id, result.Id);
    }

    [TestMethod]
    public async Task GetByType_ReturnsNotFound()
    {
        // Arrange
        const string searchName = "TestActivityType";

        var (mockRepository, mockMapper) = GetMocks();
        mockRepository.Setup(repo => repo.GetAsync(searchName, ServiceConstants.CultureCode.Default)).ReturnsAsync((ActivityType?) null);

        mockMapper.Setup(mapper => mapper.Map<ActivityTypeV1>(null)).Returns((ActivityTypeV1?) null!);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByType(searchName);

        // Assert
        Assert.IsInstanceOfType<NotFoundResult>(actionResult);
    }
}
