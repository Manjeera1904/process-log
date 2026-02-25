using EI.API.ProcessLogging.Data;
using EI.API.ProcessLogging.Data.Context;
using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Worker.Model;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;

namespace EI.API.ProcessLogging.Worker.Services;

public class FileLogProcessor(ILogger<FileLogProcessor> logger)
{
    public async Task AddFilesAsync(
        ProcessLogDbContext context,
        Guid processLogId,
        IEnumerable<FileEntry>? files,
        DateTime timestamp,
        string createdBy
    )
    {
        if (files == null)
            return;

        var existing = await context
            .FileProcessLogs.Where(f => f.ProcessLogId == processLogId)
            .Select(f => new { f.FileName, f.FilePath })
            .ToListAsync();
        //HashSet to avoid duplicates in the database and in the same batch
        var fileSet = new HashSet<string>(
            existing.Select(x => $"{x.FileName}|{x.FilePath}"),
            StringComparer.OrdinalIgnoreCase
        );

        foreach (var file in files)
        {
            if (
                string.IsNullOrWhiteSpace(file.FileName) || string.IsNullOrWhiteSpace(file.FilePath)
            )
            {
                logger.LogWarning("Skipping FileProcessLog due to missing FileName/FilePath");
                continue;
            }

            var key = $"{file.FileName}|{file.FilePath}";

            if (fileSet.Contains(key))
                continue;

            fileSet.Add(key);

            var fileLog = new FileProcessLog
            {
                Id = Guid.NewGuid(),
                ProcessLogId = processLogId,
                FileName = file.FileName,
                FilePath = file.FilePath,
                FileSize = file.FileSize ?? 0,
                PurposeName = file.FilePurpose,
                ProcessStatus = file.Status ?? string.Empty,
                UpdatedBy = createdBy,
            };

            try
            {
                await context.FileProcessLogs.AddAsync(fileLog);
            }
            catch (Exception ex)
            {
                logger.LogError(
                    ex,
                    "Failed to  Add data to FileProcessLogs FileName: {FileLog}",
                    fileLog.FileName
                );
                throw;
            }

            //TODO: this a first implementation   "List of messages needd Database Changes
            if (file.Messages?.Any() == true)
            {
                foreach (var msg in file.Messages)
                {
                    await context
                        .ProcessLogMessages.AddAsync(
                            new ProcessLogMessage
                            {
                                ProcessLogId = processLogId,
                                Level = msg.MessageLevel ?? ProcessLogConstants.MessageLevel.Info,
                                Message = $"{file.FileName}: {msg.Message}",
                                MessageTimestamp = timestamp,
                                UpdatedBy = createdBy,
                            }
                        )
                        .ConfigureAwait(false);
                }
            }
        }
    }
}
