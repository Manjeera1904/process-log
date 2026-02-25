using Microsoft.EntityFrameworkCore.Migrations;
using System;

#nullable disable

namespace EI.API.ProcessLogging.Data.Migrations;

/// <inheritdoc />
public partial class AddIsDownloadableToFilePurpose : Migration
{
    /// <inheritdoc />
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.AddColumn<bool>(
            name: "IsDownloadable",
            table: "FilePurposes",
            type: "bit",
            nullable: false,
            defaultValue: false);

        migrationBuilder.UpdateData(
            table: "FilePurposes",
            keyColumn: "FilePurposeId",
            keyValue: new Guid("a4be1c12-5c39-497d-a4a2-42d3cc4ac851"),
            column: "IsDownloadable",
            value: true);

        migrationBuilder.UpdateData(
            table: "FilePurposes",
            keyColumn: "FilePurposeId",
            keyValue: new Guid("b54e58a5-6076-4333-8c8c-76c32992ae39"),
            column: "IsDownloadable",
            value: false);

        migrationBuilder.UpdateData(
            table: "FilePurposes",
            keyColumn: "FilePurposeId",
            keyValue: new Guid("d2f9c6e4-9a1b-4f4f-9b6d-8e1b27ef7f41"),
            column: "IsDownloadable",
            value: false);

        migrationBuilder.InsertData(
            table: "FilePurposes",
            columns: new[] { "FilePurposeId", "IsDownloadable", "IsSystemGenerated", "PurposeName", "UpdatedBy" },
            values: new object[] { new Guid("3f324e2a-42df-4017-9664-39ca2c2c50c4"), true, true, "Contract Pricing Rules Excel", "Reference Data 1.0" });
    }

    /// <inheritdoc />
    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DeleteData(
            table: "FilePurposes",
            keyColumn: "FilePurposeId",
            keyValue: new Guid("3f324e2a-42df-4017-9664-39ca2c2c50c4"));

        migrationBuilder.DropColumn(
            name: "IsDownloadable",
            table: "FilePurposes");
    }
}
