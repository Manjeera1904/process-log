using EI.API.ProcessLogging.Data.Entities;
using EI.API.Service.Rest.Helpers.Model.Mapper;

namespace EI.API.ProcessLogging.Model.Mapper;

public class ProcessLogDtoAutomapperProfile : BaseDtoAutomapperProfile
{
    public ProcessLogDtoAutomapperProfile()
    {
        CreateEntityMap<FileProcessLogV1, FileProcessLog>();
        CreateMap<FileProcessLog, FileProcessLogV1>();
        CreateEntityMap<FileProcessLogV2, FileProcessLog>();
        CreateMap<FileProcessLog, FileProcessLogV2>()
            .ForMember(d => d.PurposeName, opt => opt.MapFrom(s => s.PurposeName))
            .ForMember(d => d.ProcessStatus, opt => opt.MapFrom(s => s.ProcessStatus));
        CreateMap<FileProcessLogV1, FileProcessLogV2>();

        CreateEntityMap<ProcessLogMessageV1, ProcessLogMessage>();
        CreateEntityMap<ProcessLogMessageV2, ProcessLogMessage>();
        CreateMap<ProcessLogMessage, ProcessLogMessageV2>()
            .ForMember(d => d.FileProcessLogId, opt => opt.MapFrom(s => s.FileProcessLogId));
        CreateMap<ProcessLogMessageV1, ProcessLogMessageV2>();
        CreateEntityMap<ProcessLogV1, ProcessLog>();
        CreateMap<ProcessLog, ProcessLogWithFilesV1>()
            .ForMember(dest => dest.Files, opt => opt.MapFrom(src => src.FileProcessLogs))
            .ForMember(dest => dest.FileCount,
                opt => opt.MapFrom(src => src.FileProcessLogs != null ? src.FileProcessLogs.Count : 0));
        CreateEntityMap<X12FunctionalGroupV1, X12FunctionalGroup>();
        CreateEntityMap<X12InterchangeV1, X12Interchange>();
        CreateEntityMap<X12MessageV1, X12Message>();
        CreateEntityMap<X12TransactionSetV1, X12TransactionSet>();

        // Entities with translations:
        CreateEntityMap<ActivityTypeV1, ActivityType, ActivityTypeTranslation>();
        CreateEntityMap<MessageLevelV1, MessageLevel, MessageLevelTranslation>();
        CreateEntityMap<ProcessStatusV1, ProcessStatus, ProcessStatusTranslation>();
        CreateEntityMap<X12StatusV1, X12Status, X12StatusTranslation>();
    }
}
