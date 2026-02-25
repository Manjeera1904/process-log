using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace EI.API.ProcessLogging.Data.Migrations;

/// <inheritdoc />
public partial class AddActivityType_PayorContractAnalysis : Migration
{
    /// <inheritdoc />
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.InsertData(
            table: "ActivityTypes",
            columns: new[] { "ActivityTypeId", "Inbound", "Outbound", "ActivityType", "UpdatedBy" },
            values: new object[]
            {
                new Guid("702524f1-6ae1-4989-8480-1a00b0bbc04d"),
                true,
                false,
                "PayorContractAnalysis",
                "Reference Data 1.0",
            }
        );

        migrationBuilder.InsertData(
            table: "ActivityTypeTranslations",
            columns: new[] { "CultureCode", "ActivityTypeId", "Description", "Name", "UpdatedBy" },
            values: new object[]
            {
                "en-US",
                new Guid("702524f1-6ae1-4989-8480-1a00b0bbc04d"),
                "Payor Contract Analysis from external system",
                "Payor Contract Analysis",
                "Reference Data 1.0",
            }
        );
    }

    /// <inheritdoc />
    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DeleteData(
            table: "ActivityTypeTranslations",
            keyColumns: new[] { "CultureCode", "ActivityTypeId" },
            keyValues: new object[] { "en-US", new Guid("702524f1-6ae1-4989-8480-1a00b0bbc04d") }
        );

        migrationBuilder.DeleteData(
            table: "ActivityTypes",
            keyColumn: "ActivityTypeId",
            keyValue: new Guid("702524f1-6ae1-4989-8480-1a00b0bbc04d")
        );
    }
}
