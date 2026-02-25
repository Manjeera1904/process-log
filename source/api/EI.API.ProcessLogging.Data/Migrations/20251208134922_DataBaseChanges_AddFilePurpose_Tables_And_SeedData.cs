using Microsoft.EntityFrameworkCore.Migrations;
using System;

#nullable disable

#pragma warning disable CA1814 // Prefer jagged arrays over multidimensional

namespace EI.API.ProcessLogging.Data.Migrations;

/// <inheritdoc />
public partial class DataBaseChanges_AddFilePurpose_Tables_And_SeedData : Migration
{
    /// <inheritdoc />
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropIndex(
            name: "IX_FileProcessLogs_ProcessLogId",
            table: "FileProcessLogs");

        migrationBuilder.AddColumn<Guid>(
            name: "FileProcessLogId",
            table: "ProcessLogMessages",
            type: "uniqueidentifier",
            nullable: true)
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogMessagesHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.AddColumn<string>(
            name: "ProcessStatus",
            table: "FileProcessLogs",
            type: "nvarchar(50)",
            maxLength: 50,
            nullable: false,
            defaultValue: "New")
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "FileProcessLogsHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.AddColumn<string>(
            name: "PurposeName",
            table: "FileProcessLogs",
            type: "nvarchar(50)",
            maxLength: 50,
            nullable: false,
            defaultValue: "Originating Contract")
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "FileProcessLogsHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.CreateTable(
            name: "FilePurposes",
            columns: table => new
            {
                FilePurposeId = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                PurposeName = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: false),
                IsSystemGenerated = table.Column<bool>(type: "bit", nullable: false),
                UpdatedBy = table.Column<string>(type: "nvarchar(120)", maxLength: 120, nullable: false),
                RowVersion = table.Column<byte[]>(type: "rowversion", rowVersion: true, nullable: false)
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_FilePurposes", x => x.FilePurposeId);
                table.UniqueConstraint("AK_FilePurposes_PurposeName", x => x.PurposeName);
            });

        migrationBuilder.CreateTable(
            name: "FilePurposeTranslations",
            columns: table => new
            {
                FilePurposeId = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                CultureCode = table.Column<string>(type: "nvarchar(20)", maxLength: 20, nullable: false),
                Name = table.Column<string>(type: "nvarchar(max)", nullable: false),
                Description = table.Column<string>(type: "nvarchar(max)", maxLength: 8192, nullable: true),
                UpdatedBy = table.Column<string>(type: "nvarchar(120)", maxLength: 120, nullable: false),
                RowVersion = table.Column<byte[]>(type: "rowversion", rowVersion: true, nullable: false)
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_FilePurposeTranslations", x => new { x.FilePurposeId, x.CultureCode });
                table.ForeignKey(
                    name: "FK_FilePurposeTranslations_FilePurposes_FilePurposeId",
                    column: x => x.FilePurposeId,
                    principalTable: "FilePurposes",
                    principalColumn: "FilePurposeId",
                    onDelete: ReferentialAction.Restrict);
            });

        migrationBuilder.Sql(@"
                IF NOT EXISTS (SELECT 1 FROM FilePurposes WHERE PurposeName = 'Contract Pricing Rules')
                INSERT INTO FilePurposes (FilePurposeId, IsSystemGenerated, PurposeName, UpdatedBy)
                VALUES ('a4be1c12-5c39-497d-a4a2-42d3cc4ac851', 1, 'Contract Pricing Rules', 'Reference Data 1.0');

                IF NOT EXISTS (SELECT 1 FROM FilePurposes WHERE PurposeName = 'Originating Contract')
                INSERT INTO FilePurposes (FilePurposeId, IsSystemGenerated, PurposeName, UpdatedBy)
                VALUES ('d2f9c6e4-9a1b-4f4f-9b6d-8e1b27ef7f41', 0, 'Originating Contract', 'Reference Data 1.0');
            ");

        migrationBuilder.CreateIndex(
            name: "IX_ProcessLogMessages_FileProcessLogId",
            table: "ProcessLogMessages",
            column: "FileProcessLogId");

        migrationBuilder.CreateIndex(
            name: "IX_FileProcessLogs_ProcessLogId_FileName",
            table: "FileProcessLogs",
            columns: new[] { "ProcessLogId", "FileName" },
            unique: true);

        migrationBuilder.CreateIndex(
            name: "IX_FileProcessLogs_ProcessStatus",
            table: "FileProcessLogs",
            column: "ProcessStatus");

        migrationBuilder.CreateIndex(
            name: "IX_FileProcessLogs_PurposeName",
            table: "FileProcessLogs",
            column: "PurposeName");

        migrationBuilder.AddForeignKey(
            name: "FK_FileProcessLogs_FilePurposes_PurposeName",
            table: "FileProcessLogs",
            column: "PurposeName",
            principalTable: "FilePurposes",
            principalColumn: "PurposeName",
            onDelete: ReferentialAction.Restrict);

        migrationBuilder.AddForeignKey(
            name: "FK_FileProcessLogs_ProcessStatuses_ProcessStatus",
            table: "FileProcessLogs",
            column: "ProcessStatus",
            principalTable: "ProcessStatuses",
            principalColumn: "ProcessStatus",
            onDelete: ReferentialAction.Restrict);

        migrationBuilder.AddForeignKey(
            name: "FK_ProcessLogMessages_FileProcessLogs_FileProcessLogId",
            table: "ProcessLogMessages",
            column: "FileProcessLogId",
            principalTable: "FileProcessLogs",
            principalColumn: "FileProcessLogId",
            onDelete: ReferentialAction.Restrict);

    }

    /// <inheritdoc />
    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropForeignKey(
            name: "FK_FileProcessLogs_FilePurposes_PurposeName",
            table: "FileProcessLogs");

        migrationBuilder.DropForeignKey(
            name: "FK_FileProcessLogs_ProcessStatuses_ProcessStatus",
            table: "FileProcessLogs");

        migrationBuilder.DropForeignKey(
            name: "FK_ProcessLogMessages_FileProcessLogs_FileProcessLogId",
            table: "ProcessLogMessages");

        migrationBuilder.DropTable(
            name: "FilePurposeTranslations");

        migrationBuilder.DropTable(
            name: "FilePurposes");

        migrationBuilder.DropIndex(
            name: "IX_ProcessLogMessages_FileProcessLogId",
            table: "ProcessLogMessages");

        migrationBuilder.DropIndex(
            name: "IX_FileProcessLogs_ProcessLogId_FileName",
            table: "FileProcessLogs");

        migrationBuilder.DropIndex(
            name: "IX_FileProcessLogs_ProcessStatus",
            table: "FileProcessLogs");

        migrationBuilder.DropIndex(
            name: "IX_FileProcessLogs_PurposeName",
            table: "FileProcessLogs");

        migrationBuilder.DropColumn(
            name: "FileProcessLogId",
            table: "ProcessLogMessages")
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogMessagesHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.DropColumn(
            name: "ProcessStatus",
            table: "FileProcessLogs")
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "FileProcessLogsHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.DropColumn(
            name: "PurposeName",
            table: "FileProcessLogs")
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "FileProcessLogsHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.CreateIndex(
            name: "IX_FileProcessLogs_ProcessLogId",
            table: "FileProcessLogs",
            column: "ProcessLogId");
    }
}
