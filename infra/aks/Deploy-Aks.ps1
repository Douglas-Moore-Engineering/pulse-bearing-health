param(
    [Parameter(Mandatory=$true)][string]$Inputs,
    [switch]$Execute
)
$ErrorActionPreference = 'Stop'
$budget = Get-Content -LiteralPath (Join-Path $PSScriptRoot '../../governance/cloud-budget.json') -Raw | ConvertFrom-Json
if ($budget.aksExecutionAllowed -ne $true) {
    throw "AKS deployment disabled by owner budget policy: USD $($budget.monthlyCeiling)/month. Existing proposal exceeds this ceiling. No Azure call performed."
}
$cfg = Get-Content -LiteralPath $Inputs -Raw | ConvertFrom-Json
if ($cfg.approvedMonthlyCeilingUsd -gt $budget.monthlyCeiling) {
    throw 'Input ceiling exceeds the recorded owner budget policy.'
}
function Read-AzJson([string[]]$Arguments) {
    $result = & az @Arguments --output json
    if ($LASTEXITCODE -ne 0) { throw "Azure command failed: $($Arguments[0..1] -join ' ')" }
    return ($result | ConvertFrom-Json)
}
foreach ($field in @('subscriptionId','resourceGroup','location','owner','nodeSku','kubernetesVersion')) {
    if (-not $cfg.$field) { throw "Missing required field: $field" }
}
if ($cfg.resourceGroup -ne 'rg-pulse-aks-reference') { throw 'This increment is scoped to rg-pulse-aks-reference.' }
if ($cfg.location -ne 'eastus2') { throw 'Region changes require refreshed price/quota/network review.' }
$account = Read-AzJson @('account','show')
if ($account.id -ne $cfg.subscriptionId) { throw 'Active subscription differs from reviewed inputs.' }
$cli = Read-AzJson @('version')
if ([version]$cli.'azure-cli' -lt [version]'2.86.0') { throw 'Managed Gateway API requires Azure CLI >=2.86.0.' }
$skus = Read-AzJson @('vm','list-skus','--location',$cfg.location,'--size',$cfg.nodeSku,'--all')
$sku = @($skus | Where-Object { $_.name -eq $cfg.nodeSku })
if ($sku.Count -ne 1 -or @($sku[0].restrictions).Count -gt 0) { throw 'Node size is unavailable/restricted for this subscription.' }
$usage = Read-AzJson @('vm','list-usage','--location',$cfg.location)
$regional = $usage | Where-Object { $_.name.value -eq 'cores' }
$family = $usage | Where-Object { $_.name.value -ieq $sku[0].family }
foreach ($quota in @($regional,$family)) {
    if (-not $quota -or ([int]$quota.limit - [int]$quota.currentValue) -lt 44) {
        throw 'Need 44 free regional and selected-family vCPUs for pool maxima and two surge nodes.'
    }
}
if (-not $Execute) {
    Write-Output 'Read-only preflight passed. No provisioning performed.'
    return
}
# The values below must record the actual owner's decision, never an inferred fictional budget.
if (-not $cfg.spendingApprovedBy -or $cfg.approvedMonthlyCeilingUsd -le 0 -or
    $cfg.reviewedMonthlyEstimateUsd -le 0 -or $cfg.approvedMonthlyCeilingUsd -lt $cfg.reviewedMonthlyEstimateUsd) {
    throw 'A reviewed full estimate and sufficient owner-authorized spending ceiling are required.'
}
if (-not $cfg.privateOperatorPathValidated) { throw 'Private deployment/operator network path is required.' }
$rg = Read-AzJson @('group','create','--name',$cfg.resourceGroup,'--location',$cfg.location)
$parameters = @("location=$($cfg.location)","owner=$($cfg.owner)","nodeSku=$($cfg.nodeSku)","kubernetesVersion=$($cfg.kubernetesVersion)")
$template = Join-Path $PSScriptRoot 'main.bicep'
& az deployment group validate --resource-group $cfg.resourceGroup --template-file $template --parameters @parameters
if ($LASTEXITCODE -ne 0) { throw 'ARM validation failed.' }
& az deployment group what-if --resource-group $cfg.resourceGroup --template-file $template --parameters @parameters
if ($LASTEXITCODE -ne 0) { throw 'ARM what-if failed.' }
# Explicit -Execute is authorization to create the reviewed reference foundation, not a model release.
& az deployment group create --resource-group $cfg.resourceGroup --name pulse-aks-foundation --template-file $template --parameters @parameters
if ($LASTEXITCODE -ne 0) { throw 'Foundation deployment failed; retain diagnostics and inspect partial resources.' }
& az aks update --resource-group $cfg.resourceGroup --name pulse-aks --enable-gateway-api --enable-app-routing-istio
if ($LASTEXITCODE -ne 0) { throw 'Managed Gateway API setup failed.' }
Write-Output 'Foundation created. Continue identity, image, private TLS and application rollout checks in README.md.'
