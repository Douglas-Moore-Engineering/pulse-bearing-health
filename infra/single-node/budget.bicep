// Tracking only: no automatic billing cutoff or external notifications.
resource budget 'Microsoft.Consumption/budgets@2024-08-01' = {
  name: 'pulse-monthly-50'
  properties: {
    category: 'Cost'
    amount: 100
    timeGrain: 'Monthly'
    timePeriod: {
      startDate: '2026-10-01T00:00:00Z'
      endDate: '2027-10-01T00:00:00Z'
    }
    notifications: {}
  }
}
