@secure()
param adminPublicKey string
param operatorCidr string
param adminUsername string = 'pulseadmin'
param location string = 'eastus2'
param vmSize string = 'Standard_D2as_v6'
param zone string = '1'

resource subnet 'Microsoft.Network/virtualNetworks/subnets@2024-05-01' existing = {
  name: 'vnet-pulse-reference/kubernetes-demo'
}
resource nsg 'Microsoft.Network/networkSecurityGroups@2024-05-01' existing = {
  name: 'nsg-pulse-reference'
}
resource sshRule 'Microsoft.Network/networkSecurityGroups/securityRules@2024-05-01' = {
  parent: nsg
  name: 'OperatorSsh'
  properties: {
    priority: 100
    direction: 'Inbound'
    access: 'Allow'
    protocol: 'Tcp'
    sourcePortRange: '*'
    destinationPortRange: '22'
    sourceAddressPrefix: operatorCidr
    destinationAddressPrefix: '*'
  }
}
resource publicIp 'Microsoft.Network/publicIPAddresses@2024-05-01' = {
  name: 'pip-pulse-k3s'
  location: location
  zones: [zone]
  sku: { name: 'Standard' }
  properties: { publicIPAllocationMethod: 'Static' }
  tags: { project: 'pulse', environment: 'reference' }
}
resource nic 'Microsoft.Network/networkInterfaces@2024-05-01' = {
  name: 'nic-pulse-k3s'
  location: location
  properties: {
    ipConfigurations: [{
      name: 'primary'
      properties: {
        primary: true
        privateIPAllocationMethod: 'Dynamic'
        subnet: { id: subnet.id }
        publicIPAddress: { id: publicIp.id }
      }
    }]
  }
}
resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' existing = {
  name: 'id-pulse-reference-client'
}
resource vm 'Microsoft.Compute/virtualMachines@2024-07-01' = {
  name: 'vm-pulse-k3s'
  location: location
  zones: [zone]
  tags: { project: 'pulse', environment: 'reference', monthlyBudgetUsd: '100' }
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: { '${identity.id}': {} }
  }
  properties: {
    hardwareProfile: { vmSize: vmSize }
    securityProfile: {
      securityType: 'TrustedLaunch'
      uefiSettings: { secureBootEnabled: true, vTpmEnabled: true }
    }
    osProfile: {
      computerName: 'pulse-k3s'
      adminUsername: adminUsername
      linuxConfiguration: {
        disablePasswordAuthentication: true
        provisionVMAgent: true
        ssh: {
          publicKeys: [{ path: '/home/${adminUsername}/.ssh/authorized_keys', keyData: adminPublicKey }]
        }
        patchSettings: { patchMode: 'AutomaticByPlatform', assessmentMode: 'AutomaticByPlatform' }
      }
    }
    storageProfile: {
      imageReference: { publisher: 'Canonical', offer: 'ubuntu-24_04-lts', sku: 'server', version: '24.04.202609040' }
      osDisk: {
        name: 'os-pulse-k3s'
        createOption: 'FromImage'
        diskSizeGB: 32
        caching: 'ReadWrite'
        managedDisk: { storageAccountType: 'Premium_LRS' }
        deleteOption: 'Delete'
      }
    }
    networkProfile: { networkInterfaces: [{ id: nic.id, properties: { primary: true } }] }
  }
}
output publicIpAddress string = publicIp.properties.ipAddress
output vmId string = vm.id
