using 'main.bicep'

param azureContainerRegistryImageTag = ''

param projectName = 'eclipsesaas'

param environmentName = ''

param ClientSpecific = 'No'

param TierWeb = 'Web App'

param TechStackWeb = 'React 18.2'

param TechStackApi = 'DotNet 8.0'

param TierAPI = 'API'

param serviceBusNamespace = 'asb-${projectName}-${environmentName}'

param userAssignedManagedIdentityName = 'uaid-${projectName}-${environmentName}'

param azureContainerRegistryWebImageName = 'process-logging-web'

param azureContainerRegistryAPIImageName = 'process-logging-api'

param dnsZoneName = 'eclipsevantage.com'

param commonRGName = '${projectName}-common-rg'

param keyVaultName = 'kv-${projectName}-${environmentName}'

param azureContainerRegistry = '${projectName}acr'

param azureContainerWebAppName = 'aca-process-logging-web-${environmentName}'

param azureContainerAPIName = 'aca-process-logging-api-${environmentName}'

param deploymentPrefix = 'deploy-${environmentName}'

param resourceGroupName = '${projectName}-${environmentName}-rg'

param containerAppEnvironmentName = 'cae-${projectName}-${environmentName}'

param customDomainNameWeb = '${azureContainerRegistryWebImageName}.${environmentName}.${dnsZoneName}'

param customDomainNameAPI = '${azureContainerRegistryAPIImageName}.${environmentName}.${dnsZoneName}'

param azureContainerWebFdqn = 'aca-${azureContainerRegistryWebImageName}'

param azureContainerAPIFdqn = 'aca-${azureContainerRegistryAPIImageName}'

param location = 'East US'

param webCertificateName = 'cae-eclipsesaas-${environmentName}-${azureContainerWebAppName}'

param apiCertificateName = 'cae-eclipsesaas-${environmentName}-${azureContainerAPIName}'

param keyVaultUrl = 'vault.azure.net'

param sideCarImageName = 'process-log-sidecar'
