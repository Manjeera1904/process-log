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
public class MessageLevelController(IBaseControllerServices services)
: BaseReadTranslationControllerWithoutHistory<MessageLevelV1, MessageLevel, MessageLevelTranslation, IMessageLevelRepository>(services)
{
    [HttpGet]
    [ApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(IEnumerable<MessageLevelV1>))]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public override async Task<IActionResult> Get([FromQuery] string? cultureCode = null)
        => await InternalGetAsync(cultureCode);

    [HttpGet("{id:guid}")]
    [ApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(MessageLevelV1))]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public override async Task<IActionResult> Get(Guid id, [FromQuery] string? cultureCode = null)
        => await InternalGetAsync(id, cultureCode);

    [HttpGet("level/{level}")]
    [ApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(MessageLevelV1))]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public async Task<IActionResult> GetByLevel(string level, [FromQuery] string? cultureCode = null)
        => await GetOne(async repo => await repo.GetAsync(level, cultureCode ?? ServiceConstants.CultureCode.Default));
}
