"""Take an online SQLite backup over pinned SSH and verify an isolated restore.

The private backup stays off the Azure host. Never overwrite the live database.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shlex
import sqlite3
import subprocess
import tempfile


REMOTE = '''import os,sqlite3,sys,tempfile
fd,path=tempfile.mkstemp(prefix="pulse-backup-",suffix=".db",dir="/data")
os.close(fd)
try:
 source=sqlite3.connect("file:/data/assessments.db?mode=ro",uri=True)
 target=sqlite3.connect(path)
 source.backup(target)
 target.close()
 source.close()
 if os.path.getsize(path)>52428800:
  raise RuntimeError("Backup exceeds the 50 MiB operator-transfer bound")
 with open(path,"rb") as stream:
  sys.stdout.buffer.write(stream.read())
finally:
 os.unlink(path)
'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='pulseadmin@20.55.240.61')
    parser.add_argument('--private-dir', type=Path, default=Path('outputs/private/pulse-deployment'))
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--minimum-reviews', type=int, default=0)
    args = parser.parse_args()
    root = args.private_dir.resolve()
    if not (root/'operator.key').is_file() or not (root/'known_hosts').is_file():
        raise ValueError('Pinned operator key and known_hosts required')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    output = root/f'receipts-{stamp}.db'
    ssh = ['ssh', '-i', str(root/'operator.key'), '-o', f'UserKnownHostsFile={root / "known_hosts"}',
           '-o', 'StrictHostKeyChecking=yes', args.host]
    command = 'sudo k3s kubectl -n pulse exec deployment/pulse-api -- python -c '+shlex.quote(REMOTE)
    with output.open('xb') as stream:
        if os.name == 'nt':
            identity = subprocess.check_output(['whoami'], text=True).strip()
            subprocess.run(['icacls', str(output), '/inheritance:r', '/grant:r', identity+':(F)'],
                           capture_output=True, check=True)
        else:
            output.chmod(0o600)
        subprocess.run(ssh+[command], stdout=stream, check=True, timeout=120)
    checksum = hashlib.sha256(output.read_bytes()).hexdigest()
    # Restore to an independent database, never to the live PVC.
    with tempfile.TemporaryDirectory(prefix='pulse-restore-', dir=root) as folder:
        restored = Path(folder)/'restored.db'
        source = sqlite3.connect(f'file:{output.as_posix()}?mode=ro', uri=True)
        target = sqlite3.connect(restored)
        try:
            source.backup(target)
            integrity = target.execute('PRAGMA integrity_check').fetchone()[0]
            rows = target.execute('SELECT COUNT(*) FROM api_assessments').fetchone()[0]
            invalid = target.execute('SELECT response FROM api_assessments').fetchall()
            if integrity != 'ok' or any(not json.loads(row[0]).get('persisted') for row in invalid):
                raise ValueError('Restored receipt validation failed')
            tables = {row[0] for row in target.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            reference_windows = target.execute('SELECT COUNT(*) FROM reference_windows').fetchone()[0] if 'reference_windows' in tables else 0
            alerts = target.execute('SELECT COUNT(*) FROM alerts').fetchone()[0] if 'alerts' in tables else 0
            acknowledgements = target.execute('SELECT COUNT(*) FROM alerts WHERE acknowledged_by IS NOT NULL').fetchone()[0] if 'alerts' in tables else 0
            review_rows = target.execute('SELECT * FROM reviews ORDER BY rowid').fetchall() if 'reviews' in tables else []
            original_reviews = source.execute('SELECT * FROM reviews ORDER BY rowid').fetchall() if 'reviews' in tables else []
            if review_rows != original_reviews or len(review_rows) < args.minimum_reviews:
                raise ValueError('Restored review history differs or required reviews are absent')
            if target.execute('PRAGMA foreign_key_check').fetchall():
                raise ValueError('Restored database has broken foreign-key references')
        finally:
            target.close()
            source.close()
    report = {'executed_at': stamp, 'online_backup': True, 'off_host_copy': True,
              'isolated_restore_integrity': integrity, 'receipt_count': rows,
              'backup_sha256': checksum, 'bytes': output.stat().st_size,
              'reference_windows': reference_windows, 'alert_episodes': alerts,
              'acknowledged_episodes': acknowledgements,
              'review_count': len(review_rows), 'review_history_matches_backup': review_rows == original_reviews,
              'nonempty_review_recovery_tested': bool(review_rows),
              'live_database_replaced': False, 'scheduled_backup': False,
              'limits': 'Manual operator backup; no disaster RTO/RPO or automated retention claimed'}
    args.evidence.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
