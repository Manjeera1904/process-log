param environmentName string
param location string
param customDomainName string
param managedCertificateName string
@description('The name of the Container App')
param containerAppName string

@description('The name of the Container App Environment')
param containerAppEnvironmentName string

@description('The name of the Container Registry (docker) Image')
param azureContainerRegistryImageName string

@description('The name of the Azure Container Registry')
param azureContainerRegistry string

@description('Common tags for resources')
param resourceTags object

param serviceBusNamespace string

param keyVaultUrl string

param azureContainerRegistryImageTag string

param targetPort int

@description('The name of the KeyVault')
param keyVaultName string

@description('The name of the SQL Database.')
param userAssignedManagedIdentityName string

param sideCarImageName string
param clientIdentity string
var mainContainerCpu = 1
var mainContainerMemory = '2Gi'
var sidecarCpu = 1
var sidecarMemory = '2Gi'
var isIntEnvironment = (environmentName == 'int')
var totalCpu = isIntEnvironment ? mainContainerCpu + sidecarCpu : 1
var totalMemory = isIntEnvironment ? '4Gi' : '2Gi'
var originUrl = '${environmentName}.eclipsevantage.com'
  
resource containerAppEnvironment 'Microsoft.App/managedEnvironments@2024-03-01' existing = {
  name: containerAppEnvironmentName
}

resource certificate 'Microsoft.App/managedEnvironments/managedCertificates@2022-11-01-preview' existing = {
  name: managedCertificateName
  parent: containerAppEnvironment
}

resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2022-01-31-preview' existing = {
  name: userAssignedManagedIdentityName
}

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' existing = {
  name: keyVaultName
}

var connectionStringsb = '${serviceBusNamespace}.servicebus.windows.net'

resource keyVaultAccessPolicy 'Microsoft.KeyVault/vaults/accessPolicies@2023-07-01' = {
  parent: keyVault
  name: 'add'
  properties: {
    accessPolicies: [
      {
        tenantId: subscription().tenantId
        objectId: identity.properties.principalId
        permissions: {
          secrets: [
            'get'
            'list'
          ]
        }
      }
    ]
  }
}
var isApiApp = contains(toLower(containerAppName), 'api')
var isLabOrDemo = contains(['lab', 'demo'], toLower(environmentName))

var minReplicasFinal = isLabOrDemo
  ? 1
  : (isApiApp ? 1 : 0)

var maxReplicasFinal = 1

var aspnetCoreEnvironment = environmentName == 'test' ? 'Staging' : (environmentName == 'demo' || environmentName == 'lab' ? 'Production' : 'Development')

resource containerApp 'Microsoft.App/containerApps@2023-08-01-preview' = {
  name: containerAppName
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${identity.id}': {}
    }
  }
  tags: resourceTags
  properties: {
    managedEnvironmentId: containerAppEnvironment.id
    configuration: {
      ingress: {
        external: true
        targetPort: isIntEnvironment ? 80 : targetPort
        allowInsecure: false
        traffic: [
          {
            latestRevision: true
            weight: 100
          }
        ]
        corsPolicy: environmentName == 'int' ? null : {
          allowedOrigins: union(
            [
              'https://${originUrl}'
            ],
            contains(['dev', 'test'], environmentName) ? ['http://localhost:8080'] : []
          )
          allowedMethods: [
            '*'
          ]
          allowedHeaders: [
            '*'
          ]
        }
        customDomains: [
          {
            certificateId: certificate.id
            bindingType: 'SniEnabled'
            name: customDomainName
          }
        ]
      }
      registries: [
        {
          server: '${azureContainerRegistry}.azurecr.io'
          identity: identity.id
        }
      ]
      secrets: [
        {
          name: 'app-insights-key'
          keyVaultUrl: 'https://${keyVault.name}.${keyVaultUrl}/secrets/appinsightsinstrumentationkey'
          identity: identity.id
        }
        {
          name: 'app-insights-connection-string'
          keyVaultUrl: 'https://${keyVault.name}.${keyVaultUrl}/secrets/appinsightsconnectionstring'
          identity: identity.id
        }
      ]
    }
    template: {
      containers: isIntEnvironment ? [
        {
          name: containerAppName
          image: '${azureContainerRegistry}.azurecr.io/${azureContainerRegistryImageName}:${azureContainerRegistryImageTag}'
          resources: {
            cpu: json(string(mainContainerCpu))
            memory: mainContainerMemory
          }
          env: [
            {
              name: 'ConnectionStrings__AzureKeyVault'
              value: 'https://${keyVault.name}.${keyVaultUrl}'
            }
            {
              name: 'ASPNETCORE_ENVIRONMENT'
              value: aspnetCoreEnvironment
            }
            {
              name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
              secretRef: 'app-insights-connection-string'
            }
            {
              name: 'AZURE_CLIENT_ID'
              value: clientIdentity
            }
            {
              name: 'SERVICES__PLATFORMCOREAPI__HTTPS__0'
              value: 'https://platform-core-api.${environmentName}.eclipsevantage.com'
            }
            {
              name: 'ConnectionStrings__AzureServiceBus'
              value: connectionStringsb
            }
          ]
          probes: [
            {
              type: 'Liveness'
              httpGet: {
                path: '/ServiceHealth'
                port: targetPort
                httpHeaders: [
                  {
                    name: 'User-Agent'
                    value: 'Azure Container App Liveness Probe'
                  }
                ]
              }
              initialDelaySeconds: 10
              periodSeconds: 30
            }
          ]
        }
        {
          name: 'cors-sidecar'
          image: '${azureContainerRegistry}.azurecr.io/${sideCarImageName}:${azureContainerRegistryImageTag}'
          resources: {
            cpu: json(string(sidecarCpu))
            memory: sidecarMemory
          }
          env: [
            {
              name: 'UPSTREAM_PORT'
              value: '${targetPort}'
            }
          ]
          probes: [
            {
              type: 'Liveness'
              httpGet: {
                path: '/ServiceHealth'
                port: 80
              }
              initialDelaySeconds: 5
              periodSeconds: 30
            }
          ]
        }
      ] : [
        {
          name: containerAppName
          image: '${azureContainerRegistry}.azurecr.io/${azureContainerRegistryImageName}:${azureContainerRegistryImageTag}'
          resources: {
            cpu: json(string(totalCpu))
            memory: totalMemory
          }
          env: [
            {
              name: 'PORT'
              value: '${targetPort}'
            }
            {
              name: 'ConnectionStrings__AzureKeyVault'
              value: 'https://${keyVault.name}.${keyVaultUrl}'
            }
            {
              name: 'ASPNETCORE_ENVIRONMENT'
              value: aspnetCoreEnvironment
            }
            {
              name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
              secretRef: 'app-insights-connection-string'
            }
            {
              name: 'AZURE_CLIENT_ID'
              value: clientIdentity
            }
            {
              name: 'SERVICES__PLATFORMCOREAPI__HTTPS__0'
              value: 'https://platform-core-api.${environmentName}.eclipsevantage.com'
            }
            {
              name: 'ConnectionStrings__AzureServiceBus'
              value: connectionStringsb
            }
          ]
          probes: [
            // Task#3951: Disabling temporarily - this is failing in the test environment, causing container crash loop
            {
              type: 'Liveness'
              httpGet: {
                path: '/ServiceHealth'
                port: targetPort
                httpHeaders: [
                  {
                    name: 'User-Agent'
                    value: 'Azure Container App Liveness Probe'
                  }
                ]
              }
              initialDelaySeconds: 10
              periodSeconds: 30
            }
          ]
        }
      ]
      scale: {
        minReplicas: minReplicasFinal
        maxReplicas: maxReplicasFinal
      }
    }
  }
}
