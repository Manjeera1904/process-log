param dnsZoneName string
param cnameRecordName string
param ttl int
param cnameTargetFqdn string
param txtRecordName string = 'asuid'
param txtValue string

resource cname 'Microsoft.Network/dnsZones/CNAME@2018-05-01' = {
  parent: dnsZone
  name: cnameRecordName
  properties: {
    CNAMERecord: {
      cname: cnameTargetFqdn
    }
    TTL: ttl
  }
}

resource dnsZone 'Microsoft.Network/dnsZones@2018-05-01' = {
  name: dnsZoneName
  location: 'global'
}

resource txtRecord 'Microsoft.Network/dnsZones/TXT@2023-07-01-preview' = {
  parent: dnsZone
  name: txtRecordName
  properties: {
    TXTRecords: [
      {
        value: [
          txtValue
        ]
      }
    ]
    TTL: ttl
  }
}
