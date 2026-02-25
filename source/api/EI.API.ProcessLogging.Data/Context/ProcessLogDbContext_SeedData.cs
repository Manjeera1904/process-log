using EI.API.ProcessLogging.Data.Entities;
using EI.API.Service.Data.Helpers;
using Microsoft.EntityFrameworkCore;

namespace EI.API.ProcessLogging.Data.Context;

public partial class ProcessLogDbContext
{
    partial void OnModelCreatingSeedData(ModelBuilder modelBuilder)
    {
        AddActivityTypes(modelBuilder);
        AddProcessStatuses(modelBuilder);
        AddMessageLevels(modelBuilder);
        AddX12Statuses(modelBuilder);
        AddFilePurposes(modelBuilder);
    }

    private void AddActivityTypes(ModelBuilder modelBuilder)
    {
        var data = new[]
                   {
                       new
                       {
                           Id = Guid.Parse("27A1378D-E392-486E-A63F-8C2414E44C1D"),
                           Type = ProcessLogConstants.ActivityType.ReceiveFile,
                           Name = "Receive File",
                           Description = "File received from external system",
                           Inbound = true,
                           Outbound = false,
                       },
                       new
                        {
                            Id = Guid.Parse("702524f1-6ae1-4989-8480-1a00b0bbc04d"),
                            Type = ProcessLogConstants.ActivityType.PayorContractAnalysis,
                            Name = "Payor Contract Analysis",
                            Description = "Payor Contract Analysis from external system",
                            Inbound = true,
                            Outbound = false,
                        },
                       new
                        {
                            Id = Guid.Parse("945047df-c585-45ff-b07f-f629174b8c61"),
                            Type = ProcessLogConstants.ActivityType.X12Ingestion,
                            Name = "X12 Ingestion",
                            Description = "X12 Ingestion from external system",
                            Inbound = true,
                            Outbound = false,
                        },
                   };

        var models = data.Select(config =>
                                     new
                                     {
                                         Entity = new ActivityType
                                         {
                                             Id = config.Id,
                                             Type = config.Type,
                                             IsInbound = config.Inbound,
                                             IsOutbound = config.Outbound,
                                             UpdatedBy = "Reference Data 1.0",
                                         },
                                         Translation = new ActivityTypeTranslation
                                         {
                                             Id = config.Id,
                                             CultureCode = ServiceConstants.CultureCode.Default,
                                             Name = config.Name,
                                             Description = config.Description,
                                             UpdatedBy = "Reference Data 1.0",
                                         }
                                     }).ToArray();

        modelBuilder.Entity<ActivityType>().HasData(models.Select(m => m.Entity));
        modelBuilder.Entity<ActivityTypeTranslation>().HasData(models.Select(m => m.Translation));
    }

    private void AddProcessStatuses(ModelBuilder modelBuilder)
    {
        var data = new[]
                   {
                       new
                       {
                           Id = Guid.Parse("4ED43DE1-A88D-4E53-8370-51738497C0DA"),
                           Status = ProcessLogConstants.ProcessStatus.New,
                           Name = "New",
                           Description = "Event has been received but not yet started",
                       },
                       new
                       {
                           Id = Guid.Parse("6DFE6EE6-36D8-428F-97B2-571DEF4A6FB4"),
                           Status = ProcessLogConstants.ProcessStatus.InProgress,
                           Name = "In-Progress",
                           Description = "Event is currently in-progress",
                       },
                       new
                       {
                           Id = Guid.Parse("8ED812BD-1761-4D34-AD12-F4D9515FF43E"),
                           Status = ProcessLogConstants.ProcessStatus.Paused,
                           Name = "Paused",
                           Description = "Event processing was started, but is currently on hold with no activity occurring",
                       },
                       new
                       {
                           Id = Guid.Parse("EFD534E1-DB63-4B03-A36E-523FA9C14963"),
                           Status = ProcessLogConstants.ProcessStatus.Completed,
                           Name = "Complete",
                           Description = "Event processing completed successfully",
                       },
                       new
                       {
                           Id = Guid.Parse("C59F50B2-D7C2-4A6F-897C-5B9EC0D3D539"),
                           Status = ProcessLogConstants.ProcessStatus.Failed,
                           Name = "Failed",
                           Description = "Event processing completed unsuccessfully",
                       },
                       new
                       {
                           Id = Guid.Parse("D40D80F7-EB09-4F95-86FA-79FF569E7907"),
                           Status = ProcessLogConstants.ProcessStatus.Cancelled,
                           Name = "Cancelled",
                           Description = "Event processing was started, but ended without completing",
                       },
                       new
                       {
                           Id = Guid.Parse("D7C7AE65-285E-47A4-B421-5BDC9B39AEC2"),
                           Status = ProcessLogConstants.ProcessStatus.Duplicate,
                           Name = "Duplicate",
                           Description = "Event processing was halted after being identified as a duplicate of an earlier, un-cancelled process",
                       },
                   };

        var models = data.Select(config =>
                                     new
                                     {
                                         Entity = new ProcessStatus
                                         {
                                             Id = config.Id,
                                             Status = config.Status,
                                             UpdatedBy = "Reference Data 1.0",
                                         },
                                         Translation = new ProcessStatusTranslation
                                         {
                                             Id = config.Id,
                                             CultureCode = ServiceConstants.CultureCode.Default,
                                             Name = config.Name,
                                             Description = config.Description,
                                             UpdatedBy = "Reference Data 1.0",
                                         }
                                     }).ToArray();

        modelBuilder.Entity<ProcessStatus>().HasData(models.Select(m => m.Entity));
        modelBuilder.Entity<ProcessStatusTranslation>().HasData(models.Select(m => m.Translation));
    }

    private void AddMessageLevels(ModelBuilder modelBuilder)
    {
        var data = new[]
                   {
                       new
                       {
                           Id = Guid.Parse("0E8D0B7E-811A-47F3-BB5A-B64EB9FB92C8"),
                           Level = ProcessLogConstants.MessageLevel.Info,
                           Name = "Informational",
                           Description = "Message is a routine status message",
                       },
                       new
                       {
                           Id = Guid.Parse("198AA513-A2A2-4781-9E19-D79AF8947CDD"),
                           Level = ProcessLogConstants.MessageLevel.Status,
                           Name = "Status Change",
                           Description = "Record of the Event Log entry's status changing",
                       },
                       new
                       {
                           Id = Guid.Parse("36304564-2B06-401D-B71F-B9062890EDB9"),
                           Level = ProcessLogConstants.MessageLevel.Warn,
                           Name = "Warning",
                           Description = "A message describing a potentially problematic issue while processing the Event",
                       },
                       new
                       {
                           Id = Guid.Parse("EE72BDE9-E89D-4BC0-B91B-9294F160FBF9"),
                           Level = ProcessLogConstants.MessageLevel.Error,
                           Name = "Error",
                           Description = "A message describing an error that occurred while processing the Event",
                       },
                       new
                       {
                           Id = Guid.Parse("7252F49D-CA4C-4623-BE6D-55C90602C1C1"),
                           Level = ProcessLogConstants.MessageLevel.Fatal,
                           Name = "Fatal",
                           Description = "A message describing a severe error that halted processing of the Event",
                       },
                   };

        var models = data.Select(config =>
                                     new
                                     {
                                         Entity = new MessageLevel
                                         {
                                             Id = config.Id,
                                             Level = config.Level,
                                             UpdatedBy = "Reference Data 1.0",
                                         },
                                         Translation = new MessageLevelTranslation
                                         {
                                             Id = config.Id,
                                             CultureCode = ServiceConstants.CultureCode.Default,
                                             Name = config.Name,
                                             Description = config.Description,
                                             UpdatedBy = "Reference Data 1.0",
                                         }
                                     }).ToArray();

        modelBuilder.Entity<MessageLevel>().HasData(models.Select(m => m.Entity));
        modelBuilder.Entity<MessageLevelTranslation>().HasData(models.Select(m => m.Translation));
    }

    private void AddFilePurposes(ModelBuilder modelBuilder)
    {
        var data = new[]
                {
                    new
                    {
                        Id = Guid.Parse("D2F9C6E4-9A1B-4F4F-9B6D-8E1B27EF7F41"),
                        PurposeName = "Originating Contract",
                        IsSystemGenerated = false,
                        IsDownloadable = false
                    },
                    new
                    {
                        Id = Guid.Parse("A4BE1C12-5C39-497D-A4A2-42D3CC4AC851"),
                        PurposeName = "Contract Pricing Rules",
                        IsSystemGenerated = true,
                        IsDownloadable = true
                    },
                    new
                    {
                        Id = Guid.Parse("b54e58a5-6076-4333-8c8c-76c32992ae39"),
                        PurposeName = "Originating x12 transactions",
                        IsSystemGenerated = false,
                        IsDownloadable = false
                    },
                    new
                    {
                        Id = Guid.Parse("3F324E2A-42DF-4017-9664-39CA2C2C50C4"),
                        PurposeName = "Contract Pricing Rules Excel",
                        IsSystemGenerated = true,
                        IsDownloadable = true
                    }
                };

        var models = data.Select(config =>
                                    new FilePurpose
                                    {
                                        Id = config.Id,
                                        PurposeName = config.PurposeName,
                                        IsSystemGenerated = config.IsSystemGenerated,
                                        IsDownloadable = config.IsDownloadable,
                                        UpdatedBy = "Reference Data 1.0",
                                    }).ToArray();

        modelBuilder.Entity<FilePurpose>().HasData(models);
    }

    private void AddX12Statuses(ModelBuilder modelBuilder)
    {
        var data = new[]
                   {
                       new
                       {
                           Id = Guid.Parse("21C50E68-788D-41C5-A4F1-05D1E9AA00F8"),
                           Status = ProcessLogConstants.X12Status.Accepted,
                           Name = "Accepted",
                           Description = "The X12 record was validated and accepted",
                       },
                       new
                       {
                           Id = Guid.Parse("CF1E5C7F-C9B7-443F-B7FB-BDAC96C9FC60"),
                           Status = ProcessLogConstants.X12Status.Rejected,
                           Name = "Rejected",
                           Description = "The X12 record was rejected for reasons other than being Invalid",
                       },
                       new
                       {
                           Id = Guid.Parse("E119C843-1C46-4571-B379-EEE66F6B7E7B"),
                           Status = ProcessLogConstants.X12Status.Invalid,
                           Name = "Error",
                           Description = "The X12 record was rejected do to validation errors",
                       },
                       new
                       {
                           Id = Guid.Parse("65A9F7AB-757F-4FC8-BBCE-571039900B9E"),
                           Status = ProcessLogConstants.X12Status.Duplicate,
                           Name = "Duplicate",
                           Description = "The X12 record was rejected as a duplicate",
                       },
                   };

        var models = data.Select(config =>
                                     new
                                     {
                                         Entity = new X12Status
                                         {
                                             Id = config.Id,
                                             Status = config.Status,
                                             UpdatedBy = "Reference Data 1.0",
                                         },
                                         Translation = new X12StatusTranslation
                                         {
                                             Id = config.Id,
                                             CultureCode = ServiceConstants.CultureCode.Default,
                                             Name = config.Name,
                                             Description = config.Description,
                                             UpdatedBy = "Reference Data 1.0",
                                         }
                                     }).ToArray();

        modelBuilder.Entity<X12Status>().HasData(models.Select(m => m.Entity));
        modelBuilder.Entity<X12StatusTranslation>().HasData(models.Select(m => m.Translation));
    }
}
