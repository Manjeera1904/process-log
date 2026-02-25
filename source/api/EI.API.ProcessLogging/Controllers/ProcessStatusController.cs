using Asp.Versioning;
using AutoMapper;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.API.ProcessLogging.Model;
using EI.API.Service.Data.Helpers;
using EI.API.Service.Rest.Helpers.Controllers;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace EI.API.ProcessLogging.Controllers;

[ApiController, Route("api/[controller]")]
[Authorize(AuthenticationSchemes = JwtBearerDefaults.AuthenticationScheme)]
public class ProcessStatusController(IBaseControllerServices services)
: BaseReadTranslationControllerWithoutHistory<ProcessStatusV1, ProcessStatus, ProcessStatusTranslation, IProcessStatusRepository>(services)
{
    [HttpGet]
    [ApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(IEnumerable<ProcessStatusV1>))]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public override async Task<IActionResult> Get([FromQuery] string? cultureCode = null)
        => await InternalGetAsync(cultureCode);

    [HttpGet("{id:guid}")]
    [ApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(ProcessStatusV1))]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public override async Task<IActionResult> Get(Guid id, [FromQuery] string? cultureCode = null)
        => await InternalGetAsync(id, cultureCode);

    [HttpGet("status/{status}")]
    [ApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(ProcessStatusV1))]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public async Task<IActionResult> GetByStatus(string status, [FromQuery] string? cultureCode = null)
        => await GetOne(async repo => await repo.GetAsync(status, cultureCode ?? ServiceConstants.CultureCode.Default));
}
