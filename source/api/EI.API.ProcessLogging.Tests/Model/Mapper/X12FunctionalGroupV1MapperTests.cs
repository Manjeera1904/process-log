using EI.API.ProcessLogging.Data.Entities;
using EI.API.ProcessLogging.Model;
using EI.API.ProcessLogging.Model.Mapper;
using EI.Data.TestHelpers.Mapper;

namespace EI.API.ProcessLogging.Tests.Model.Mapper;

[TestClass] public class X12FunctionalGroupV1MapperTests : BaseMapperTests<X12FunctionalGroupV1, X12FunctionalGroup, ProcessLogDtoAutomapperProfile>;