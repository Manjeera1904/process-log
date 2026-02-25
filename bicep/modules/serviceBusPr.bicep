@description('Name of the Service Bus namespace')
param namespaceName string

@description('Location for the namespace')
param location string = resourceGroup().location

@description('Subscription name for process log')
param subscriptionProcessLog string

@description('Tags to be applied to all resources')
param resourceTags object

@description('Topic name for process log')
param topicProcessLog string

@description('Subscription name for application events')
param subscriptionAppliationEvents string

@description('Topic name for application events')
param topicAppliationEvents string

@description('Object ID of the Service Principal that needs access')
param servicePrincipalObjectId string

@description('Name of the User Assigned Managed Identity')
param userAssignedIdentityName string

resource uami 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' existing = {
  name: userAssignedIdentityName
}

var uamiPrincipalId = uami.properties.principalId

resource serviceBusNamespace 'Microsoft.ServiceBus/namespaces@2022-10-01-preview' = {
  name: namespaceName
  location: location
  tags: resourceTags
  sku: {
    name: 'Standard'
    tier: 'Standard'
  }
  properties: {
    disableLocalAuth: true
  }
}

var roleSender   = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '69a216fc-b8fb-44d8-bc22-1f3c2cd27a39')
var roleReceiver = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4f6d3b9b-027b-4f4c-9142-0e5a2a2247e0')

resource spSender 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(serviceBusNamespace.id, 'sp-sender')
  scope: serviceBusNamespace
  properties: {
    roleDefinitionId: roleSender
    principalId: servicePrincipalObjectId
    principalType: 'ServicePrincipal'
  }
}

resource spReceiver 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(serviceBusNamespace.id, 'sp-receiver')
  scope: serviceBusNamespace
  properties: {
    roleDefinitionId: roleReceiver
    principalId: servicePrincipalObjectId
    principalType: 'ServicePrincipal'
  }
}

resource uamiSender 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(serviceBusNamespace.id, 'uami-sender')
  scope: serviceBusNamespace
  properties: {
    roleDefinitionId: roleSender
    principalId: uamiPrincipalId
    principalType: 'ServicePrincipal'
  }
}

resource uamiReceiver 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(serviceBusNamespace.id, 'uami-receiver')
  scope: serviceBusNamespace
  properties: {
    roleDefinitionId: roleReceiver
    principalId: uamiPrincipalId
    principalType: 'ServicePrincipal'
  }
}


resource topicsProcessLog 'Microsoft.ServiceBus/namespaces/topics@2024-01-01' = {
  parent: serviceBusNamespace
  name: topicProcessLog
  properties: {
    autoDeleteOnIdle: 'P10675199D'
    defaultMessageTimeToLive: 'P14D'
    duplicateDetectionHistoryTimeWindow: 'PT10M'
    enableBatchedOperations: true
    enableExpress: false
    enablePartitioning: false
    maxMessageSizeInKilobytes: 256
    maxSizeInMegabytes: 4096
    requiresDuplicateDetection: false
    supportOrdering: true
  }
}

resource subscriptionsProcessLog 'Microsoft.ServiceBus/namespaces/topics/subscriptions@2024-01-01' = {
  parent: topicsProcessLog
  name: subscriptionProcessLog
  properties: {
    autoDeleteOnIdle: 'P10675199D'
    deadLetteringOnFilterEvaluationExceptions: true
    deadLetteringOnMessageExpiration: true
    defaultMessageTimeToLive: 'P14D'
    duplicateDetectionHistoryTimeWindow: 'PT10M'
    enableBatchedOperations: true
    isClientAffine: false
    lockDuration: 'PT5M'
    maxDeliveryCount: 10
    requiresSession: false
  }
}


resource topicsAppliationEvents 'Microsoft.ServiceBus/namespaces/topics@2024-01-01' = {
  parent: serviceBusNamespace
  name: topicAppliationEvents
  properties: {
    autoDeleteOnIdle: 'P10675199D'
    defaultMessageTimeToLive: 'P14D'
    duplicateDetectionHistoryTimeWindow: 'PT10M'
    enableBatchedOperations: true
    enableExpress: false
    enablePartitioning: false
    maxMessageSizeInKilobytes: 256
    maxSizeInMegabytes: 4096
    requiresDuplicateDetection: false
    supportOrdering: true
  }
}

resource subscriptionsAppliationEvents 'Microsoft.ServiceBus/namespaces/topics/subscriptions@2024-01-01' = {
  parent: topicsAppliationEvents
  name: subscriptionAppliationEvents
  properties: {
    autoDeleteOnIdle: 'P10675199D'
    deadLetteringOnFilterEvaluationExceptions: true
    deadLetteringOnMessageExpiration: true
    defaultMessageTimeToLive: 'P14D'
    duplicateDetectionHistoryTimeWindow: 'PT10M'
    enableBatchedOperations: true
    isClientAffine: false
    lockDuration: 'PT5M'
    maxDeliveryCount: 10
    requiresSession: false
  }
}
