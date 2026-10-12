"""Half-hourly bounded on-host SQLite snapshots; not a host-loss recovery substitute."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess

root = Path('/var/lib/pulse-ops/backups')
root.mkdir(mode=0o700, parents=True, exist_ok=True)
stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
target = root/f'receipts-{stamp}.db'
partial = root/f'receipts-{stamp}.partial'
code = '''import os,sqlite3,sys,tempfile
source=sqlite3.connect("file:/data/assessments.db?mode=ro",uri=True)
pages=source.execute("PRAGMA page_count").fetchone()[0]
size=source.execute("PRAGMA page_size").fetchone()[0]
if pages*size>52428800: raise RuntimeError("Backup size bound exceeded; operator action required")
fd,path=tempfile.mkstemp(prefix="pulse-snapshot-",dir="/data")
os.close(fd)
try:
 target=sqlite3.connect(path)
 source.backup(target)
 target.close()
 if os.path.getsize(path)>52428800: raise RuntimeError("Backup size bound exceeded")
 with open(path,"rb") as stream: sys.stdout.buffer.write(stream.read())
finally:
 source.close()
 os.unlink(path)
'''
try:
    with partial.open('xb') as stream:
        os.chmod(partial, 0o600)
        subprocess.run(['/usr/local/bin/k3s', 'kubectl', '-n', 'pulse', 'exec',
            'deployment/pulse-api', '--', 'python', '-c', code], stdout=stream, check=True, timeout=120)
    db = sqlite3.connect(f'file:{partial}?mode=ro', uri=True)
    try:
        if db.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
            raise RuntimeError('Snapshot integrity failed')
        rows = db.execute('SELECT COUNT(*) FROM api_assessments').fetchone()[0]
    finally:
        db.close()
    partial.replace(target)
finally:
    partial.unlink(missing_ok=True)
# Prune only this tool's timestamped backups, never the live database or other files.
backups = sorted(p for p in root.iterdir() if p.is_file() and not p.is_symlink()
                 and re.fullmatch(r'receipts-\d{8}T\d{6}Z\.db', p.name))
for old in backups[:-48]:
    old.unlink()
report = {'observed_at': stamp, 'integrity': 'ok', 'receipt_count': rows,
          'backup_sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
          'bytes': target.stat().st_size, 'retained_snapshots': min(48, len(backups)),
          'maximum_snapshot_bytes': 52428800, 'maximum_retained_snapshots': 48, 'off_host': False, 'external_notification_sent': False}
(root.parent/'backup-status.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report))
