"""Authorized Blob read via pinned SSH, followed by isolated local container recovery."""
from contextlib import closing
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import uuid


REMOTE = '''import hashlib,json,sys,urllib.request,urllib.parse
from pathlib import Path
status=json.loads(Path('/var/lib/pulse-ops/backup-status.json').read_text())
config=json.loads(Path('/home/pulseadmin/pulse-release/offhost-backup-config.json').read_text())
backup=status['offhost_result']
query=urllib.parse.urlencode({'api-version':'2018-02-01','resource':'https://storage.azure.com/','client_id':config['client_id']})
with urllib.request.urlopen(urllib.request.Request('http://169.254.169.254/metadata/identity/oauth2/token?'+query,headers={'Metadata':'true'}),timeout=20) as r: token=json.load(r)['access_token']
url='https://'+config['account']+'.blob.core.windows.net/'+config['container']+'/'+backup['blob']
with urllib.request.urlopen(urllib.request.Request(url,headers={'Authorization':'Bearer '+token,'x-ms-version':'2023-11-03'}),timeout=60) as r: payload=r.read(52428801)
assert len(payload)<=52428800 and hashlib.sha256(payload).hexdigest()==backup['sha256']
print(json.dumps({'backup':backup,'source_url':url}),file=sys.stderr)
sys.stdout.buffer.write(payload)
'''


def main():
    root = Path('outputs/private/pulse-deployment').resolve()
    directory = root / ('blob-recovery-' + uuid.uuid4().hex)
    directory.mkdir()
    identity = subprocess.check_output(['whoami'], text=True).strip()
    subprocess.run(['icacls', str(directory), '/inheritance:r', '/grant:r', identity+':(OI)(CI)F'],
                   check=True, capture_output=True)
    ssh = ['ssh', '-i', str(root/'operator.key'), '-o', f'UserKnownHostsFile={root / "known_hosts"}',
           '-o', 'StrictHostKeyChecking=yes', '-o', 'ConnectTimeout=15', 'pulseadmin@20.55.240.61', 'sudo python3 -']
    snapshot = directory/'snapshot.db'
    with snapshot.open('xb') as stream:
        transfer = subprocess.run(ssh, input=REMOTE.encode(), stdout=stream, stderr=subprocess.PIPE,
                                  check=True, timeout=100)
    metadata = json.loads(transfer.stderr.decode())
    checksum = hashlib.sha256(snapshot.read_bytes()).hexdigest()
    assert checksum == metadata['backup']['sha256']
    restored = directory/'assessments.db'
    with closing(sqlite3.connect(snapshot.as_uri()+'?mode=ro', uri=True)) as source, closing(sqlite3.connect(restored)) as target:
        source.backup(target)
        assert target.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
        assert target.execute('PRAGMA foreign_key_check').fetchall() == []
        tables = {row[0] for row in target.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        counts = {name: target.execute(f'SELECT COUNT(*) FROM {name}').fetchone()[0] if name in tables else 0
                  for name in ('api_assessments', 'reference_windows', 'alerts', 'reviews', 'alert_closures')}
    identity_config = json.loads(Path('infra/single-node/identity-config.json').read_text())
    import runpy
    render = runpy.run_path('scripts/render_single_node_manifests.py')['render']
    image = 'pulse-api:sha256-c21a6fd0df51b1e3ca9e90a7b0b7968aab477dc4893430969ed0d854690436c2'
    configuration = next(d['data'] for d in render(image=image, **identity_config, pilot_components=True) if d['kind']=='ConfigMap')
    command = ['docker', 'run', '-d', '--pull=never', '--network=none', '--read-only', '--cap-drop=ALL',
               '--security-opt=no-new-privileges', '--memory=512m', '--cpus=1',
               '--mount', f'type=bind,source={directory},target=/data']
    for key,value in configuration.items(): command.extend(['--env', key+'='+value])
    container = subprocess.check_output(command+[image], text=True, timeout=30).strip()
    try:
        probe = '''import json,sqlite3,time,urllib.request
deadline=time.monotonic()+15
while True:
 try:
  with urllib.request.urlopen('http://127.0.0.1:8000/health/ready',timeout=2) as r: assert r.status==200
  break
 except OSError:
  if time.monotonic()>deadline: raise
  time.sleep(.2)
with sqlite3.connect('file:/data/assessments.db?mode=ro',uri=True) as db:
 assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 tables={row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
 counts={name:db.execute('SELECT COUNT(*) FROM '+name).fetchone()[0] if name in tables else 0 for name in ('api_assessments','reference_windows','alerts','reviews','alert_closures')}
print(json.dumps(counts))
'''
        actual = json.loads(subprocess.check_output(['docker','exec',container,'python','-c',probe], timeout=25))
        assert actual == counts
    finally:
        subprocess.run(['docker','rm','-f',container], check=True, capture_output=True, timeout=20)
    report = {'result':'PASS','observed_at':datetime.now(timezone.utc).isoformat(),
              'source':metadata,'snapshot_sha256':checksum,'counts':counts,'container_image':image,
              'default_command_ready':True,'counts_preserved_after_startup':True,'container_removed':True,
              'tables_absent_in_snapshot':[name for name in counts if name not in tables],
              'live_database_modified':False,'cloud_resources_created':False,
              'limits':'Blob-to-local isolated container recovery; no Azure host-loss RTO/RPO or authenticated workflow verification'}
    Path('governance/evidence/blob-container-recovery.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
