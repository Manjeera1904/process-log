using Asp.Versioning;
using AutoMapper;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Models;
using EI.API.ProcessLogging.Data.Repositories;
using EI.API.ProcessLogging.Model;
using EI.API.Service.Rest.Helpers.Controllers;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace EI.API.ProcessLogging.Controllers;

[ApiController, Route("api/[controller]")]
[Authorize(AuthenticationSchemes = JwtBearerDefaults.AuthenticationScheme)]
public class ProcessLogController(IBaseControllerServices services)
    : BaseControllerWithoutHistory<ProcessLogV1, ProcessLog, IProcessLogRepository>(services)
{
    [HttpGet]
    [ApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(IEnumerable<ProcessLogV1>))]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public override async Task<IActionResult> Get()
        => await InternalGetAllAsync();

    [HttpGet("{id:guid}")]
    [ApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(ProcessLogV1))]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public override async Task<IActionResult> Get(Guid id)
        => await InternalGetAsync(id);

    [HttpGet("Search")]
    [ApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(PagedResult<ProcessLogV1>))]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public async Task<IActionResult> Search([FromQuery] ProcessLogSearch request)
    {
        // Set default timezone if not provided
        request.TimeZone = !string.IsNullOrWhiteSpace(request.TimeZone)
    ? request.TimeZone.Trim()
    : "UTC";

        var result = await _lazyRepository.Value.SearchAsync(request);

        if (result?.Items == null || result.Items.Count == 0)
            return NoContent();
        var mapped = new PagedResult<ProcessLogWithFilesV1>
        {
            Items = result.Items.Select(x =>
            {
                var mappedItem = _mapper.Map<ProcessLogWithFilesV1>(x);
                return mappedItem;
            }).ToList(),
            TotalCount = result.TotalCount,
            PageNumber = result.PageNumber,
            PageSize = result.PageSize
        };
        return (Ok(mapped));
    }

    [HttpPost]
    [ApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status201Created, Type = typeof(ProcessLogV1))]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status409Conflict)]
    public override async Task<IActionResult> Post([FromBody] ProcessLogV1 dto)
        => await InternalPostAsync(dto);

    [HttpPut("{id:guid}")]
    [ApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(ProcessLogV1))]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status409Conflict)]
    public override async Task<IActionResult> Put(Guid id, [FromBody] ProcessLogV1 dto)
        => await InternalPutAsync(id, dto);

}
