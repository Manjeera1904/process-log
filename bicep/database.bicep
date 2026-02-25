targetScope = 'subscription'

param deploymentPrefix string
param resourceGroupName string
param sqlServerName string
param sqlDBName string
param environmentName string
param clientname string
param managedIdentityName string
param ClientSpecific string 
param TierSql string
param prExpiryDate string

var resourceTagsSql = {
Environment: environmentName
ClientSpecific: ClientSpecific
Tier: TierSql
PRID: environmentName
PRExpireDate: prExpiryDate
}

module sqldb 'modules/sqldb.bicep' = {
  scope: resourceGroup(resourceGroupName)
  name: '${deploymentPrefix}-sqldb'
  params: {
    sqlDBName: sqlDBName
    serverName: sqlServerName
    managedIdentityName: managedIdentityName
    resourceTags: resourceTagsSql
  }
}
