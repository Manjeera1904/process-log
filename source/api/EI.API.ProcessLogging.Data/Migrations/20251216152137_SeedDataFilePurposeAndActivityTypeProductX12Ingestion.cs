using Microsoft.EntityFrameworkCore.Migrations;
using System;

#nullable disable

namespace EI.API.ProcessLogging.Data.Migrations;

/// <inheritdoc />
public partial class SeedDataFilePurposeAndActivityTypeProductX12Ingestion : Migration
{
    /// <inheritdoc />
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.InsertData(
            table: "ActivityTypes",
            columns: new[] { "ActivityTypeId", "Inbound", "Outbound", "ActivityType", "UpdatedBy" },
            values: new object[] { new Guid("945047df-c585-45ff-b07f-f629174b8c61"), true, false, "X12Ingestion", "Reference Data 1.0" });

        migrationBuilder.InsertData(
            table: "FilePurposes",
            columns: new[] { "FilePurposeId", "IsSystemGenerated", "PurposeName", "UpdatedBy" },
            values: new object[] { new Guid("b54e58a5-6076-4333-8c8c-76c32992ae39"), false, "Originating x12 transactions", "Reference Data 1.0" });

        migrationBuilder.InsertData(
            table: "ActivityTypeTranslations",
            columns: new[] { "CultureCode", "ActivityTypeId", "Description", "Name", "UpdatedBy" },
            values: new object[] { "en-US", new Guid("945047df-c585-45ff-b07f-f629174b8c61"), "X12 Ingestion from external system", "X12 Ingestion", "Reference Data 1.0" });
    }

    /// <inheritdoc />
    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DeleteData(
            table: "ActivityTypeTranslations",
            keyColumns: new[] { "CultureCode", "ActivityTypeId" },
            keyValues: new object[] { "en-US", new Guid("945047df-c585-45ff-b07f-f629174b8c61") });

        migrationBuilder.DeleteData(
            table: "FilePurposes",
            keyColumn: "FilePurposeId",
            keyValue: new Guid("b54e58a5-6076-4333-8c8c-76c32992ae39"));

        migrationBuilder.DeleteData(
            table: "ActivityTypes",
            keyColumn: "ActivityTypeId",
            keyValue: new Guid("945047df-c585-45ff-b07f-f629174b8c61"));
    }
}
