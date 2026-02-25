namespace EI.API.ProcessLogging.Data.App;

public static class PermissionsId
{
    /// <summary>
    /// A user with this permission can view Activity Types
    /// </summary>
    public static Guid ViewActivityTypes = Guid.Parse(Permissions.ViewActivityTypes);

    /// <summary>
    /// A user with this permission can view File Process Logs
    /// </summary>
    public static Guid ViewFileProcessLogs = Guid.Parse(Permissions.ViewFileProcessLogs);

    /// <summary>
    /// A user with this permission can edit File Process Logs
    /// </summary>
    public static Guid EditFileProcessLogs = Guid.Parse(Permissions.EditFileProcessLogs);

    /// <summary>
    /// A user with this permission can view Message Levels
    /// </summary>
    public static Guid ViewMessageLevels = Guid.Parse(Permissions.ViewMessageLevels);

    /// <summary>
    /// A user with this permission can view Process Log Messages
    /// </summary>
    public static Guid ViewProcessLogMessages = Guid.Parse(Permissions.ViewProcessLogMessages);

    /// <summary>
    /// A user with this permission can view Process Logs
    /// </summary>
    public static Guid ViewProcessLogs = Guid.Parse(Permissions.ViewProcessLogs);

    /// <summary>
    /// A user with this permission can edit Process Logs
    /// </summary>
    public static Guid EditProcessLogs = Guid.Parse(Permissions.EditProcessLogs);

    /// <summary>
    /// A user with this permission can view Process Statuses
    /// </summary>
    public static Guid ViewProcessStatuses = Guid.Parse(Permissions.ViewProcessStatuses);

    /// <summary>
    /// A user with this permission can view X12 Functional Groups
    /// </summary>
    public static Guid ViewX12FunctionalGroups = Guid.Parse(Permissions.ViewX12FunctionalGroups);

    /// <summary>
    /// A user with this permission can edit X12 Functional Groups
    /// </summary>
    public static Guid EditX12FunctionalGroups = Guid.Parse(Permissions.EditX12FunctionalGroups);

    /// <summary>
    /// A user with this permission can view X12 Interchanges
    /// </summary>
    public static Guid ViewX12Interchanges = Guid.Parse(Permissions.ViewX12Interchanges);

    /// <summary>
    /// A user with this permission can edit X12 Interchanges
    /// </summary>
    public static Guid EditX12Interchanges = Guid.Parse(Permissions.EditX12Interchanges);

    /// <summary>
    /// A user with this permission can view X12 Status Translation
    /// </summary>
    public static Guid ViewX12StatusTranslation = Guid.Parse(Permissions.ViewX12StatusTranslation);

    /// <summary>
    /// A user with this permission can edit X12 Status Translation
    /// </summary>
    public static Guid EditX12StatusTranslation = Guid.Parse(Permissions.EditX12StatusTranslation);

    /// <summary>
    /// A user with this permission can view X12 Statuses
    /// </summary>
    public static Guid ViewX12Statuses = Guid.Parse(Permissions.ViewX12Statuses);

    /// <summary>
    /// A user with this permission can view X12 Transaction Sets
    /// </summary>
    public static Guid ViewX12TransactionSets = Guid.Parse(Permissions.ViewX12TransactionSets);

    /// <summary>
    /// A user with this permission can edit X12 Transaction Sets
    /// </summary>
    public static Guid EditX12TransactionSets = Guid.Parse(Permissions.EditX12TransactionSets);
}
