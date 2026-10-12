targetScope = 'subscription'

@description('Metadata location for the isolated reference resource group.')
param location string = 'eastus2'

resource group 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: 'rg-pulse-reference'
  location: location
  tags: {
    project: 'pulse'
    environment: 'reference'
    monthlyBudgetUsd: '100'
    owner: 'DrMoore'
  }
}

module budget 'budget.bicep' = {
  name: 'pulse-cost-budget'
  scope: group
}

module network 'network.bicep' = {
  name: 'pulse-reference-network'
  scope: group
  params: {
    location: location
  }
}

output resourceGroupId string = group.id
