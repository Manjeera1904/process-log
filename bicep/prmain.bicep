targetScope = 'subscription'

param azureContainerRegistry string
param azureContainerWebAppName string
param azureContainerRegistryImageTag string
param azureContainerRegistryWebImageName string
param userAssignedManagedIdentityName string
param deploymentPrefix string
param resourceGroupName string
param containerAppEnvironmentName string
param environmentName string
param keyVaultName string
param azureContainerRegistryAPIImageName string
param azureContainerAPIName string
param commonRGName string
param dnsZoneName string
param customDomainNameWeb string
param customDomainNameAPI string
param azureContainerWebFdqn string
param azureContainerAPIFdqn string
param location string
param webCertificateName string
param apiCertificateName string
param certificateName string
param keyVaultUrl string
param serviceBusNamespace string
param projectName string
param ClientSpecific string 
param prExpiryDate string
param TierWeb string
param TierAPI string
param TechStackWeb string
param TechStackApi string
param subscriptionProcessLog string
param topicProcessLog string
param subscriptionAppliationEvents string
param topicAppliationEvents string
param servicePrincipalObjectId string
param sideCarImageName string
param Servicebus string

var resourceTagsWeb = {
  Environment: environmentName
  ClientSpecific: ClientSpecific
  PRID: environmentName
  PRExpireDate: prExpiryDate
  Tier: TierWeb
  TechStack: TechStackWeb
}

var resourceTagsApi = {
  Environment: environmentName
  ClientSpecific: ClientSpecific
  PRID: environmentName
  PRExpireDate: prExpiryDate
  Tier: TierAPI
  TechStack: TechStackApi
}

var resourceTagsServiceBus = {
  Environment: environmentName
  ClientSpecific: ClientSpecific
  PRID: environmentName
  PRExpireDate: prExpiryDate
  Tier: Servicebus
}

resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2022-01-31-preview' existing = {
  name: userAssignedManagedIdentityName
  scope: resourceGroup(resourceGroupName)
}


module webContainerApp './modules/containerApp.bicep' = {
  name: '${deploymentPrefix}-${azureContainerRegistryWebImageName}-aca'
  params: {
    azureContainerRegistryImageName: azureContainerRegistryWebImageName
    azureContainerRegistry: azureContainerRegistry
    azureContainerRegistryImageTag: azureContainerRegistryImageTag
    userAssignedManagedIdentityName: userAssignedManagedIdentityName
    containerAppEnvironmentName: containerAppEnvironmentName
    containerAppName: azureContainerWebAppName
    targetPort: 8086
    keyVaultName: keyVaultName
    location: location
    sideCarImageName: sideCarImageName
    environmentName: environmentName
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
    certificateName: certificateName
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
    customDomainName: customDomainNameAPI
    azureContainerAppNameFdqn: azureContainerAPIFdqn
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
    certificateName: certificateName
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

module servicebus './modules/serviceBusPr.bicep' = {
  name: '${deploymentPrefix}-servicebus'
  params:{
     namespaceName:serviceBusNamespace
    topicProcessLog:topicProcessLog
    subscriptionProcessLog:subscriptionProcessLog
    topicAppliationEvents:topicAppliationEvents
    subscriptionAppliationEvents:subscriptionAppliationEvents
    servicePrincipalObjectId: servicePrincipalObjectId
    userAssignedIdentityName: userAssignedManagedIdentityName
    resourceTags: resourceTagsServiceBus
    }
  scope: resourceGroup(resourceGroupName)
  dependsOn: [
    apiContainerAppCertificateBinding
  ]
}
