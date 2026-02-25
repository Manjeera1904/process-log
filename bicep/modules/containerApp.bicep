@description('The name of the Container App')
param containerAppName string

@description('The name of the Container App Environment')
param containerAppEnvironmentName string

@description('The name of the Container Registry (docker) Image')
param azureContainerRegistryImageName string

@description('The name of the Azure Container Registry')
param azureContainerRegistry string

param azureContainerRegistryImageTag string

param targetPort int

@description('The name of the KeyVault')
param keyVaultName string

@description('The name.')
param userAssignedManagedIdentityName string

@description('The name of the Azure location')
param location string

@description('The name of the Environment being deployed to')
param environmentName string
param sideCarImageName string
var originUrl = '${environmentName}.eclipsevantage.com'
var mainContainerCpu = 1
var mainContainerMemory = '2Gi'
var sidecarCpu = 1
var sidecarMemory = '2Gi'
var isIntEnvironment = (environmentName == 'int')
var totalCpu = isIntEnvironment ? mainContainerCpu + sidecarCpu : 1
var totalMemory = isIntEnvironment ? '4Gi' : '2Gi'

resource containerAppEnvironment 'Microsoft.App/managedEnvironments@2024-03-01' existing = {
  name: containerAppEnvironmentName
}

resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2022-01-31-preview' existing = {
  name: userAssignedManagedIdentityName
}

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' existing = {
  name: keyVaultName
}

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

resource containerApp 'Microsoft.App/containerApps@2023-08-01-preview' = {
  name: containerAppName
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${identity.id}': {}
    }
  }
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
      }
      registries: [
        {
          server: '${azureContainerRegistry}.azurecr.io'
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
          env: []
          probes: []
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
          probes: []
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
          ]
          probes: []
        }
      ]
    }
  }
}

output fdqn string = containerApp.properties.configuration.ingress.fqdn
output customDomainVerificationId string = containerApp.properties.customDomainVerificationId
