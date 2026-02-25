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
public class MessageLevelControllerTests
    : BaseReadTranslationControllerWithoutHistoryTests<IMessageLevelRepository, MessageLevelController, MessageLevel, MessageLevelTranslation, MessageLevelV1>
{
    /*
    protected override MessageLevelController GetController(Mock<IMessageLevelRepository> mockRepository, Mock<IMapper> mockMapper)
    {
        var mockServices = base.SetupBaseControllerServices<IMessageLevelControllerServices>(mockRepository, mockMapper);

        var controller = new MessageLevelController(mockServices.Object);
        return controller;
    }
    */

    [TestMethod]
    public async Task GetByLevel_ReturnsMessageLevel_WithCultureCode()
    {
        // Arrange
        const string testCultureCode = "ABC";
        const string searchName = "TestMessageLevel";
        var (dto1, entity1) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();
        mockRepository.Setup(repo => repo.GetAsync(searchName, testCultureCode)).ReturnsAsync(entity1);

        mockMapper.Setup(mapper => mapper.Map<MessageLevelV1>(entity1)).Returns(dto1);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByLevel(searchName, testCultureCode);

        // Assert
        var result = actionResult.GetOkResult<MessageLevelV1>();
        Assert.AreEqual(entity1.Id, result.Id);
    }

    [TestMethod]
    public async Task GetByLevel_ReturnsMessageLevel_WithoutCultureCode()
    {
        // Arrange
        const string searchName = "TestMessageLevel";
        var (dto1, entity1) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();
        mockRepository.Setup(repo => repo.GetAsync(searchName, ServiceConstants.CultureCode.Default)).ReturnsAsync(entity1);

        mockMapper.Setup(mapper => mapper.Map<MessageLevelV1>(entity1)).Returns(dto1);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByLevel(searchName);

        // Assert
        var result = actionResult.GetOkResult<MessageLevelV1>();
        Assert.AreEqual(entity1.Id, result.Id);
    }

    [TestMethod]
    public async Task GetByLevel_ReturnsNotFound()
    {
        // Arrange
        const string searchName = "TestMessageLevel";

        var (mockRepository, mockMapper) = GetMocks();
        mockRepository.Setup(repo => repo.GetAsync(searchName, ServiceConstants.CultureCode.Default)).ReturnsAsync((MessageLevel?) null);

        mockMapper.Setup(mapper => mapper.Map<MessageLevelV1>(null)).Returns((MessageLevelV1?) null!);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.GetByLevel(searchName);

        // Assert
        Assert.IsInstanceOfType<NotFoundResult>(actionResult);
    }
}
