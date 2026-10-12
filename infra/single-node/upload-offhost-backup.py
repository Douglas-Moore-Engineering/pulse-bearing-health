"""Upload a validated local snapshot to a bounded Azure Blob ring using IMDS."""
import hashlib,json,sqlite3,urllib.parse,urllib.request,tempfile
from pathlib import Path
from datetime import datetime,timezone
from contextlib import closing

def upload(account,container,snapshot,client_id,now=None):
    now=now or datetime.now(timezone.utc)
    payload=Path(snapshot).read_bytes()
    if not 0<len(payload)<=50*1024*1024:raise ValueError('Snapshot exceeds size bound')
    with closing(sqlite3.connect(Path(snapshot).resolve().as_uri()+'?mode=ro',uri=True)) as db:
        if db.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise ValueError('Invalid SQLite snapshot')
    query=urllib.parse.urlencode({'api-version':'2018-02-01','resource':'https://storage.azure.com/','client_id':client_id})
    with urllib.request.urlopen(urllib.request.Request('http://169.254.169.254/metadata/identity/oauth2/token?'+query,headers={'Metadata':'true'}),timeout=20) as r:
        token=json.load(r)['access_token']
    # At most 48 objects; replacement is bounded backup rotation, never primary deletion.
    slot=int(now.timestamp()//1800)%48
    name=f'receipts/slot-{slot:02}.db'
    checksum=hashlib.sha256(payload).hexdigest()
    url=f'https://{account}.blob.core.windows.net/{container}/{name}'
    headers={'Authorization':'Bearer '+token,'x-ms-version':'2023-11-03','x-ms-blob-type':'BlockBlob',
             'x-ms-meta-sha256':checksum,'x-ms-meta-created':now.isoformat(),'Content-Type':'application/octet-stream'}
    with urllib.request.urlopen(urllib.request.Request(url,data=payload,headers=headers,method='PUT'),timeout=90) as r:
        if r.status!=201:raise RuntimeError('Upload not confirmed')
    # Read back the stored bytes; a successful PUT alone is not recovery verification.
    with urllib.request.urlopen(urllib.request.Request(url,headers={'Authorization':'Bearer '+token,'x-ms-version':'2023-11-03'}),timeout=90) as r:
        restored=r.read(50*1024*1024+1)
    if hashlib.sha256(restored).hexdigest()!=checksum:raise RuntimeError('Readback checksum mismatch')
    with tempfile.TemporaryDirectory(prefix='pulse-offhost-restore-') as folder:
        recovered=Path(folder)/'restored.db';recovered.write_bytes(restored)
        with closing(sqlite3.connect(recovered)) as db:
            if db.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise RuntimeError('Restored database invalid')
            receipt_count=db.execute('SELECT COUNT(*) FROM api_assessments').fetchone()[0]
    return {'restored_receipt_count':receipt_count,'isolated_restore_integrity':'ok','uploaded_at':now.isoformat(),'blob':name,'bytes':len(payload),'sha256':checksum,
            'off_host':True,'readback_verified':True,'host_loss_rpo_qualified':False}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--config',type=Path,required=True);p.add_argument('--snapshot',type=Path,required=True)
    a=p.parse_args();config=json.loads(a.config.read_text())
    print(json.dumps(upload(snapshot=a.snapshot,**config)))
