// Reference foundation only. Compile/what-if and account-specific review required.
targetScope = 'resourceGroup'

@description('Explicitly approved Azure region; no automatic account selection.')
param location string
@minLength(3)
@maxLength(12)
param prefix string = 'pulse'
@allowed(['reference'])
param environment string = 'reference'
@description('Accountable owner tag. Not an identity or role assignment.')
@minLength(1)
param owner string
@description('Must not overlap the approved private operator network.')
param vnetAddressPrefix string = '10.84.0.0/24'
param privateEndpointSubnetPrefix string = '10.84.0.0/27'

var suffix = uniqueString(resourceGroup().id)
var tags = { application: 'pulse', environment: environment, owner: owner, exposure: 'reference-only' }

resource network 'Microsoft.Network/virtualNetworks@2024-05-01' = {
  name: '${prefix}-${environment}-vnet'
  location: location
  tags: tags
  properties: {
    addressSpace: { addressPrefixes: [vnetAddressPrefix] }
    subnets: [{ name: 'private-endpoints', properties: { addressPrefix: privateEndpointSubnetPrefix, privateEndpointNetworkPolicies: 'Disabled' } }]
  }
}
var subnetId = resourceId('Microsoft.Network/virtualNetworks/subnets', network.name, 'private-endpoints')

resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: 'st${suffix}'
  location: location
  tags: tags
  kind: 'StorageV2'
  sku: { name: 'Standard_LRS' }
  properties: {
    allowBlobPublicAccess: false
    allowSharedKeyAccess: false
    defaultToOAuthAuthentication: true
    publicNetworkAccess: 'Disabled'
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
    networkAcls: { defaultAction: 'Deny', bypass: 'None' }
  }
}
resource blobs 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = {
  parent: storage
  name: 'default'
  properties: {
    isVersioningEnabled: true
    deleteRetentionPolicy: { enabled: true, days: 7 }
    containerDeleteRetentionPolicy: { enabled: true, days: 7 }
  }
}
resource containers 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = [for layer in ['bronze', 'silver', 'gold', 'evidence']: {
  parent: blobs
  name: layer
  properties: { publicAccess: 'None' }
}]

resource vault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: 'kv-${suffix}'
  location: location
  tags: tags
  properties: {
    tenantId: tenant().tenantId
    sku: { family: 'A', name: 'standard' }
    enableRbacAuthorization: true
    enableSoftDelete: true
    enablePurgeProtection: true
    softDeleteRetentionInDays: 7
    publicNetworkAccess: 'Disabled'
    networkAcls: { defaultAction: 'Deny', bypass: 'None' }
  }
}

resource logs 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: '${prefix}-${environment}-logs'
  location: location
  tags: tags
  properties: {
    sku: { name: 'PerGB2018' }
    retentionInDays: 30
    workspaceCapping: { dailyQuotaGb: json('0.1') }
    features: { disableLocalAuth: true }
  }
}
resource insights 'Microsoft.Insights/components@2020-02-02' = {
  name: '${prefix}-${environment}-insights'
  location: location
  kind: 'web'
  tags: tags
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logs.id
    DisableLocalAuth: true
    publicNetworkAccessForIngestion: 'Disabled'
    publicNetworkAccessForQuery: 'Disabled'
  }
}

resource workspace 'Microsoft.MachineLearningServices/workspaces@2025-12-01' = {
  name: '${prefix}-${environment}-ml'
  location: location
  tags: tags
  identity: { type: 'SystemAssigned' }
  sku: { name: 'Basic', tier: 'Basic' }
  properties: {
    friendlyName: 'Pulse isolated reference'
    description: 'Unvalidated for customer site; no training or serving compute provisioned.'
    storageAccount: storage.id
    keyVault: vault.id
    applicationInsights: insights.id
    publicNetworkAccess: 'Disabled'
    allowPublicAccessWhenBehindVnet: false
    systemDatastoresAuthMode: 'Identity'
    managedNetwork: { isolationMode: 'AllowOnlyApprovedOutbound' }
  }
}

var privateServices = [
  { name: 'blob', resource: storage.id, group: 'blob', zones: ['privatelink.blob.${az.environment().suffixes.storage}'] }
  { name: 'file', resource: storage.id, group: 'file', zones: ['privatelink.file.${az.environment().suffixes.storage}'] }
  { name: 'vault', resource: vault.id, group: 'vault', zones: ['privatelink.vaultcore.azure.net'] }
  { name: 'ml', resource: workspace.id, group: 'amlworkspace', zones: ['privatelink.api.azureml.ms', 'privatelink.notebooks.azure.net'] }
]
var zoneNames = ['privatelink.blob.${az.environment().suffixes.storage}', 'privatelink.file.${az.environment().suffixes.storage}', 'privatelink.vaultcore.azure.net', 'privatelink.api.azureml.ms', 'privatelink.notebooks.azure.net']
resource zones 'Microsoft.Network/privateDnsZones@2020-06-01' = [for zone in zoneNames: {
  name: zone
  location: 'global'
  tags: tags
}]
resource zoneLinks 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = [for (zone, i) in zoneNames: {
  parent: zones[i]
  name: 'pulse-link'
  location: 'global'
  properties: { registrationEnabled: false, virtualNetwork: { id: network.id } }
}]
resource endpoints 'Microsoft.Network/privateEndpoints@2024-05-01' = [for service in privateServices: {
  name: '${prefix}-${service.name}-pe'
  location: location
  tags: tags
  properties: {
    subnet: { id: subnetId }
    privateLinkServiceConnections: [{
      name: '${service.name}-connection'
      properties: { privateLinkServiceId: service.resource, groupIds: [service.group] }
    }]
  }
}]
resource endpointDns 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2024-05-01' = [for (service, i) in privateServices: {
  parent: endpoints[i]
  name: 'default'
  properties: {
    privateDnsZoneConfigs: [for zone in service.zones: { name: replace(zone, '.', '-'), properties: { privateDnsZoneId: resourceId('Microsoft.Network/privateDnsZones', zone) } }]
  }
  dependsOn: [zones]
}]

output workspaceId string = workspace.id
output storageId string = storage.id
output vaultId string = vault.id
output privateNetworkId string = network.id
output workspacePrincipalId string = workspace.identity.principalId
