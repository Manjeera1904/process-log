using Asp.Versioning;
using EI.API.ProcessLogging.Data.App;
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
public class ActivityTypeController(IBaseControllerServices services)
    : BaseReadTranslationControllerWithoutHistory<ActivityTypeV1, ActivityType, ActivityTypeTranslation, IActivityTypeRepository>(services)
{
    [HttpGet]
    [ApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(IEnumerable<ActivityTypeV1>))]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    [Authorize(Permissions.ViewActivityTypes)]
    public override async Task<IActionResult> Get([FromQuery] string? cultureCode = null)
        => await InternalGetAsync(cultureCode);

    [HttpGet("{id:guid}")]
    [ApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(ActivityTypeV1))]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    [Authorize(Permissions.ViewActivityTypes)]
    public override async Task<IActionResult> Get(Guid id, [FromQuery] string? cultureCode = null)
        => await InternalGetAsync(id, cultureCode);

    [HttpGet("type/{type}")]
    [ApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(ActivityTypeV1))]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    [Authorize(Permissions.ViewActivityTypes)]
    public async Task<IActionResult> GetByType(string type, [FromQuery] string? cultureCode = null)
        => await GetOne(async repo => await repo.GetAsync(type, cultureCode ?? ServiceConstants.CultureCode.Default));
}
