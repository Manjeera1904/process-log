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
public class FileProcessLogController
    : BaseControllerWithoutHistory<FileProcessLogV1, FileProcessLog, IFileProcessLogRepository>
{
    public FileProcessLogController(IBaseControllerServices services)
        : base(services)
    {
    }

    #region V1

    [HttpGet]
    [MapToApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(IEnumerable<FileProcessLogV1>))]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public override async Task<IActionResult> Get()
        => await InternalGetAllAsync();

    [HttpGet("{id:guid}")]
    [MapToApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(FileProcessLogV1))]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public override async Task<IActionResult> Get(Guid id)
        => await InternalGetAsync(id);

    [HttpGet("ProcessLog/{processLogId:guid}")]
    [MapToApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(IEnumerable<FileProcessLogV1>))]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public async Task<IActionResult> GetByProcessLog(Guid processLogId)
        => await GetMany(async repo =>
            (await repo.GetByProcessLogAsync(processLogId)).AsEnumerable());

    [HttpPost]
    [MapToApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status201Created, Type = typeof(FileProcessLogV1))]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status409Conflict)]
    public override async Task<IActionResult> Post([FromBody] FileProcessLogV1 dto)
        => await InternalPostAsync(dto);

    [HttpPut("{id:guid}")]
    [MapToApiVersion("1.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(FileProcessLogV1))]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status409Conflict)]
    public override async Task<IActionResult> Put(Guid id, [FromBody] FileProcessLogV1 dto)
        => await InternalPutAsync(id, dto);

    #endregion

    #region V2

    [HttpGet]
    [MapToApiVersion("2.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(IEnumerable<FileProcessLogV2>))]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public async Task<IActionResult> GetV2()
    {
        var entities = await _lazyRepository.Value.GetAllAsync();

        if (entities == null || entities.Count == 0)
            return NoContent();

        return Ok(_mapper.Map<IEnumerable<FileProcessLogV2>>(entities));
    }

    [HttpGet("{id:guid}")]
    [MapToApiVersion("2.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(FileProcessLogV2))]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public async Task<IActionResult> GetV2(Guid id)
    {
        var entity = await _lazyRepository.Value.GetByIdAsync(id);

        if (entity == null)
            return NotFound();

        return Ok(_mapper.Map<FileProcessLogV2>(entity));
    }

    [HttpGet("ProcessLog/{processLogId:guid}")]
    [MapToApiVersion("2.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(IEnumerable<FileProcessLogV2>))]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public async Task<IActionResult> GetByProcessLogV2(Guid processLogId)
    {
        var entities =
            (await _lazyRepository.Value.GetByProcessLogAsync(processLogId))
            .ToList();

        if (entities.Count == 0)
            return NoContent();

        return Ok(_mapper.Map<IEnumerable<FileProcessLogV2>>(entities));
    }

    [HttpPost]
    [MapToApiVersion("2.0")]
    [ProducesResponseType(StatusCodes.Status201Created, Type = typeof(FileProcessLogV2))]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status409Conflict)]
    [ProducesResponseType(StatusCodes.Status500InternalServerError)]
    public async Task<IActionResult> PostV2([FromBody] FileProcessLogV2 dto)
    {
        try
        {
            var entity = _mapper.Map<FileProcessLog>(dto);

            var savedEntity = await _lazyRepository.Value.InsertAsync(entity);

            var persistedEntity =
                await _lazyRepository.Value.GetByIdAsync(savedEntity.Id);

            if (persistedEntity == null)
                return StatusCode(500, "Failed to retrieve saved entity");

            return CreatedAtAction(
                nameof(GetV2),
                new { id = persistedEntity.Id },
                _mapper.Map<FileProcessLogV2>(persistedEntity));
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

    [HttpPut("{id:guid}")]
    [MapToApiVersion("2.0")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(FileProcessLogV2))]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status409Conflict)]
    [ProducesResponseType(StatusCodes.Status500InternalServerError)]
    public async Task<IActionResult> PutV2(Guid id, [FromBody] FileProcessLogV2 dto)
    {
        if (id != dto.Id)
            return BadRequest("ID mismatch");

        if (dto.RowVersion == null)
        {
            ModelState.AddModelError(
                nameof(dto.RowVersion),
                "RowVersion is required for updates"
            );
            return BadRequest(ModelState);
        }

        try
        {
            var entity = _mapper.Map<FileProcessLog>(dto);
            entity.Id = id;

            await _lazyRepository.Value.UpdateAsync(entity);

            var persistedEntity =
                await _lazyRepository.Value.GetByIdAsync(id);

            if (persistedEntity == null)
                return NotFound();

            return Ok(_mapper.Map<FileProcessLogV2>(persistedEntity));
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
