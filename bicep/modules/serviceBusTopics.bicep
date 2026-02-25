@description('The name of the Azure Service Bus namespace')
param namespaceName string

resource serviceBusNamespace 'Microsoft.ServiceBus/namespaces@2021-06-01' existing = {
  name: namespaceName
}


// -----------------------------------------------------------------------------------
//
//   Topic:    file-received
//
// -----------------------------------------------------------------------------------
resource topicFileReceived 'Microsoft.ServiceBus/namespaces/topics@2024-01-01' = {
  parent: serviceBusNamespace
  name: 'file-received'
  properties: {
    autoDeleteOnIdle: 'P10675199D' // Delete the topic if it is idle for this duration - but we never want to delete it!
    defaultMessageTimeToLive: 'P14D' // 14 days
    duplicateDetectionHistoryTimeWindow: 'PT10M' // 10 minutes
    enableBatchedOperations: true
    enableExpress: false
    enablePartitioning: false
    maxMessageSizeInKilobytes: 256
    maxSizeInMegabytes: 4096
    requiresDuplicateDetection: false
    supportOrdering: true
  }
}

resource subscriptionFileReceivedNewDocument 'Microsoft.ServiceBus/namespaces/topics/subscriptions@2024-01-01' = {
  parent: topicFileReceived
  name: 'file-status-notification'
  properties: {
    autoDeleteOnIdle: 'P10675199D' // Delete the topic if it is idle for this duration - but we never want to delete it!
    deadLetteringOnFilterEvaluationExceptions: true
    deadLetteringOnMessageExpiration: true
    defaultMessageTimeToLive: 'P14D' // 14 days
    duplicateDetectionHistoryTimeWindow: 'PT10M'
    enableBatchedOperations: true
    isClientAffine: false
    lockDuration: 'PT5M'
    maxDeliveryCount: 10
    requiresSession: false
  }
}

// resource subscriptionFileReceivedRuleNewDocument 'Microsoft.ServiceBus/namespaces/topics/subscriptions/rules@2024-01-01' = {
//   name: 'FilterMessageStatusNew'
//   parent: subscriptionFileReceivedNewDocument
//   properties: {
//     filterType: 'SqlFilter'
//     sqlFilter: {
//       sqlExpression: '"MessageStatus = \'New\'"'
//     }
//   }
// }


// -----------------------------------------------------------------------------------
//
//   Topic:    x12-parse-result
//
// -----------------------------------------------------------------------------------
resource topicX12ParseResult 'Microsoft.ServiceBus/namespaces/topics@2024-01-01' = {
  parent: serviceBusNamespace
  name: 'x12-parse-result'
  properties: {
    autoDeleteOnIdle: 'P10675199D' // Delete the topic if it is idle for this duration - but we never want to delete it!
    defaultMessageTimeToLive: 'P14D' // 14 days
    duplicateDetectionHistoryTimeWindow: 'PT10M' // 10 minutes
    enableBatchedOperations: true
    enableExpress: false
    enablePartitioning: false
    maxMessageSizeInKilobytes: 256
    maxSizeInMegabytes: 4096
    requiresDuplicateDetection: false
    supportOrdering: true
  }
}

resource subscriptionX12Valid 'Microsoft.ServiceBus/namespaces/topics/subscriptions@2024-01-01' = {
  parent: topicX12ParseResult
  name: 'valid'
  properties: {
    autoDeleteOnIdle: 'P10675199D' // Delete the topic if it is idle for this duration - but we never want to delete it!
    deadLetteringOnFilterEvaluationExceptions: true
    deadLetteringOnMessageExpiration: true
    defaultMessageTimeToLive: 'P14D' // 14 days
    duplicateDetectionHistoryTimeWindow: 'PT10M'
    enableBatchedOperations: true
    isClientAffine: false
    lockDuration: 'PT5M'
    maxDeliveryCount: 10
    requiresSession: false
  }
}

resource subscriptionX12ResultReceivedRuleValid 'Microsoft.ServiceBus/namespaces/topics/subscriptions/rules@2024-01-01' = {
  name: 'FilterMessageStatusValid'
  parent: subscriptionX12Valid
  properties: {
    filterType: 'SqlFilter'
    sqlFilter: {
      sqlExpression: 'MessageStatus = \'Valid\''
    }
  }
}


resource subscriptionX12Invalid 'Microsoft.ServiceBus/namespaces/topics/subscriptions@2024-01-01' = {
  parent: topicX12ParseResult
  name: 'invalid'
  properties: {
    autoDeleteOnIdle: 'P10675199D' // Delete the topic if it is idle for this duration - but we never want to delete it!
    deadLetteringOnFilterEvaluationExceptions: true
    deadLetteringOnMessageExpiration: true
    defaultMessageTimeToLive: 'P14D' // 14 days
    duplicateDetectionHistoryTimeWindow: 'PT10M'
    enableBatchedOperations: true
    isClientAffine: false
    lockDuration: 'PT5M'
    maxDeliveryCount: 10
    requiresSession: false
  }
}

resource subscriptionX12ResultReceivedRuleInvalid 'Microsoft.ServiceBus/namespaces/topics/subscriptions/rules@2024-01-01' = {
  name: 'FilterMessageStatusInvalid'
  parent: subscriptionX12Invalid
  properties: {
    filterType: 'SqlFilter'
    sqlFilter: {
      sqlExpression: 'MessageStatus = \'Invalid\''
    }
  }
}
// -----------------------------------------------------------------------------------
//
//   Topic:    process-logging
//
// -----------------------------------------------------------------------------------

resource topicProcessLogging 'Microsoft.ServiceBus/namespaces/topics@2024-01-01' = {
  parent: serviceBusNamespace
  name: 'process-logging'
  properties: {
    autoDeleteOnIdle: 'P10675199D' // Never auto-delete
    defaultMessageTimeToLive: 'P14D' // 14 days
    duplicateDetectionHistoryTimeWindow: 'PT10M' // 10 minutes
    enableBatchedOperations: true
    enableExpress: false
    enablePartitioning: false
    maxMessageSizeInKilobytes: 256
    maxSizeInMegabytes: 4096
    requiresDuplicateDetection: false
    supportOrdering: true
  }
}

// Create the subscription for process-notifications
resource subscriptionProcessNotifications 'Microsoft.ServiceBus/namespaces/topics/subscriptions@2024-01-01' = {
  parent: topicProcessLogging
  name: 'process-notifications'
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

