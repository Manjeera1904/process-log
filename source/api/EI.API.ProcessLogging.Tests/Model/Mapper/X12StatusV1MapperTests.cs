using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Model;
using EI.API.ProcessLogging.Model.Mapper;
using EI.Data.TestHelpers.Mapper;

namespace EI.API.ProcessLogging.Tests.Model.Mapper;

[TestClass] public class X12StatusV1MapperTests : BaseMapperTests<X12StatusV1, X12Status, ProcessLogDtoAutomapperProfile>;