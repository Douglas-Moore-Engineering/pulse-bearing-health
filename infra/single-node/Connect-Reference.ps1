# Run from this checkout. The private key is intentionally excluded from Git.
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$key = Join-Path $root 'outputs/private/pulse-deployment/operator.key'
$known = Join-Path $root 'outputs/private/pulse-deployment/known_hosts'
if (-not (Test-Path -LiteralPath $key)) { throw 'The operator private key is not present in this checkout.' }
Write-Output 'Opening SSH tunnel. Health: http://127.0.0.1:18080/health/ready. Assessment calls require a Pulse Entra token. Ctrl+C closes the tunnel.'
& ssh -i $key -o "UserKnownHostsFile=$known" -o StrictHostKeyChecking=yes -o ExitOnForwardFailure=yes -N -L 127.0.0.1:18080:127.0.0.1:18080 pulseadmin@20.55.240.61
if ($LASTEXITCODE -ne 0) { throw 'SSH tunnel ended with an error.' }
