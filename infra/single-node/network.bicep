param location string = resourceGroup().location

resource security 'Microsoft.Network/networkSecurityGroups@2024-05-01' = {
  name: 'nsg-pulse-reference'
  location: location
  tags: {
    project: 'pulse'
    environment: 'reference'
  }
  properties: {
    securityRules: [
      {
        name: 'DenyInboundUntilOperatorConfigured'
        properties: {
          priority: 4096
          direction: 'Inbound'
          access: 'Deny'
          protocol: '*'
          sourcePortRange: '*'
          destinationPortRange: '*'
          sourceAddressPrefix: '*'
          destinationAddressPrefix: '*'
        }
      }
    ]
  }
}

resource network 'Microsoft.Network/virtualNetworks@2024-05-01' = {
  name: 'vnet-pulse-reference'
  location: location
  tags: {
    project: 'pulse'
    environment: 'reference'
  }
  properties: {
    addressSpace: {
      addressPrefixes: ['10.87.0.0/16']
    }
    subnets: [
      {
        name: 'kubernetes-demo'
        properties: {
          addressPrefix: '10.87.1.0/24'
          defaultOutboundAccess: false
          networkSecurityGroup: {
            id: security.id
          }
        }
      }
    ]
  }
}

output virtualNetworkId string = network.id
