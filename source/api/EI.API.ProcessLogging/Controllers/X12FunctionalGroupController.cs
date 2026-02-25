using Asp.Versioning;
using AutoMapper;
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
public class X12FunctionalGroupController(IBaseControllerServices services)
    : BaseControllerWithoutHistory<X12FunctionalGroupV1, X12FunctionalGroup, IX12FunctionalGroupRepository>(services)
{
    [HttpGet]
    [ApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(IEnumerable<X12FunctionalGroupV1>))]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public override async Task<IActionResult> Get()
        => await InternalGetAllAsync();

    [HttpGet("{id:guid}")]
    [ApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(X12FunctionalGroupV1))]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public override async Task<IActionResult> Get(Guid id)
        => await InternalGetAsync(id);

    [HttpGet("X12Interchange/{x12InterchangeId:guid}")]
    [ApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(IEnumerable<X12FunctionalGroupV1>))]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public async Task<IActionResult> GetByX12Interchange(Guid x12InterchangeId)
        => await GetMany(async repo => await repo.GetByInterchangeAsync(x12InterchangeId));

    [HttpPost]
    [ApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status201Created, Type = typeof(X12FunctionalGroupV1))]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status409Conflict)]
    public override async Task<IActionResult> Post([FromBody] X12FunctionalGroupV1 dto)
        => await InternalPostAsync(dto);

    [HttpPut("{id:guid}")]
    [ApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(X12FunctionalGroupV1))]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status409Conflict)]
    public override async Task<IActionResult> Put(Guid id, [FromBody] X12FunctionalGroupV1 dto)
        => await InternalPutAsync(id, dto);

}
