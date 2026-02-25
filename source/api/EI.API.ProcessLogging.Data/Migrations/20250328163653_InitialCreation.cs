using Microsoft.EntityFrameworkCore.Migrations;
using System;

#nullable disable

#pragma warning disable CA1814 // Prefer jagged arrays over multidimensional

namespace EI.API.ProcessLogging.Data.Migrations;

/// <inheritdoc />
public partial class InitialCreation : Migration
{
    /// <inheritdoc />
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.CreateTable(
            name: "ActivityTypes",
            columns: table => new
            {
                ActivityTypeId = table.Column<Guid>(type: "uniqueidentifier", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ActivityTypesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ActivityType = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ActivityTypesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                Inbound = table.Column<bool>(type: "bit", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ActivityTypesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                Outbound = table.Column<bool>(type: "bit", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ActivityTypesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidFrom = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ActivityTypesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidTo = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ActivityTypesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                UpdatedBy = table.Column<string>(type: "nvarchar(120)", maxLength: 120, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ActivityTypesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                RowVersion = table.Column<byte[]>(type: "rowversion", rowVersion: true, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ActivityTypesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom")
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_ActivityTypes", x => x.ActivityTypeId);
                table.UniqueConstraint("AK_ActivityTypes_ActivityType", x => x.ActivityType);
            })
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "ActivityTypesHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.CreateTable(
            name: "MessageLevels",
            columns: table => new
            {
                MessageLevelId = table.Column<Guid>(type: "uniqueidentifier", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "MessageLevelsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                MessageLevel = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "MessageLevelsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidFrom = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "MessageLevelsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidTo = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "MessageLevelsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                UpdatedBy = table.Column<string>(type: "nvarchar(120)", maxLength: 120, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "MessageLevelsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                RowVersion = table.Column<byte[]>(type: "rowversion", rowVersion: true, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "MessageLevelsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom")
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_MessageLevels", x => x.MessageLevelId);
                table.UniqueConstraint("AK_MessageLevels_MessageLevel", x => x.MessageLevel);
            })
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "MessageLevelsHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.CreateTable(
            name: "ProcessStatuses",
            columns: table => new
            {
                ProcessStatusId = table.Column<Guid>(type: "uniqueidentifier", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessStatusesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ProcessStatus = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessStatusesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidFrom = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessStatusesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidTo = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessStatusesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                UpdatedBy = table.Column<string>(type: "nvarchar(120)", maxLength: 120, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessStatusesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                RowVersion = table.Column<byte[]>(type: "rowversion", rowVersion: true, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessStatusesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom")
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_ProcessStatuses", x => x.ProcessStatusId);
                table.UniqueConstraint("AK_ProcessStatuses_ProcessStatus", x => x.ProcessStatus);
            })
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "ProcessStatusesHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.CreateTable(
            name: "X12Statuses",
            columns: table => new
            {
                X12StatusId = table.Column<Guid>(type: "uniqueidentifier", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12StatusesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                X12Status = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12StatusesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidFrom = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12StatusesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidTo = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12StatusesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                UpdatedBy = table.Column<string>(type: "nvarchar(120)", maxLength: 120, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12StatusesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                RowVersion = table.Column<byte[]>(type: "rowversion", rowVersion: true, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12StatusesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom")
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_X12Statuses", x => x.X12StatusId);
                table.UniqueConstraint("AK_X12Statuses_X12Status", x => x.X12Status);
            })
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "X12StatusesHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.CreateTable(
            name: "ActivityTypeTranslations",
            columns: table => new
            {
                ActivityTypeId = table.Column<Guid>(type: "uniqueidentifier", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ActivityTypeTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                CultureCode = table.Column<string>(type: "nvarchar(20)", maxLength: 20, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ActivityTypeTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                Name = table.Column<string>(type: "nvarchar(250)", maxLength: 250, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ActivityTypeTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                Description = table.Column<string>(type: "nvarchar(max)", maxLength: 8192, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ActivityTypeTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidFrom = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ActivityTypeTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidTo = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ActivityTypeTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                UpdatedBy = table.Column<string>(type: "nvarchar(120)", maxLength: 120, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ActivityTypeTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                RowVersion = table.Column<byte[]>(type: "rowversion", rowVersion: true, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ActivityTypeTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom")
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_ActivityTypeTranslations", x => new { x.ActivityTypeId, x.CultureCode });
                table.ForeignKey(
                    name: "FK_ActivityTypeTranslations_ActivityTypes_ActivityTypeId",
                    column: x => x.ActivityTypeId,
                    principalTable: "ActivityTypes",
                    principalColumn: "ActivityTypeId",
                    onDelete: ReferentialAction.Restrict);
            })
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "ActivityTypeTranslationsHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.CreateTable(
            name: "MessageLevelTranslations",
            columns: table => new
            {
                MessageLevelId = table.Column<Guid>(type: "uniqueidentifier", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "MessageLevelTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                CultureCode = table.Column<string>(type: "nvarchar(20)", maxLength: 20, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "MessageLevelTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                Name = table.Column<string>(type: "nvarchar(250)", maxLength: 250, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "MessageLevelTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                Description = table.Column<string>(type: "nvarchar(max)", maxLength: 8192, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "MessageLevelTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidFrom = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "MessageLevelTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidTo = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "MessageLevelTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                UpdatedBy = table.Column<string>(type: "nvarchar(120)", maxLength: 120, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "MessageLevelTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                RowVersion = table.Column<byte[]>(type: "rowversion", rowVersion: true, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "MessageLevelTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom")
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_MessageLevelTranslations", x => new { x.MessageLevelId, x.CultureCode });
                table.ForeignKey(
                    name: "FK_MessageLevelTranslations_MessageLevels_MessageLevelId",
                    column: x => x.MessageLevelId,
                    principalTable: "MessageLevels",
                    principalColumn: "MessageLevelId",
                    onDelete: ReferentialAction.Restrict);
            })
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "MessageLevelTranslationsHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.CreateTable(
            name: "ProcessLogs",
            columns: table => new
            {
                ProcessLogId = table.Column<Guid>(type: "uniqueidentifier", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ActivityType = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ProcessStatus = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                StartTimestamp = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                LastUpdatedTimestamp = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidFrom = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidTo = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                UpdatedBy = table.Column<string>(type: "nvarchar(120)", maxLength: 120, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                RowVersion = table.Column<byte[]>(type: "rowversion", rowVersion: true, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom")
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_ProcessLogs", x => x.ProcessLogId);
                table.ForeignKey(
                    name: "FK_ProcessLogs_ActivityTypes_ActivityType",
                    column: x => x.ActivityType,
                    principalTable: "ActivityTypes",
                    principalColumn: "ActivityType",
                    onDelete: ReferentialAction.Restrict);
                table.ForeignKey(
                    name: "FK_ProcessLogs_ProcessStatuses_ProcessStatus",
                    column: x => x.ProcessStatus,
                    principalTable: "ProcessStatuses",
                    principalColumn: "ProcessStatus",
                    onDelete: ReferentialAction.Restrict);
            })
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogsHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.CreateTable(
            name: "ProcessStatusTranslations",
            columns: table => new
            {
                ProcessStatusId = table.Column<Guid>(type: "uniqueidentifier", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessStatusTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                CultureCode = table.Column<string>(type: "nvarchar(20)", maxLength: 20, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessStatusTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                Name = table.Column<string>(type: "nvarchar(250)", maxLength: 250, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessStatusTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                Description = table.Column<string>(type: "nvarchar(max)", maxLength: 8192, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessStatusTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidFrom = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessStatusTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidTo = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessStatusTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                UpdatedBy = table.Column<string>(type: "nvarchar(120)", maxLength: 120, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessStatusTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                RowVersion = table.Column<byte[]>(type: "rowversion", rowVersion: true, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessStatusTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom")
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_ProcessStatusTranslations", x => new { x.ProcessStatusId, x.CultureCode });
                table.ForeignKey(
                    name: "FK_ProcessStatusTranslations_ProcessStatuses_ProcessStatusId",
                    column: x => x.ProcessStatusId,
                    principalTable: "ProcessStatuses",
                    principalColumn: "ProcessStatusId",
                    onDelete: ReferentialAction.Restrict);
            })
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "ProcessStatusTranslationsHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.CreateTable(
            name: "X12StatusTranslations",
            columns: table => new
            {
                X12StatusId = table.Column<Guid>(type: "uniqueidentifier", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12StatusTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                CultureCode = table.Column<string>(type: "nvarchar(20)", maxLength: 20, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12StatusTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                Name = table.Column<string>(type: "nvarchar(250)", maxLength: 250, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12StatusTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                Description = table.Column<string>(type: "nvarchar(max)", maxLength: 8192, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12StatusTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidFrom = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12StatusTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidTo = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12StatusTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                UpdatedBy = table.Column<string>(type: "nvarchar(120)", maxLength: 120, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12StatusTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                RowVersion = table.Column<byte[]>(type: "rowversion", rowVersion: true, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12StatusTranslationsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom")
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_X12StatusTranslations", x => new { x.X12StatusId, x.CultureCode });
                table.ForeignKey(
                    name: "FK_X12StatusTranslations_X12Statuses_X12StatusId",
                    column: x => x.X12StatusId,
                    principalTable: "X12Statuses",
                    principalColumn: "X12StatusId",
                    onDelete: ReferentialAction.Restrict);
            })
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "X12StatusTranslationsHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.CreateTable(
            name: "FileProcessLogs",
            columns: table => new
            {
                FileProcessLogId = table.Column<Guid>(type: "uniqueidentifier", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "FileProcessLogsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ProcessLogId = table.Column<Guid>(type: "uniqueidentifier", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "FileProcessLogsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                FileName = table.Column<string>(type: "nvarchar(1000)", maxLength: 1000, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "FileProcessLogsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                FilePath = table.Column<string>(type: "nvarchar(1000)", maxLength: 1000, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "FileProcessLogsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                FileSize = table.Column<int>(type: "int", nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "FileProcessLogsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                FileHash = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "FileProcessLogsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidFrom = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "FileProcessLogsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidTo = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "FileProcessLogsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                UpdatedBy = table.Column<string>(type: "nvarchar(120)", maxLength: 120, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "FileProcessLogsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                RowVersion = table.Column<byte[]>(type: "rowversion", rowVersion: true, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "FileProcessLogsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom")
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_FileProcessLogs", x => x.FileProcessLogId);
                table.ForeignKey(
                    name: "FK_FileProcessLogs_ProcessLogs_ProcessLogId",
                    column: x => x.ProcessLogId,
                    principalTable: "ProcessLogs",
                    principalColumn: "ProcessLogId",
                    onDelete: ReferentialAction.Restrict);
            })
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "FileProcessLogsHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.CreateTable(
            name: "ProcessLogMessages",
            columns: table => new
            {
                ProcessLogMessageId = table.Column<Guid>(type: "uniqueidentifier", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogMessagesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ProcessLogId = table.Column<Guid>(type: "uniqueidentifier", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogMessagesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                MessageLevel = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogMessagesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                Message = table.Column<string>(type: "nvarchar(max)", maxLength: 8192, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogMessagesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                MessageTimestamp = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogMessagesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidFrom = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogMessagesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidTo = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogMessagesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                UpdatedBy = table.Column<string>(type: "nvarchar(120)", maxLength: 120, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogMessagesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                RowVersion = table.Column<byte[]>(type: "rowversion", rowVersion: true, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogMessagesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom")
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_ProcessLogMessages", x => x.ProcessLogMessageId);
                table.ForeignKey(
                    name: "FK_ProcessLogMessages_MessageLevels_MessageLevel",
                    column: x => x.MessageLevel,
                    principalTable: "MessageLevels",
                    principalColumn: "MessageLevel",
                    onDelete: ReferentialAction.Restrict);
                table.ForeignKey(
                    name: "FK_ProcessLogMessages_ProcessLogs_ProcessLogId",
                    column: x => x.ProcessLogId,
                    principalTable: "ProcessLogs",
                    principalColumn: "ProcessLogId",
                    onDelete: ReferentialAction.Restrict);
            })
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogMessagesHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.CreateTable(
            name: "X12Interchanges",
            columns: table => new
            {
                X12InterchangeId = table.Column<Guid>(type: "uniqueidentifier", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12InterchangesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                FileProcessLogId = table.Column<Guid>(type: "uniqueidentifier", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12InterchangesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                X12Status = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12InterchangesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                InterchangeSenderIdQualifier = table.Column<string>(type: "nvarchar(10)", maxLength: 10, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12InterchangesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                InterchangeSenderId = table.Column<string>(type: "nvarchar(15)", maxLength: 15, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12InterchangesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                InterchangeReceiverIdQualifier = table.Column<string>(type: "nvarchar(10)", maxLength: 10, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12InterchangesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                InterchangeReceiverId = table.Column<string>(type: "nvarchar(15)", maxLength: 15, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12InterchangesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                InterchangeDate = table.Column<string>(type: "nvarchar(6)", maxLength: 6, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12InterchangesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                InterchangeTime = table.Column<string>(type: "nvarchar(4)", maxLength: 4, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12InterchangesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                RepetitionSeparator = table.Column<string>(type: "nvarchar(4)", maxLength: 4, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12InterchangesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                InterchangeControlVersionNumber = table.Column<string>(type: "nvarchar(5)", maxLength: 5, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12InterchangesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                InterchangeControlNumber = table.Column<string>(type: "nvarchar(9)", maxLength: 9, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12InterchangesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                AcknowledgementRequested = table.Column<string>(type: "nvarchar(1)", maxLength: 1, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12InterchangesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                UsageIndicator = table.Column<string>(type: "nvarchar(1)", maxLength: 1, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12InterchangesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ComponentElementSeparator = table.Column<string>(type: "nvarchar(1)", maxLength: 1, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12InterchangesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidFrom = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12InterchangesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidTo = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12InterchangesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                UpdatedBy = table.Column<string>(type: "nvarchar(120)", maxLength: 120, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12InterchangesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                RowVersion = table.Column<byte[]>(type: "rowversion", rowVersion: true, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12InterchangesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom")
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_X12Interchanges", x => x.X12InterchangeId);
                table.ForeignKey(
                    name: "FK_X12Interchanges_FileProcessLogs_FileProcessLogId",
                    column: x => x.FileProcessLogId,
                    principalTable: "FileProcessLogs",
                    principalColumn: "FileProcessLogId",
                    onDelete: ReferentialAction.Restrict);
                table.ForeignKey(
                    name: "FK_X12Interchanges_X12Statuses_X12Status",
                    column: x => x.X12Status,
                    principalTable: "X12Statuses",
                    principalColumn: "X12Status",
                    onDelete: ReferentialAction.Restrict);
            })
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "X12InterchangesHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.CreateTable(
            name: "X12FunctionalGroups",
            columns: table => new
            {
                X12FunctionalGroupId = table.Column<Guid>(type: "uniqueidentifier", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12FunctionalGroupsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                X12InterchangeId = table.Column<Guid>(type: "uniqueidentifier", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12FunctionalGroupsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                X12Status = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12FunctionalGroupsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                FunctionalIdentifierCode = table.Column<string>(type: "nvarchar(2)", maxLength: 2, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12FunctionalGroupsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ApplicationSenderCode = table.Column<string>(type: "nvarchar(15)", maxLength: 15, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12FunctionalGroupsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ApplicationReceiverCode = table.Column<string>(type: "nvarchar(15)", maxLength: 15, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12FunctionalGroupsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                Date = table.Column<string>(type: "nvarchar(8)", maxLength: 8, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12FunctionalGroupsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                Time = table.Column<string>(type: "nvarchar(8)", maxLength: 8, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12FunctionalGroupsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                GroupControlNumber = table.Column<string>(type: "nvarchar(9)", maxLength: 9, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12FunctionalGroupsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ResponsibleAgencyCode = table.Column<string>(type: "nvarchar(2)", maxLength: 2, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12FunctionalGroupsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                VersionReleaseIndustryIdentifierCode = table.Column<string>(type: "nvarchar(12)", maxLength: 12, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12FunctionalGroupsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidFrom = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12FunctionalGroupsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidTo = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12FunctionalGroupsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                UpdatedBy = table.Column<string>(type: "nvarchar(120)", maxLength: 120, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12FunctionalGroupsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                RowVersion = table.Column<byte[]>(type: "rowversion", rowVersion: true, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12FunctionalGroupsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom")
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_X12FunctionalGroups", x => x.X12FunctionalGroupId);
                table.ForeignKey(
                    name: "FK_X12FunctionalGroups_X12Interchanges_X12InterchangeId",
                    column: x => x.X12InterchangeId,
                    principalTable: "X12Interchanges",
                    principalColumn: "X12InterchangeId",
                    onDelete: ReferentialAction.Restrict);
                table.ForeignKey(
                    name: "FK_X12FunctionalGroups_X12Statuses_X12Status",
                    column: x => x.X12Status,
                    principalTable: "X12Statuses",
                    principalColumn: "X12Status",
                    onDelete: ReferentialAction.Restrict);
            })
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "X12FunctionalGroupsHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.CreateTable(
            name: "X12TransactionSets",
            columns: table => new
            {
                X12TransactionSetId = table.Column<Guid>(type: "uniqueidentifier", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12TransactionSetsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                X12FunctionalGroupId = table.Column<Guid>(type: "uniqueidentifier", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12TransactionSetsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                X12Status = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12TransactionSetsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                TransactionSetIdentifierCode = table.Column<string>(type: "nvarchar(3)", maxLength: 3, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12TransactionSetsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                TransactionSetControlNumber = table.Column<string>(type: "nvarchar(9)", maxLength: 9, nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12TransactionSetsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidFrom = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12TransactionSetsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidTo = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12TransactionSetsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                UpdatedBy = table.Column<string>(type: "nvarchar(120)", maxLength: 120, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12TransactionSetsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                RowVersion = table.Column<byte[]>(type: "rowversion", rowVersion: true, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12TransactionSetsHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom")
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_X12TransactionSets", x => x.X12TransactionSetId);
                table.ForeignKey(
                    name: "FK_X12TransactionSets_X12FunctionalGroups_X12FunctionalGroupId",
                    column: x => x.X12FunctionalGroupId,
                    principalTable: "X12FunctionalGroups",
                    principalColumn: "X12FunctionalGroupId",
                    onDelete: ReferentialAction.Restrict);
                table.ForeignKey(
                    name: "FK_X12TransactionSets_X12Statuses_X12Status",
                    column: x => x.X12Status,
                    principalTable: "X12Statuses",
                    principalColumn: "X12Status",
                    onDelete: ReferentialAction.Restrict);
            })
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "X12TransactionSetsHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.CreateTable(
            name: "X12Messages",
            columns: table => new
            {
                X12MessageId = table.Column<Guid>(type: "uniqueidentifier", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12MessagesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                X12InterchangeId = table.Column<Guid>(type: "uniqueidentifier", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12MessagesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                X12FunctionalGroupId = table.Column<Guid>(type: "uniqueidentifier", nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12MessagesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                X12TransactionSetId = table.Column<Guid>(type: "uniqueidentifier", nullable: true)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12MessagesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                MessageLevel = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12MessagesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                Message = table.Column<string>(type: "nvarchar(max)", maxLength: 8192, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12MessagesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                MessageTimestamp = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12MessagesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidFrom = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12MessagesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                ValidTo = table.Column<DateTime>(type: "datetime2", nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12MessagesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                UpdatedBy = table.Column<string>(type: "nvarchar(120)", maxLength: 120, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12MessagesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom"),
                RowVersion = table.Column<byte[]>(type: "rowversion", rowVersion: true, nullable: false)
                    .Annotation("SqlServer:IsTemporal", true)
                    .Annotation("SqlServer:TemporalHistoryTableName", "X12MessagesHistory")
                    .Annotation("SqlServer:TemporalHistoryTableSchema", null)
                    .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
                    .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom")
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_X12Messages", x => x.X12MessageId);
                table.ForeignKey(
                    name: "FK_X12Messages_MessageLevels_MessageLevel",
                    column: x => x.MessageLevel,
                    principalTable: "MessageLevels",
                    principalColumn: "MessageLevel",
                    onDelete: ReferentialAction.Restrict);
                table.ForeignKey(
                    name: "FK_X12Messages_X12FunctionalGroups_X12FunctionalGroupId",
                    column: x => x.X12FunctionalGroupId,
                    principalTable: "X12FunctionalGroups",
                    principalColumn: "X12FunctionalGroupId",
                    onDelete: ReferentialAction.Restrict);
                table.ForeignKey(
                    name: "FK_X12Messages_X12Interchanges_X12InterchangeId",
                    column: x => x.X12InterchangeId,
                    principalTable: "X12Interchanges",
                    principalColumn: "X12InterchangeId",
                    onDelete: ReferentialAction.Restrict);
                table.ForeignKey(
                    name: "FK_X12Messages_X12TransactionSets_X12TransactionSetId",
                    column: x => x.X12TransactionSetId,
                    principalTable: "X12TransactionSets",
                    principalColumn: "X12TransactionSetId",
                    onDelete: ReferentialAction.Restrict);
            })
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "X12MessagesHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.InsertData(
            table: "ActivityTypes",
            columns: new[] { "ActivityTypeId", "Inbound", "Outbound", "ActivityType", "UpdatedBy" },
            values: new object[] { new Guid("27a1378d-e392-486e-a63f-8c2414e44c1d"), true, false, "ReceiveFile", "Reference Data 1.0" });

        migrationBuilder.InsertData(
            table: "MessageLevels",
            columns: new[] { "MessageLevelId", "MessageLevel", "UpdatedBy" },
            values: new object[,]
            {
                { new Guid("0e8d0b7e-811a-47f3-bb5a-b64eb9fb92c8"), "Information", "Reference Data 1.0" },
                { new Guid("198aa513-a2a2-4781-9e19-d79af8947cdd"), "Status", "Reference Data 1.0" },
                { new Guid("36304564-2b06-401d-b71f-b9062890edb9"), "Warning", "Reference Data 1.0" },
                { new Guid("7252f49d-ca4c-4623-be6d-55c90602c1c1"), "Fatal", "Reference Data 1.0" },
                { new Guid("ee72bde9-e89d-4bc0-b91b-9294f160fbf9"), "Error", "Reference Data 1.0" }
            });

        migrationBuilder.InsertData(
            table: "ProcessStatuses",
            columns: new[] { "ProcessStatusId", "ProcessStatus", "UpdatedBy" },
            values: new object[,]
            {
                { new Guid("4ed43de1-a88d-4e53-8370-51738497c0da"), "New", "Reference Data 1.0" },
                { new Guid("6dfe6ee6-36d8-428f-97b2-571def4a6fb4"), "InProgress", "Reference Data 1.0" },
                { new Guid("8ed812bd-1761-4d34-ad12-f4d9515ff43e"), "Paused", "Reference Data 1.0" },
                { new Guid("c59f50b2-d7c2-4a6f-897c-5b9ec0d3d539"), "Failed", "Reference Data 1.0" },
                { new Guid("d40d80f7-eb09-4f95-86fa-79ff569e7907"), "Cancelled", "Reference Data 1.0" },
                { new Guid("d7c7ae65-285e-47a4-b421-5bdc9b39aec2"), "Duplicate", "Reference Data 1.0" },
                { new Guid("efd534e1-db63-4b03-a36e-523fa9c14963"), "Completed", "Reference Data 1.0" }
            });

        migrationBuilder.InsertData(
            table: "X12Statuses",
            columns: new[] { "X12StatusId", "X12Status", "UpdatedBy" },
            values: new object[,]
            {
                { new Guid("21c50e68-788d-41c5-a4f1-05d1e9aa00f8"), "Accepted", "Reference Data 1.0" },
                { new Guid("65a9f7ab-757f-4fc8-bbce-571039900b9e"), "Duplicate", "Reference Data 1.0" },
                { new Guid("cf1e5c7f-c9b7-443f-b7fb-bdac96c9fc60"), "Rejected", "Reference Data 1.0" },
                { new Guid("e119c843-1c46-4571-b379-eee66f6b7e7b"), "Invalid", "Reference Data 1.0" }
            });

        migrationBuilder.InsertData(
            table: "ActivityTypeTranslations",
            columns: new[] { "CultureCode", "ActivityTypeId", "Description", "Name", "UpdatedBy" },
            values: new object[] { "en-US", new Guid("27a1378d-e392-486e-a63f-8c2414e44c1d"), "File received from external system", "Receive File", "Reference Data 1.0" });

        migrationBuilder.InsertData(
            table: "MessageLevelTranslations",
            columns: new[] { "CultureCode", "MessageLevelId", "Description", "Name", "UpdatedBy" },
            values: new object[,]
            {
                { "en-US", new Guid("0e8d0b7e-811a-47f3-bb5a-b64eb9fb92c8"), "Message is a routine status message", "Informational", "Reference Data 1.0" },
                { "en-US", new Guid("198aa513-a2a2-4781-9e19-d79af8947cdd"), "Record of the Event Log entry's status changing", "Status Change", "Reference Data 1.0" },
                { "en-US", new Guid("36304564-2b06-401d-b71f-b9062890edb9"), "A message describing a potentially problematic issue while processing the Event", "Warning", "Reference Data 1.0" },
                { "en-US", new Guid("7252f49d-ca4c-4623-be6d-55c90602c1c1"), "A message describing a severe error that halted processing of the Event", "Fatal", "Reference Data 1.0" },
                { "en-US", new Guid("ee72bde9-e89d-4bc0-b91b-9294f160fbf9"), "A message describing an error that occurred while processing the Event", "Error", "Reference Data 1.0" }
            });

        migrationBuilder.InsertData(
            table: "ProcessStatusTranslations",
            columns: new[] { "CultureCode", "ProcessStatusId", "Description", "Name", "UpdatedBy" },
            values: new object[,]
            {
                { "en-US", new Guid("4ed43de1-a88d-4e53-8370-51738497c0da"), "Event has been received but not yet started", "New", "Reference Data 1.0" },
                { "en-US", new Guid("6dfe6ee6-36d8-428f-97b2-571def4a6fb4"), "Event is currently in-progress", "In-Progress", "Reference Data 1.0" },
                { "en-US", new Guid("8ed812bd-1761-4d34-ad12-f4d9515ff43e"), "Event processing was started, but is currently on hold with no activity occurring", "Paused", "Reference Data 1.0" },
                { "en-US", new Guid("c59f50b2-d7c2-4a6f-897c-5b9ec0d3d539"), "Event processing completed unsuccessfully", "Failed", "Reference Data 1.0" },
                { "en-US", new Guid("d40d80f7-eb09-4f95-86fa-79ff569e7907"), "Event processing was started, but ended without completing", "Cancelled", "Reference Data 1.0" },
                { "en-US", new Guid("d7c7ae65-285e-47a4-b421-5bdc9b39aec2"), "Event processing was halted after being identified as a duplicate of an earlier, un-cancelled process", "Duplicate", "Reference Data 1.0" },
                { "en-US", new Guid("efd534e1-db63-4b03-a36e-523fa9c14963"), "Event processing completed successfully", "Complete", "Reference Data 1.0" }
            });

        migrationBuilder.InsertData(
            table: "X12StatusTranslations",
            columns: new[] { "CultureCode", "X12StatusId", "Description", "Name", "UpdatedBy" },
            values: new object[,]
            {
                { "en-US", new Guid("21c50e68-788d-41c5-a4f1-05d1e9aa00f8"), "The X12 record was validated and accepted", "Accepted", "Reference Data 1.0" },
                { "en-US", new Guid("65a9f7ab-757f-4fc8-bbce-571039900b9e"), "The X12 record was rejected as a duplicate", "Duplicate", "Reference Data 1.0" },
                { "en-US", new Guid("cf1e5c7f-c9b7-443f-b7fb-bdac96c9fc60"), "The X12 record was rejected for reasons other than being Invalid", "Rejected", "Reference Data 1.0" },
                { "en-US", new Guid("e119c843-1c46-4571-b379-eee66f6b7e7b"), "The X12 record was rejected do to validation errors", "Error", "Reference Data 1.0" }
            });

        migrationBuilder.CreateIndex(
            name: "IX_FileProcessLogs_ProcessLogId",
            table: "FileProcessLogs",
            column: "ProcessLogId");

        migrationBuilder.CreateIndex(
            name: "IX_ProcessLogMessages_MessageLevel",
            table: "ProcessLogMessages",
            column: "MessageLevel");

        migrationBuilder.CreateIndex(
            name: "IX_ProcessLogMessages_ProcessLogId",
            table: "ProcessLogMessages",
            column: "ProcessLogId");

        migrationBuilder.CreateIndex(
            name: "IX_ProcessLogs_ActivityType",
            table: "ProcessLogs",
            column: "ActivityType");

        migrationBuilder.CreateIndex(
            name: "IX_ProcessLogs_ProcessStatus",
            table: "ProcessLogs",
            column: "ProcessStatus");

        migrationBuilder.CreateIndex(
            name: "IX_X12FunctionalGroups_X12InterchangeId",
            table: "X12FunctionalGroups",
            column: "X12InterchangeId");

        migrationBuilder.CreateIndex(
            name: "IX_X12FunctionalGroups_X12Status",
            table: "X12FunctionalGroups",
            column: "X12Status");

        migrationBuilder.CreateIndex(
            name: "IX_X12Interchanges_FileProcessLogId",
            table: "X12Interchanges",
            column: "FileProcessLogId");

        migrationBuilder.CreateIndex(
            name: "IX_X12Interchanges_X12Status",
            table: "X12Interchanges",
            column: "X12Status");

        migrationBuilder.CreateIndex(
            name: "IX_X12Messages_MessageLevel",
            table: "X12Messages",
            column: "MessageLevel");

        migrationBuilder.CreateIndex(
            name: "IX_X12Messages_X12FunctionalGroupId",
            table: "X12Messages",
            column: "X12FunctionalGroupId");

        migrationBuilder.CreateIndex(
            name: "IX_X12Messages_X12InterchangeId",
            table: "X12Messages",
            column: "X12InterchangeId");

        migrationBuilder.CreateIndex(
            name: "IX_X12Messages_X12TransactionSetId",
            table: "X12Messages",
            column: "X12TransactionSetId");

        migrationBuilder.CreateIndex(
            name: "IX_X12TransactionSets_X12FunctionalGroupId",
            table: "X12TransactionSets",
            column: "X12FunctionalGroupId");

        migrationBuilder.CreateIndex(
            name: "IX_X12TransactionSets_X12Status",
            table: "X12TransactionSets",
            column: "X12Status");
    }

    /// <inheritdoc />
    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropTable(
            name: "ActivityTypeTranslations")
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "ActivityTypeTranslationsHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.DropTable(
            name: "MessageLevelTranslations")
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "MessageLevelTranslationsHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.DropTable(
            name: "ProcessLogMessages")
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogMessagesHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.DropTable(
            name: "ProcessStatusTranslations")
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "ProcessStatusTranslationsHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.DropTable(
            name: "X12Messages")
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "X12MessagesHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.DropTable(
            name: "X12StatusTranslations")
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "X12StatusTranslationsHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.DropTable(
            name: "MessageLevels")
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "MessageLevelsHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.DropTable(
            name: "X12TransactionSets")
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "X12TransactionSetsHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.DropTable(
            name: "X12FunctionalGroups")
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "X12FunctionalGroupsHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.DropTable(
            name: "X12Interchanges")
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "X12InterchangesHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.DropTable(
            name: "FileProcessLogs")
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "FileProcessLogsHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.DropTable(
            name: "X12Statuses")
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "X12StatusesHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.DropTable(
            name: "ProcessLogs")
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "ProcessLogsHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.DropTable(
            name: "ActivityTypes")
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "ActivityTypesHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");

        migrationBuilder.DropTable(
            name: "ProcessStatuses")
            .Annotation("SqlServer:IsTemporal", true)
            .Annotation("SqlServer:TemporalHistoryTableName", "ProcessStatusesHistory")
            .Annotation("SqlServer:TemporalHistoryTableSchema", null)
            .Annotation("SqlServer:TemporalPeriodEndColumnName", "ValidTo")
            .Annotation("SqlServer:TemporalPeriodStartColumnName", "ValidFrom");
    }
}
