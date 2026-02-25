using 'prmain.bicep'

param projectName = 'eclipsesaas'

param environmentName = ''

param prExpiryDate = ''

param TierWeb = 'Web App'

param TierAPI = 'API'

param TechStackWeb = 'React 18.2'

param TechStackApi = 'DotNet 8.0'

param ClientSpecific = 'No'

param azureContainerRegistryWebImageName = 'process-logging-web'

param azureContainerRegistryAPIImageName = 'process-logging-api'

param dnsZoneName = 'eclipsevantage.com'

param commonRGName = '${projectName}-common-rg'

param azureContainerRegistryImageTag = ''

param userAssignedManagedIdentityName = 'uaid-${projectName}-int'

param keyVaultName = 'kv-${projectName}-int'

param azureContainerRegistry = '${projectName}acr'

param azureContainerWebAppName = 'aca-process-logging-web-${environmentName}'

param deploymentPrefix = 'deploy-${environmentName}'

param resourceGroupName = '${projectName}-int-rg'

param containerAppEnvironmentName = 'cae-${projectName}-int'

param azureContainerAPIName = 'aca-process-logging-api-${environmentName}'

param customDomainNameWeb = '${azureContainerRegistryWebImageName}.${environmentName}.${dnsZoneName}'

param customDomainNameAPI = '${azureContainerRegistryAPIImageName}.${environmentName}.${dnsZoneName}'

param azureContainerWebFdqn = 'aca-${azureContainerRegistryWebImageName}-${environmentName}'

param azureContainerAPIFdqn = 'aca-${azureContainerRegistryAPIImageName}-${environmentName}'

param location = 'East US'

param webCertificateName = 'cae-eclipsesaas-${environmentName}-${azureContainerWebAppName}'

param apiCertificateName = 'cae-eclipsesaas-${environmentName}-${azureContainerAPIName}'

param certificateName = 'cae-eclipsesaas-${environmentName}'

param serviceBusNamespace = 'asb-${projectName}-${environmentName}'

param topicProcessLog = 'process-logging'

param subscriptionProcessLog = 'process-notifications'

param topicAppliationEvents = 'application-events'

param keyVaultUrl = 'vault.azure.net'

param subscriptionAppliationEvents = 'rule-events'

param servicePrincipalObjectId = 'b8e140b1-72ea-4374-84dd-255918df43d7'

param sideCarImageName = 'process-log-sidecar'

param Servicebus = 'Service Bus'
