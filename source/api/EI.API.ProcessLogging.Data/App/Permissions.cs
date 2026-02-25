using System.Reflection;

namespace EI.API.ProcessLogging.Data.App;

public static class Permissions
{
    /// <summary>
    /// A user with this permission can view Activity Types
    /// </summary>
    public const string ViewActivityTypes = "B92A14D6-F67B-4352-AAB5-EAD515DB06DA";

    /// <summary>
    /// A user with this permission can view File Process Logs
    /// </summary>
    public const string ViewFileProcessLogs = "CD4F6906-3B70-433A-8AC4-C7817A401E50";

    /// <summary>
    /// A user with this permission can edit File Process Logs
    /// </summary>
    public const string EditFileProcessLogs = "754D002C-E8A7-452B-B591-FAA471C1E89B";

    /// <summary>
    /// A user with this permission can view Message Levels
    /// </summary>
    public const string ViewMessageLevels = "9199A0EE-AB47-40D7-8EF6-763672A46DA9";

    /// <summary>
    /// A user with this permission can view Process Log Messages
    /// </summary>
    public const string ViewProcessLogMessages = "584EBB11-590B-4A84-AD5E-63FF3D21F4A3";

    /// <summary>
    /// A user with this permission can view Process Logs
    /// </summary>
    public const string ViewProcessLogs = "7E6C7E3E-E48E-47FD-8FDF-18849F7A5C4A";

    /// <summary>
    /// A user with this permission can edit Process Logs
    /// </summary>
    public const string EditProcessLogs = "992F3A26-0D9A-4584-ACDB-081BB3C66EBF";

    /// <summary>
    /// A user with this permission can view Process Statuses
    /// </summary>
    public const string ViewProcessStatuses = "007B4F82-6016-4BD2-A3D1-B4DC286131A2";

    /// <summary>
    /// A user with this permission can view X12 Functional Groups
    /// </summary>
    public const string ViewX12FunctionalGroups = "021845B5-3E90-4480-A032-A5132CE97C9B";

    /// <summary>
    /// A user with this permission can edit X12 Functional Groups
    /// </summary>
    public const string EditX12FunctionalGroups = "4121C172-750C-4159-A227-166F078F7A9B";

    /// <summary>
    /// A user with this permission can view X12 Interchanges
    /// </summary>
    public const string ViewX12Interchanges = "EDCE45CE-8ED6-4C30-B644-74F74AD6CCD3";

    /// <summary>
    /// A user with this permission can edit X12 Interchanges
    /// </summary>
    public const string EditX12Interchanges = "1A9CC626-1203-451C-BC31-B81D143DBDED";

    /// <summary>
    /// A user with this permission can view X12 Status Translation
    /// </summary>
    public const string ViewX12StatusTranslation = "78737723-1AAE-401B-96E1-EB262EF228C0";

    /// <summary>
    /// A user with this permission can edit X12 Status Translation
    /// </summary>
    public const string EditX12StatusTranslation = "59084B05-56A8-49CE-AD47-25D5C1A18271";

    /// <summary>
    /// A user with this permission can view X12 Statuses
    /// </summary>
    public const string ViewX12Statuses = "5F2497F9-D3B8-4BD4-B16C-E1CAD79B6F63";

    /// <summary>
    /// A user with this permission can view X12 Transaction Sets
    /// </summary>
    public const string ViewX12TransactionSets = "7AD28BCE-9897-45A6-8F71-2E814BC4AAF4";

    /// <summary>
    /// A user with this permission can edit X12 Transaction Sets
    /// </summary>
    public const string EditX12TransactionSets = "743A5341-AF00-46C7-B432-77750D97BA2E";

    /// <summary>
    /// List of all Permissions
    /// </summary>
    public static string[] AllPermissions =>
        (
            from field in typeof(Permissions).GetFields(BindingFlags.Public | BindingFlags.Static | BindingFlags.FlattenHierarchy)
            where field.IsLiteral && !field.IsInitOnly && field.FieldType == typeof(string)
            let constValue = field.GetRawConstantValue() as string
            where constValue != null
            select constValue
        ).ToArray();
}
