using 'database.bicep'

param environmentName =  ''

param TierSql = 'Database'

param prExpiryDate = ''

param ClientSpecific = 'Yes'

param clientname = ''

param sqlDBName =  'ProcessLog_${clientname}'

param sqlServerName = 'sseclipsesaas${environmentName}'

param deploymentPrefix = 'deploy-${environmentName}'

var projectName =  'eclipsesaas'

param resourceGroupName = '${projectName}-${environmentName}-rg'

param managedIdentityName =  'uaid-${projectName}-${environmentName}'
