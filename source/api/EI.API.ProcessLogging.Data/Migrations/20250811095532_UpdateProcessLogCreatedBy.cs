using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace EI.API.ProcessLogging.Data.Migrations;

/// <inheritdoc />
public partial class UpdateProcessLogCreatedBy : Migration
{
    /// <inheritdoc />
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.AddColumn<string>(
            name: "CreatedBy",
            table: "ProcessLogs",
            type: "nvarchar(max)",
            nullable: true)
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogsHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");
    }

    /// <inheritdoc />
    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropColumn(
            name: "CreatedBy",
            table: "ProcessLogs")
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogsHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");
    }
}
