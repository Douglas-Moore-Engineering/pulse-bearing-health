// Subscription what-if can review a new group without creating it.
targetScope = 'subscription'
param location string = 'eastus2'
param owner string
resource group 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: 'rg-pulse-aks-reference'
  location: location
  tags: { application: 'pulse', environment: 'reference', owner: owner }
}
module foundation './main.bicep' = {
  name: 'pulse-aks-foundation'
  scope: group
  params: { location: location, owner: owner }
}
