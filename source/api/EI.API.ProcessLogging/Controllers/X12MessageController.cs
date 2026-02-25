using Asp.Versioning;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.API.ProcessLogging.Model;
using EI.API.Service.Rest.Helpers.Controllers;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace EI.API.ProcessLogging.Controllers;

[ApiController, Route("api/[controller]")]
[Authorize(AuthenticationSchemes = JwtBearerDefaults.AuthenticationScheme)]
public class X12MessageController(IBaseControllerServices services)
    : BaseControllerWithoutHistory<X12MessageV1, X12Message, IX12MessageRepository>(services)
{
    [HttpGet]
    [ApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(IEnumerable<X12MessageV1>))]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public override async Task<IActionResult> Get()
        => await InternalGetAllAsync();

    [HttpGet("{id:guid}")]
    [ApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(X12MessageV1))]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public override async Task<IActionResult> Get(Guid id)
        => await InternalGetAsync(id);

    [HttpGet("X12Interchange/{x12InterchangeId:guid}")]
    [ApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(IEnumerable<X12MessageV1>))]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public async Task<IActionResult> GetByX12Interchange(Guid x12InterchangeId, string? messageLevel = null)
        => messageLevel == null
               ? await GetMany(async repo => await repo.GetByInterchangeAsync(x12InterchangeId))
               : await GetMany(async repo => await repo.GetByInterchangeAsync(x12InterchangeId, messageLevel));

    [HttpGet("X12FunctionalGroup/{x12FunctionalGroupId:guid}")]
    [ApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(IEnumerable<X12MessageV1>))]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public async Task<IActionResult> GetByX12FunctionalGroup(Guid x12FunctionalGroupId, string? messageLevel = null)
        => messageLevel == null
               ? await GetMany(async repo => await repo.GetByFunctionalGroupAsync(x12FunctionalGroupId))
               : await GetMany(async repo => await repo.GetByFunctionalGroupAsync(x12FunctionalGroupId, messageLevel));

    [HttpGet("X12TransactionSet/{x12TransactionSetId:guid}")]
    [ApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(IEnumerable<X12MessageV1>))]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public async Task<IActionResult> GetByX12TransactionSet(Guid x12TransactionSetId, string? messageLevel = null)
        => messageLevel == null
               ? await GetMany(async repo => await repo.GetByTransactionSetAsync(x12TransactionSetId))
               : await GetMany(async repo => await repo.GetByTransactionSetAsync(x12TransactionSetId, messageLevel));

    [HttpPost]
    [ApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status201Created, Type = typeof(X12MessageV1))]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status409Conflict)]
    public override async Task<IActionResult> Post([FromBody] X12MessageV1 dto)
        => await InternalPostAsync(dto);

    // [HttpPut("{id:guid}")] // Disable PUT
    // [ApiVersion("1.0")]    // Disable PUT
    // [ProducesResponseType(StatusCodes.Status201Created, Type = typeof(X12MessageV1))]
    // [ProducesResponseType(StatusCodes.Status400BadRequest)]
    // [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    // [ProducesResponseType(StatusCodes.Status404NotFound)]
    // [ProducesResponseType(StatusCodes.Status409Conflict)]
    public override Task<IActionResult> Put(Guid id, [FromBody] X12MessageV1 dto)
        => Task.FromResult<IActionResult>(BadRequest($"Can not POST to {nameof(X12Message)}"));
}
