"""Read-only retention planning. No deletion or export implementation."""
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sqlite3


def timestamp(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None: raise ValueError('Timezone required')
    return parsed.astimezone(timezone.utc)


def plan(records, as_of, retention_days):
    if isinstance(retention_days,bool) or not isinstance(retention_days,int) or retention_days<1:
        raise ValueError('Positive integer retention days required')
    now=timestamp(as_of);cutoff=now-timedelta(days=retention_days)
    seen=set();result=[]
    for record in records:
        identity=record.get('id')
        if not isinstance(identity,str) or not identity.strip() or identity in seen:
            raise ValueError('Unique nonblank record IDs required')
        seen.add(identity);reasons=[]
        if record.get('hold') is not False: reasons.append('HOLD_OR_HOLD_UNKNOWN')
        if record.get('review_resolved') is not True: reasons.append('REVIEW_OPEN_OR_UNKNOWN')
        if record.get('dependencies_clear') is not True: reasons.append('DEPENDENCIES_OPEN_OR_UNKNOWN')
        if record.get('export_verified') is not True: reasons.append('EXPORT_NOT_VERIFIED')
        try:
            created=timestamp(record['created_at'])
            if created>now: reasons.append('FUTURE_TIMESTAMP')
            elif created>=cutoff: reasons.append('WITHIN_RETENTION')
        except (KeyError,ValueError,TypeError,AttributeError): reasons.append('INVALID_OR_MISSING_TIMESTAMP')
        result.append({'id':identity,'disposition':'RETAIN' if reasons else 'ELIGIBLE_FOR_OWNER_REVIEW','reasons':reasons})
    return {'dry_run':True,'deletion_authorized':False,'as_of':now.isoformat(),'retention_days':retention_days,'records':result}


def inventory_sqlite(path):
    """Counts only; never read payloads or infer missing receipt timestamps."""
    target=Path(path).resolve(strict=True)
    db=sqlite3.connect(target.as_uri()+'?mode=ro',uri=True)
    try:
        db.execute('PRAGMA query_only=ON')
        tables=[]
        for (name,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchall():
            quoted='"'+name.replace('"','""')+'"'
            tables.append({'table':name,'rows':db.execute('SELECT COUNT(*) FROM '+quoted).fetchone()[0],
                'disposition':'RETAIN','reason':'No verified per-record retention metadata supplied'})
        return {'read_only':True,'deletion_authorized':False,'tables':tables}
    finally: db.close()
