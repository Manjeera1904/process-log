using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace EI.API.ProcessLogging.Data.Migrations;

/// <inheritdoc />
public partial class ProcessLogs_AddCreatedByUserId : Migration
{
    /// <inheritdoc />
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder
            .AddColumn<Guid>(
                name: "CreatedByUserId",
                table: "ProcessLogs",
                type: "uniqueidentifier",
                nullable: true
            )
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogsHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");
    }

    /// <inheritdoc />
    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder
            .DropColumn(name: "CreatedByUserId", table: "ProcessLogs")
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogsHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");
    }
}
