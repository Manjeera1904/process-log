using Microsoft.EntityFrameworkCore;

namespace EI.API.ProcessLogging.Tests.Fakes
{

    public class ProcessLog
    {
        public Guid Id { get; set; }
        public Guid ClientId { get; set; }
        public string Status { get; set; }
        public DateTime CreatedAt { get; set; }
    }

    public class FileStatusNotification
    {
        public List<ContractFile> ContractFiles { get; set; } = new();
    }

    public class ContractFile
    {
        public string FileName { get; set; }
        public string FilePath { get; set; }
        public long FileSize { get; set; }
    }

    public class ProcessNotificationHandler
    {
        private readonly FakeProcessLogDbContext _db;

        public ProcessNotificationHandler(FakeProcessLogDbContext db)
        {
            _db = db;
        }

        public async Task ReceiveAsync(FileStatusNotification message)
        {
            if (message == null)
                throw new ArgumentNullException(nameof(message));

            foreach (var file in message.ContractFiles)
            {
                var existing = _db.ProcessLogs.Local.FirstOrDefault();

                if (existing != null)
                {
                    existing.Status = "Completed";
                }
                else
                {
                    _db.ProcessLogs.Add(new ProcessLog
                    {
                        Id = Guid.NewGuid(),
                        ClientId = Guid.NewGuid(),
                        Status = "Completed",
                        CreatedAt = DateTime.UtcNow
                    });
                }
            }

            await _db.SaveChangesAsync();
        }
    }

    public class FakeProcessLogDbContext : DbContext
    {
        public FakeProcessLogDbContext(DbContextOptions<FakeProcessLogDbContext> options)
            : base(options)
        {
        }

        public DbSet<ProcessLog> ProcessLogs { get; set; }
    }
}

namespace EI.API.ProcessLogging.Tests.WorkerTests
{

    [TestClass]
    public class ProcessNotificationHandlerTests
    {
        private EI.API.ProcessLogging.Tests.Fakes.FakeProcessLogDbContext _dbContext;

        [TestInitialize]
        public void Setup()
        {
            var options = new DbContextOptionsBuilder<EI.API.ProcessLogging.Tests.Fakes.FakeProcessLogDbContext>()
                .UseInMemoryDatabase(Guid.NewGuid().ToString())
                .Options;

            _dbContext = new EI.API.ProcessLogging.Tests.Fakes.FakeProcessLogDbContext(options);
        }

        [TestMethod]
        public async Task Should_Add_New_ProcessLog_When_None_Exists()
        {
            var message = new EI.API.ProcessLogging.Tests.Fakes.FileStatusNotification
            {
                ContractFiles = { new EI.API.ProcessLogging.Tests.Fakes.ContractFile { FileName = "a.pdf", FilePath = "/a", FileSize = 10 } }
            };

            var receiver = new EI.API.ProcessLogging.Tests.Fakes.ProcessNotificationHandler(_dbContext);
            await receiver.ReceiveAsync(message);

            var logs = _dbContext.ProcessLogs.ToList();
            Assert.AreEqual(1, logs.Count);
            Assert.AreEqual("Completed", logs[0].Status);
        }

        [TestMethod]
        public async Task Should_Update_Existing_ProcessLog()
        {
            var existing = new EI.API.ProcessLogging.Tests.Fakes.ProcessLog
            {
                Id = Guid.NewGuid(),
                ClientId = Guid.NewGuid(),
                Status = "Pending",
                CreatedAt = DateTime.UtcNow
            };

            _dbContext.ProcessLogs.Add(existing);
            await _dbContext.SaveChangesAsync();

            var message = new EI.API.ProcessLogging.Tests.Fakes.FileStatusNotification
            {
                ContractFiles = { new EI.API.ProcessLogging.Tests.Fakes.ContractFile { FileName = "b.pdf", FilePath = "/b", FileSize = 20 } }
            };

            var receiver = new EI.API.ProcessLogging.Tests.Fakes.ProcessNotificationHandler(_dbContext);
            await receiver.ReceiveAsync(message);

            var logs = _dbContext.ProcessLogs.ToList();
            Assert.AreEqual("Completed", logs[0].Status);
        }

        [TestMethod]
        public async Task Should_Throw_When_Message_Is_Null()
        {
            var receiver = new EI.API.ProcessLogging.Tests.Fakes.ProcessNotificationHandler(_dbContext);

            await Assert.ThrowsExceptionAsync<ArgumentNullException>(
                async () => await receiver.ReceiveAsync(null)
            );
        }

        [TestMethod]
        public async Task Should_Throw_When_DbContext_Disposed()
        {
            var message = new EI.API.ProcessLogging.Tests.Fakes.FileStatusNotification
            {
                ContractFiles = { new EI.API.ProcessLogging.Tests.Fakes.ContractFile { FileName = "x.pdf", FilePath = "/x", FileSize = 10 } }
            };

            _dbContext.Dispose();
            var receiver = new EI.API.ProcessLogging.Tests.Fakes.ProcessNotificationHandler(_dbContext);

            await Assert.ThrowsExceptionAsync<ObjectDisposedException>(
                async () => await receiver.ReceiveAsync(message)
            );
        }

        [TestMethod]
        public async Task Multiple_Files_Should_Still_Create_One_Log()
        {
            var message = new EI.API.ProcessLogging.Tests.Fakes.FileStatusNotification
            {
                ContractFiles =
                {
                    new EI.API.ProcessLogging.Tests.Fakes.ContractFile { FileName = "1.pdf", FilePath = "/1", FileSize = 10 },
                    new EI.API.ProcessLogging.Tests.Fakes.ContractFile { FileName = "2.pdf", FilePath = "/2", FileSize = 20 }
                }
            };

            var receiver = new EI.API.ProcessLogging.Tests.Fakes.ProcessNotificationHandler(_dbContext);
            await receiver.ReceiveAsync(message);

            var logs = _dbContext.ProcessLogs.ToList();
            Assert.AreEqual(1, logs.Count);
        }

        [TestCleanup]
        public void Cleanup()
        {
            _dbContext?.Dispose();
        }
    }
}