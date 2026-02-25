using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Model;
using EI.API.ProcessLogging.Model.Mapper;
using EI.Data.TestHelpers.Mapper;

namespace EI.API.ProcessLogging.Tests.Model.Mapper;

[TestClass] public class X12TransactionSetV1MapperTests : BaseMapperTests<X12TransactionSetV1, X12TransactionSet, ProcessLogDtoAutomapperProfile>;