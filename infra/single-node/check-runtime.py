"""Bounded host-local reference health snapshot; never an external notification."""
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys
import urllib.request


checks = {}
try:
    with urllib.request.urlopen('http://127.0.0.1:18080/health/ready', timeout=10) as response:
        checks['api_ready'] = json.load(response).get('status') == 'ready'
except Exception:
    checks['api_ready'] = False
try:
    result = subprocess.run(['/usr/local/bin/k3s', 'kubectl', '-n', 'pulse', 'get',
        'deployment', 'pulse-api', '-o', 'json'], capture_output=True, text=True,
        timeout=15, check=True)
    deployment = json.loads(result.stdout)
    checks['replica_ready'] = deployment.get('status', {}).get('readyReplicas', 0) == 1
except Exception:
    checks['replica_ready'] = False
disk = shutil.disk_usage('/var/lib/rancher/k3s')
checks['disk_reserve'] = disk.free >= max(2*1024**3, disk.total*.20)
try:
    backup = json.loads(Path('/var/lib/pulse-ops/backup-status.json').read_text())
    observed = datetime.strptime(backup['observed_at'], '%Y%m%dT%H%M%SZ').replace(tzinfo=timezone.utc)
    age = (datetime.now(timezone.utc)-observed).total_seconds()
    checks['offhost_backup_verified'] = backup.get('off_host') is True and backup.get('offhost_result',{}).get('readback_verified') is True
    checks['recent_local_backup'] = backup['integrity'] == 'ok' and 0 <= age <= 45*60
except Exception:
    checks['recent_local_backup'] = False
try:
    reconciliation = json.loads(Path('/var/lib/pulse-ops/reconciliation/latest.json').read_text())
    age = (datetime.now(timezone.utc)-datetime.fromisoformat(reconciliation['executed_at'])).total_seconds()
    checks['recent_reconciliation'] = 0 <= age <= 26*3600
    failed = subprocess.run(['systemctl', 'is-failed', 'pulse-reconciliation.service'],
                            capture_output=True, text=True, timeout=5)
    checks['reconciliation_service'] = failed.stdout.strip() != 'failed'
except Exception:
    checks['recent_reconciliation'] = False
report = {'observed_at': datetime.now(timezone.utc).isoformat(), 'checks': checks,
          'status': 'healthy' if all(checks.values()) else 'attention_required',
          'disk_free_bytes': disk.free, 'disk_total_bytes': disk.total,
          'threshold_basis': 'Provisional operator threshold: 20 percent or 2 GiB free, whichever is larger',
          'external_notification_sent': False, 'detector_quality_checked': False}
root = Path('/var/lib/pulse-ops')
root.mkdir(mode=0o700, exist_ok=True)
temporary = root/'health.json.tmp'
temporary.write_text(json.dumps(report, indent=2)+'\n')
temporary.replace(root/'health.json')
print(json.dumps(report))
sys.exit(0 if all(checks.values()) else 1)
