namespace EI.API.ProcessLogging.Data;

public static class ProcessLogConstants
{
    // This should eventually be dynamic, but making it fixed for now
    public static class ActivityType
    {
        public static readonly string ReceiveFile = "ReceiveFile";
        public static readonly string PayorContractAnalysis = "PayorContractAnalysis";
        public static readonly string X12Ingestion = "X12Ingestion";
    }

    public static class ProcessStatus
    {
        public static readonly string New = "New";
        public static readonly string InProgress = "InProgress";
        public static readonly string Paused = "Paused";
        public static readonly string Completed = "Completed";
        public static readonly string Failed = "Failed";
        public static readonly string Cancelled = "Cancelled";
        public static readonly string Duplicate = "Duplicate";
    }

    public static class MessageLevel
    {
        public static readonly string Info = "Information";
        public static readonly string Status = "Status";
        public static readonly string Warn = "Warning";
        public static readonly string Error = "Error";
        public static readonly string Fatal = "Fatal";
    }

    public static class X12Status
    {
        public static readonly string Accepted = "Accepted";
        public static readonly string Rejected = "Rejected";
        public static readonly string Invalid = "Invalid";
        public static readonly string Duplicate = "Duplicate";
    }
}
