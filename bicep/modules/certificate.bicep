param location string
param customDomainName string
param customAppName string
param certificateName string

@description('The name of the Container App Environment')
param containerAppEnvironmentName string

resource managedEnvironment 'Microsoft.App/managedEnvironments@2023-11-02-preview' existing = {
  name: containerAppEnvironmentName
}

resource managedEnvironmentManagedCertificate 'Microsoft.App/managedEnvironments/managedCertificates@2022-11-01-preview' = {
  parent: managedEnvironment
  name: '${certificateName}-${customAppName}'
  location: location
  properties: {
    subjectName: customDomainName
    domainControlValidation: 'CNAME'
  }
}

output managedCertificateId string = managedEnvironmentManagedCertificate.id
