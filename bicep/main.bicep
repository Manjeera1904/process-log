targetScope = 'subscription'

param azureContainerRegistry string
param azureContainerWebAppName string
param azureContainerAPIName string
param azureContainerRegistryWebImageName string
param azureContainerRegistryAPIImageName string
param userAssignedManagedIdentityName string
param deploymentPrefix string
param resourceGroupName string
param containerAppEnvironmentName string
param environmentName string
param projectName string
param keyVaultName string
param azureContainerRegistryImageTag string
param commonRGName string
param dnsZoneName string
param customDomainNameWeb string
param customDomainNameAPI string
param azureContainerWebFdqn string
param azureContainerAPIFdqn string
param location string
param webCertificateName string
param apiCertificateName string
param serviceBusNamespace string
param ClientSpecific string
param TierWeb string
param TierAPI string
param TechStackWeb string
param TechStackApi string
param keyVaultUrl string
param sideCarImageName string

var resourceTagsWeb = {
  Environment: environmentName
  ClientSpecific: ClientSpecific
  Tier: TierWeb
  TechStack: TechStackWeb
  }

var resourceTagsApi = {
Environment: environmentName
ClientSpecific: ClientSpecific
Tier: TierAPI
TechStack: TechStackApi
}

resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2022-01-31-preview' existing = {
  name: userAssignedManagedIdentityName
  scope: resourceGroup(resourceGroupName)
}

module webContainerApp './modules/containerApp.bicep' = {
  name: '${deploymentPrefix}-${azureContainerRegistryWebImageName}-aca'
  params: {
    environmentName: environmentName
    azureContainerRegistryImageName: azureContainerRegistryWebImageName
    azureContainerRegistry: azureContainerRegistry
    containerAppEnvironmentName: containerAppEnvironmentName
    containerAppName: azureContainerWebAppName
    targetPort: 8086
    keyVaultName: keyVaultName
    userAssignedManagedIdentityName: userAssignedManagedIdentityName
    azureContainerRegistryImageTag: azureContainerRegistryImageTag
    sideCarImageName: sideCarImageName
    location: location
  }
  scope: resourceGroup(resourceGroupName)
}

module dnsRecordsweb 'modules/dnsRecords.bicep' = {
  scope: resourceGroup(commonRGName)
  name: '${deploymentPrefix}-dns-${azureContainerRegistryWebImageName}'
  params: {
    dnsZoneName: dnsZoneName
    cnameRecordName: '${azureContainerRegistryWebImageName}.${environmentName}'
    ttl: 3600
    cnameTargetFqdn: webContainerApp.outputs.fdqn
    txtValue: webContainerApp.outputs.customDomainVerificationId
    txtRecordName: 'asuid.${azureContainerRegistryWebImageName}.${environmentName}'
  }
}

module webContainerAppCustomDomain './modules/customDomain.bicep' = {
  name: '${deploymentPrefix}-${azureContainerRegistryWebImageName}-custom-domain'
  params: {
    environmentName: environmentName
    azureContainerRegistryImageName: azureContainerRegistryWebImageName
    azureContainerRegistry: azureContainerRegistry
    containerAppEnvironmentName: containerAppEnvironmentName
    containerAppName: azureContainerWebAppName
    targetPort: 8086
    keyVaultName: keyVaultName
    userAssignedManagedIdentityName: userAssignedManagedIdentityName
    azureContainerRegistryImageTag: azureContainerRegistryImageTag
    customDomainName: customDomainNameWeb
    azureContainerAppNameFdqn: azureContainerWebFdqn
    sideCarImageName: sideCarImageName
    location: location
  }
  scope: resourceGroup(resourceGroupName)
  dependsOn: [
    dnsRecordsweb
  ]
}

module webContainerAppCertificate './modules/certificate.bicep' = {
  name: '${deploymentPrefix}-${azureContainerRegistryWebImageName}-certificate'
  params: {
    customDomainName: customDomainNameWeb
    location: location
    customAppName: azureContainerWebAppName
    containerAppEnvironmentName: containerAppEnvironmentName
    certificateName: containerAppEnvironmentName
  }
  scope: resourceGroup(resourceGroupName)
  dependsOn: [
    webContainerAppCustomDomain
  ]
}

module webContainerAppCertificateBinding './modules/certificateBinding.bicep' = {
  name: '${deploymentPrefix}-${azureContainerRegistryWebImageName}-certificateBinding'
  params: {
    environmentName: environmentName
    customDomainName: customDomainNameWeb
    location: location
    azureContainerRegistryImageName: azureContainerRegistryWebImageName
    azureContainerRegistry: azureContainerRegistry
    containerAppEnvironmentName: containerAppEnvironmentName
    containerAppName: azureContainerWebAppName
    targetPort: 8086
    keyVaultName: keyVaultName
    userAssignedManagedIdentityName: userAssignedManagedIdentityName
    azureContainerRegistryImageTag: azureContainerRegistryImageTag
    managedCertificateName: webCertificateName
    keyVaultUrl: keyVaultUrl
    serviceBusNamespace: serviceBusNamespace
    resourceTags: resourceTagsWeb
    sideCarImageName: sideCarImageName
    clientIdentity: identity.properties.clientId
  }
  scope: resourceGroup(resourceGroupName)
  dependsOn: [
    webContainerAppCertificate
  ]
}

module apiContainerApp './modules/containerApp.bicep' = {
  name: '${deploymentPrefix}-${azureContainerRegistryAPIImageName}-aca'
  params: {
    environmentName: environmentName
    azureContainerRegistryImageName: azureContainerRegistryAPIImageName
    azureContainerRegistry: azureContainerRegistry
    containerAppEnvironmentName: containerAppEnvironmentName
    containerAppName: azureContainerAPIName
    targetPort: 8080
    keyVaultName: keyVaultName
    userAssignedManagedIdentityName: userAssignedManagedIdentityName
    azureContainerRegistryImageTag: azureContainerRegistryImageTag
    sideCarImageName: sideCarImageName
    location: location
  }
  scope: resourceGroup(resourceGroupName)
  dependsOn: [
    webContainerAppCertificateBinding
  ]
}

module dnsRecordsapi 'modules/dnsRecords.bicep' = {
  scope: resourceGroup(commonRGName)
  name: '${deploymentPrefix}-dns-${azureContainerRegistryAPIImageName}'
  params: {
    dnsZoneName: dnsZoneName
    cnameRecordName: '${azureContainerRegistryAPIImageName}.${environmentName}'
    ttl: 3600
    cnameTargetFqdn: apiContainerApp.outputs.fdqn
    txtValue: apiContainerApp.outputs.customDomainVerificationId
    txtRecordName: 'asuid.${azureContainerRegistryAPIImageName}.${environmentName}'
  }
}

module apiContainerAppCustomDomain './modules/customDomain.bicep' = {
  name: '${deploymentPrefix}-${azureContainerRegistryAPIImageName}-custom-domain'
  params: {
    environmentName: environmentName
    azureContainerRegistryImageName: azureContainerRegistryAPIImageName
    azureContainerRegistry: azureContainerRegistry
    containerAppEnvironmentName: containerAppEnvironmentName
    containerAppName: azureContainerAPIName
    targetPort: 8080
    keyVaultName: keyVaultName
    userAssignedManagedIdentityName: userAssignedManagedIdentityName
    azureContainerRegistryImageTag: azureContainerRegistryImageTag
    azureContainerAppNameFdqn: azureContainerAPIFdqn
    customDomainName: customDomainNameAPI
    sideCarImageName: sideCarImageName
    location: location
  }
  scope: resourceGroup(resourceGroupName)
  dependsOn: [
    dnsRecordsapi
  ]
}

module apiContainerAppCertificate './modules/certificate.bicep' = {
  name: '${deploymentPrefix}-${azureContainerRegistryAPIImageName}-certificate'
  params: {
    customDomainName: customDomainNameAPI
    location: location
    customAppName: azureContainerAPIName
    containerAppEnvironmentName: containerAppEnvironmentName
    certificateName: containerAppEnvironmentName
  }
  scope: resourceGroup(resourceGroupName)
  dependsOn: [
    apiContainerAppCustomDomain
  ]
}

module apiContainerAppCertificateBinding './modules/certificateBinding.bicep' = {
  name: '${deploymentPrefix}-${azureContainerRegistryAPIImageName}-certificateBinding'
  params: {
    environmentName: environmentName
    customDomainName: customDomainNameAPI
    location: location
    azureContainerRegistryImageName: azureContainerRegistryAPIImageName
    azureContainerRegistry: azureContainerRegistry
    containerAppEnvironmentName: containerAppEnvironmentName
    containerAppName: azureContainerAPIName
    targetPort: 8080
    keyVaultName: keyVaultName
    userAssignedManagedIdentityName: userAssignedManagedIdentityName
    azureContainerRegistryImageTag: azureContainerRegistryImageTag
    managedCertificateName: apiCertificateName
    keyVaultUrl: keyVaultUrl
    serviceBusNamespace: serviceBusNamespace
    resourceTags: resourceTagsApi
    sideCarImageName: sideCarImageName
    clientIdentity: identity.properties.clientId
  }
  scope: resourceGroup(resourceGroupName)
  dependsOn: [
    apiContainerAppCertificate
  ]
}

module serviceBusTopics './modules/serviceBusTopics.bicep' = {
  name: '${deploymentPrefix}-serviceBusTopics-asb'
  params: {
    namespaceName: 'asb-${projectName}-${environmentName}'
  }
  scope: resourceGroup(resourceGroupName)
  dependsOn: [
    apiContainerAppCertificateBinding
  ]
}
