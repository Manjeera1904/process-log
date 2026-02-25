# https://hub.docker.com/_/microsoft-dotnet
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /source

ARG NUGET_TOKEN

# Create a temporary NuGet.Config file with the credentials
RUN dotnet new nugetconfig
RUN dotnet nuget add source https://pkgs.dev.azure.com/EclipseInsightsHC/Commercialization/_packaging/eclipse-insights-nuget/nuget/v3/index.json -n "eclipse-insights-nuget" -u UnusedButRequired -p $NUGET_TOKEN --store-password-in-clear-text

# copy csproj and restore as distinct layers
COPY ./EI.API.ProcessLogging/*.csproj ./EI.API.ProcessLogging/
COPY ./EI.API.ProcessLogging.Data/*.csproj ./EI.API.ProcessLogging.Data/
COPY ./EI.API.ProcessLogging.Worker/*.csproj ./EI.API.ProcessLogging.Worker/

RUN dotnet restore ./EI.API.ProcessLogging/EI.API.ProcessLogging.csproj
RUN rm nuget.config

# copy everything else and build app
COPY ./ ./

RUN dotnet publish ./EI.API.ProcessLogging/EI.API.ProcessLogging.csproj -c Release -o /app --no-restore

# final stage/image
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app ./
ENTRYPOINT ["dotnet", "EI.API.ProcessLogging.dll"]