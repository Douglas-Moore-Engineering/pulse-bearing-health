// Explicitly bounded AKS Standard pools; not provisioned by compiling this file.
targetScope = 'resourceGroup'
param location string = 'eastus2'
param prefix string = 'pulse'
param owner string
param kubernetesVersion string = '1.36.4'
param nodeSku string = 'Standard_D4ds_v6'
param tenantId string = tenant().tenantId
@description('Approved network plan; requires private operator connectivity.')
param vnetCidr string = '10.86.0.0/16'
param nodeSubnetCidr string = '10.86.0.0/20'
param endpointSubnetCidr string = '10.86.16.0/24'
var tags = { application: 'pulse', environment: 'reference', owner: owner, costModel: 'PULSE-LCC-001' }
var suffix = uniqueString(resourceGroup().id)
resource network 'Microsoft.Network/virtualNetworks@2024-05-01' = {
  name: '${prefix}-aks-vnet'
  location: location
  tags: tags
  properties: {
    addressSpace: { addressPrefixes: [vnetCidr] }
    subnets: [
      { name: 'nodes', properties: { addressPrefix: nodeSubnetCidr } }
      { name: 'endpoints', properties: { addressPrefix: endpointSubnetCidr, privateEndpointNetworkPolicies: 'Disabled' } }
    ]
  }
}
resource control 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: '${prefix}-aks-control'
  location: location
  tags: tags
}
resource networkRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(network.id, control.id, 'network-contributor')
  scope: network
  properties: {
    principalId: control.properties.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4d97b98b-1d4f-4787-a291-c67834d212e7')
  }
}
resource logs 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: '${prefix}-aks-logs'
  location: location
  tags: tags
  properties: { sku: { name: 'PerGB2018' }, retentionInDays: 30, workspaceCapping: { dailyQuotaGb: 2 } }
}
resource registry 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: 'pulse${suffix}'
  location: location
  tags: tags
  sku: { name: 'Premium' }
  properties: { adminUserEnabled: false, publicNetworkAccess: 'Disabled', policies: { quarantinePolicy: { status: 'disabled' } } }
}
resource registryDns 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: 'privatelink.azurecr.io'
  location: 'global'
}
resource registryLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = {
  parent: registryDns
  name: 'aks-link'
  location: 'global'
  properties: { registrationEnabled: false, virtualNetwork: { id: network.id } }
}
resource registryEndpoint 'Microsoft.Network/privateEndpoints@2024-05-01' = {
  name: '${prefix}-acr-pe'
  location: location
  properties: {
    subnet: { id: resourceId('Microsoft.Network/virtualNetworks/subnets', network.name, 'endpoints') }
    privateLinkServiceConnections: [{ name: 'registry', properties: { privateLinkServiceId: registry.id, groupIds: ['registry'] } }]
  }
}
resource registryZoneGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2024-05-01' = {
  parent: registryEndpoint
  name: 'default'
  properties: { privateDnsZoneConfigs: [{ name: 'registry', properties: { privateDnsZoneId: registryDns.id } }] }
}
resource cluster 'Microsoft.ContainerService/managedClusters@2025-10-01' = {
  name: '${prefix}-aks'
  location: location
  tags: tags
  sku: { name: 'Base', tier: 'Standard' }
  identity: { type: 'UserAssigned', userAssignedIdentities: { '${control.id}': {} } }
  properties: {
    kubernetesVersion: kubernetesVersion
    dnsPrefix: '${prefix}-${suffix}'
    enableRBAC: true
    disableLocalAccounts: true
    aadProfile: { managed: true, enableAzureRBAC: true, tenantID: tenantId }
    apiServerAccessProfile: { enablePrivateCluster: true, enablePrivateClusterPublicFQDN: false }
    oidcIssuerProfile: { enabled: true }
    securityProfile: { workloadIdentity: { enabled: true }, defender: { logAnalyticsWorkspaceResourceId: logs.id, securityMonitoring: { enabled: true } } }
    autoUpgradeProfile: { upgradeChannel: 'patch', nodeOSUpgradeChannel: 'NodeImage' }
    networkProfile: {
      networkPlugin: 'azure'
      networkPluginMode: 'overlay'
      networkDataplane: 'cilium'
      loadBalancerSku: 'standard'
      outboundType: 'loadBalancer'
      podCidr: '10.244.0.0/16'
      serviceCidr: '10.245.0.0/16'
      dnsServiceIP: '10.245.0.10'
    }
    addonProfiles: {
      azurepolicy: { enabled: true }
      omsagent: { enabled: true, config: { logAnalyticsWorkspaceResourceID: logs.id, useAADAuth: 'true' } }
      azureKeyvaultSecretsProvider: { enabled: true, config: { enableSecretRotation: 'true' } }
    }
    agentPoolProfiles: [
      {
        name: 'system'
        mode: 'System'
        count: 3
        vmSize: nodeSku
        osType: 'Linux'
        osSKU: 'AzureLinux'
        osDiskType: 'Managed'
        osDiskSizeGB: 128
        type: 'VirtualMachineScaleSets'
        availabilityZones: ['1', '2', '3']
        nodeTaints: ['CriticalAddonsOnly=true:NoSchedule']
        vnetSubnetID: resourceId('Microsoft.Network/virtualNetworks/subnets', network.name, 'nodes')
        upgradeSettings: { maxSurge: '1' }
        maxPods: 50
      }
      {
        name: 'api'
        mode: 'User'
        count: 3
        minCount: 3
        maxCount: 6
        enableAutoScaling: true
        vmSize: nodeSku
        osType: 'Linux'
        osSKU: 'AzureLinux'
        osDiskType: 'Managed'
        osDiskSizeGB: 128
        type: 'VirtualMachineScaleSets'
        availabilityZones: ['1', '2', '3']
        nodeLabels: { workload: 'pulse-api' }
        vnetSubnetID: resourceId('Microsoft.Network/virtualNetworks/subnets', network.name, 'nodes')
        upgradeSettings: { maxSurge: '1' }
        maxPods: 50
      }
    ]
  }
  dependsOn: [networkRole]
}
resource pullRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(registry.id, cluster.id, 'acr-pull')
  scope: registry
  properties: {
    principalId: cluster.properties.identityProfile.kubeletidentity.objectId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')
  }
}
resource diagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: 'control-plane'
  scope: cluster
  properties: { workspaceId: logs.id, logs: [{ category: 'kube-audit-admin', enabled: true }, { category: 'kube-apiserver', enabled: true }] }
}
output clusterName string = cluster.name
output registryHost string = registry.properties.loginServer
output oidcIssuer string = cluster.properties.oidcIssuerProfile.issuerURL
output logWorkspaceId string = logs.id
