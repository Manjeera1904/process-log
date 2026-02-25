using Asp.Versioning;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Data.Repositories;
using EI.API.ProcessLogging.Model;
using EI.API.Service.Data.Helpers.Exceptions;
using EI.API.Service.Rest.Helpers.Controllers;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace EI.API.ProcessLogging.Controllers;

[ApiController]
[Route("api/[controller]")]
[ApiVersion("1.0")]
[ApiVersion("2.0")]
[Authorize(AuthenticationSchemes = JwtBearerDefaults.AuthenticationScheme)]
public class ProcessLogMessageController
    : BaseControllerWithoutHistory<
        ProcessLogMessageV1,
        ProcessLogMessage,
        IProcessLogMessageRepository>
{
    public ProcessLogMessageController(IBaseControllerServices services)
        : base(services)
    {
    }
    #region V1

    [HttpGet]
    [MapToApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(IEnumerable<ProcessLogMessageV1>))]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public override async Task<IActionResult> Get()
        => await InternalGetAllAsync();

    [HttpGet("{id:guid}")]
    [MapToApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(ProcessLogMessageV1))]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public override async Task<IActionResult> Get(Guid id)
        => await InternalGetAsync(id);

    [HttpGet("ProcessLog/{processLogId:guid}")]
    [MapToApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(IEnumerable<ProcessLogMessageV1>))]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public async Task<IActionResult> GetByProcessLog(
        Guid processLogId,
        string? messageLevel = null)
        => messageLevel == null
            ? await GetMany(async repo =>
                (await repo.GetByProcessLogAsync(processLogId)).AsEnumerable())
            : await GetMany(async repo =>
                (await repo.GetByProcessLogAsync(processLogId, messageLevel)).AsEnumerable());

    [HttpPost]
    [MapToApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status201Created, Type = typeof(ProcessLogMessageV1))]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status409Conflict)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public override async Task<IActionResult> Post(
        [FromBody] ProcessLogMessageV1 dto)
        => await InternalPostAsync(dto);

    // [HttpPut("{id:guid}")] // Disable PUT
    // [ApiVersion("1.0")]    // Disable PUT
    // [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(ProcessLogMessageV1))]
    // [ProducesResponseType(StatusCodes.Status400BadRequest)]
    // [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    // [ProducesResponseType(StatusCodes.Status404NotFound)]
    // [ProducesResponseType(StatusCodes.Status409Conflict)]
    [ApiExplorerSettings(IgnoreApi = true)]
    public override Task<IActionResult> Put(
        Guid id,
        [FromBody] ProcessLogMessageV1 dto)
        => Task.FromResult<IActionResult>(
            BadRequest($"Can not PUT to {nameof(ProcessLogMessage)}"));

    #endregion

    #region V2

    [HttpGet]
    [MapToApiVersion("2.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(IEnumerable<ProcessLogMessageV2>))]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public async Task<IActionResult> GetV2()
    {
        var entities =
            await _lazyRepository.Value.GetAllAsync();

        if (!entities.Any())
            return NoContent();

        return Ok(
            _mapper.Map<IEnumerable<ProcessLogMessageV2>>(entities));
    }

    [HttpGet("{id:guid}")]
    [MapToApiVersion("2.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(ProcessLogMessageV2))]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public async Task<IActionResult> GetV2(Guid id)
    {
        var entity =
            await _lazyRepository.Value.GetByIdAsync(id);

        if (entity == null)
            return NotFound();

        return Ok(
            _mapper.Map<ProcessLogMessageV2>(entity));
    }

    [HttpGet("ProcessLog/{processLogId:guid}")]
    [MapToApiVersion("2.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(IEnumerable<ProcessLogMessageV2>))]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public async Task<IActionResult> GetByProcessLogV2(
        Guid processLogId,
        string? messageLevel = null)
    {
        var entities = messageLevel == null
            ? (await _lazyRepository.Value
                .GetByProcessLogAsync(processLogId)).ToList()
            : (await _lazyRepository.Value
                .GetByProcessLogAsync(processLogId, messageLevel)).ToList();

        if (!entities.Any())
            return NoContent();

        return Ok(
            _mapper.Map<IEnumerable<ProcessLogMessageV2>>(entities));
    }

    [HttpPost]
    [MapToApiVersion("2.0")]
    [ProducesResponseType(StatusCodes.Status201Created, Type = typeof(ProcessLogMessageV2))]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status409Conflict)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    [ProducesResponseType(StatusCodes.Status500InternalServerError)]
    public async Task<IActionResult> PostV2([FromBody] ProcessLogMessageV2 dto)
    {
        try
        {
            var entity = _mapper.Map<ProcessLogMessage>(dto);

            var savedEntity = await _lazyRepository.Value.InsertAsync(entity);

            var persistedEntity =
                await _lazyRepository.Value.GetByIdAsync(savedEntity.Id);

            if (persistedEntity == null)
                return StatusCode(500, "Failed to retrieve saved entity");

            return CreatedAtAction(
                nameof(GetV2),
                new { id = persistedEntity.Id },
                _mapper.Map<ProcessLogMessageV2>(persistedEntity));
        }
        catch (Exception ex) when (
    ex is PrimaryKeyConflictException or
    UniqueConstraintConflictException)
        {
            var message =
                ex is PrimaryKeyConflictException
                    ? "A record with this key already exists"
                    : "This record conflicts with an existing uniqueness constraint";

            return Conflict(message);
        }
    }

    #endregion
}
