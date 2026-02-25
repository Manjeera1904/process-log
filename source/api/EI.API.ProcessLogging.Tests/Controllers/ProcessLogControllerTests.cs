using AutoMapper;
using EI.API.ProcessLogging.Controllers;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Models;
using EI.API.ProcessLogging.Data.Repositories;
using EI.API.ProcessLogging.Model;
using EI.Data.TestHelpers.Controllers;
using EI.Data.TestHelpers.Controllers.Helper;
using Microsoft.AspNetCore.Mvc;
using Moq;
using static EI.API.ProcessLogging.Data.ProcessLogConstants;

namespace EI.API.ProcessLogging.Tests.Controllers;

[TestClass]
public class ProcessLogControllerTests
    : BaseControllerWithoutHistoryTests<IProcessLogRepository, ProcessLogController, ProcessLog, ProcessLogV1>
{
    /*
    protected override ProcessLogController GetController(Mock<IProcessLogRepository> mockRepository, Mock<IMapper> mockMapper)
    {
        var mockServices = base.SetupBaseControllerServices<IProcessLogControllerServices>(mockRepository, mockMapper);

        var controller = new ProcessLogController(mockServices.Object);
        return controller;
    }
    */
    [TestMethod]
    public async Task Search_ReturnsResults()
    {
        // Arrange
        var (dto1, entity1) = BuildModels();
        var (dto2, entity2) = BuildModels();

        var (mockRepository, mockMapper) = GetMocks();

        var searchRequest = new ProcessLogSearch
        {
            ActivityType = "testActivityType",
            DateRange = "Last30Days",
            TimeZone = "UTC",
            PageNumber = 1,
            PageSize = 10
        };

        var pagedResult = new PagedResult<ProcessLog>
        {
            Items = new List<ProcessLog> { entity1, entity2 },
            TotalCount = 2,
            PageNumber = 1,
            PageSize = 10
        };

        mockRepository
            .Setup(repo => repo.SearchAsync(searchRequest))
            .ReturnsAsync(pagedResult);

        // Setup for mapping a single ProcessLog → ProcessLogWithFilesV1
        mockMapper
            .Setup(m => m.Map<ProcessLogWithFilesV1>(It.IsAny<ProcessLog>()))
            .Returns((ProcessLog src) => new ProcessLogWithFilesV1
            {
                Id = src.Id,
                Type = src.Type,
                Status = src.Status
            });

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.Search(searchRequest);

        // Assert
        var result = actionResult.GetOkResult<PagedResult<ProcessLogWithFilesV1>>();
        Assert.AreEqual(2, result.Items.Count);
        Assert.AreEqual(dto1.Id, result.Items[0].Id);
        Assert.AreEqual(dto2.Id, result.Items[1].Id);
    }

    [TestMethod]
    public async Task Search_ReturnsNoContent_WhenNoneFound()
    {
        // Arrange
        var (mockRepository, mockMapper) = GetMocks();

        var searchRequest = new ProcessLogSearch
        {
            ActivityType = "testActivityType",
            DateRange = "Last30Days",
            TimeZone = "UTC",
            PageNumber = 1,
            PageSize = 10
        };

        var emptyResult = new PagedResult<ProcessLog>
        {
            Items = new List<ProcessLog>(),
            TotalCount = 0,
            PageNumber = 1,
            PageSize = 10
        };

        mockRepository.Setup(repo => repo.SearchAsync(searchRequest)).ReturnsAsync(emptyResult);

        var controller = GetController(mockRepository, mockMapper);

        // Act
        var actionResult = await controller.Search(searchRequest);

        // Assert
        _ = actionResult.GetNoContent();
    }
}
