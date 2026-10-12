"""Deterministic daily fleet reconciliation; does not schedule or ingest data."""
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo
import sqlite3
from pathlib import Path
from contextlib import closing


def reconcile(day, plant_timezone, assets, records, as_of):
    """Reconcile the prior local calendar day at 06:00 on the following day.

    Records describe persisted results, not merely received/scored windows.
    One result establishes presence only, never full signal coverage.
    """
    zone = ZoneInfo(plant_timezone)
    day = date.fromisoformat(day)
    def instant(value):
        result = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if result.tzinfo is None or result.utcoffset() is None:
            raise ValueError('Explicit timezone required')
        return result.astimezone(timezone.utc)
    now = instant(as_of)
    if not assets or len(set(assets)) != len(assets) or any(not isinstance(a,str) or not a.strip() for a in assets):
        raise ValueError('Unique nonblank fleet asset IDs required')
    start = datetime.combine(day, time(), zone).astimezone(timezone.utc)
    end = datetime.combine(day + timedelta(days=1), time(), zone).astimezone(timezone.utc)
    deadline = datetime.combine(day + timedelta(days=1), time(6), zone).astimezone(timezone.utc)
    available, late = set(), set()
    for record in records:
        if record['asset_id'] not in assets:
            raise ValueError('Unknown fleet asset')
        observed, persisted = instant(record['observed_at']), instant(record['persisted_at'])
        if persisted < observed:
            raise ValueError('Persistence predates observation')
        if start <= observed < end and persisted <= now:
            if persisted <= deadline:
                available.add(record['asset_id'])
            else:
                late.add(record['asset_id'])
    return {'requirement_id':'PULSE-NFR-002', 'day':str(day), 'plant_timezone':plant_timezone,
            'deadline_utc':deadline.isoformat(), 'as_of_utc':now.isoformat(),
            'deadline_reached':now >= deadline,
            'assets':[{'asset_id':a,'status':'PRESENT_BY_DEADLINE' if a in available else
                      ('LATE' if a in late else ('MISSING' if now >= deadline else 'PENDING'))} for a in assets],
            'signal_coverage_verified':False, 'scheduled_execution_verified':False}


def reconcile_database(path, tenant, caller, day, plant_timezone, assets, as_of):
    """Read one caller's receipts; do not infer timing for legacy receipts.

    Commit evidence contains an upper bound. A bound after the deadline is
    inconclusive, not proof of a late commit. No database mutations occur.
    """
    if not tenant or not caller:
        raise ValueError('Explicit tenant and caller required')
    report = reconcile(day, plant_timezone, assets, [], as_of)
    known = []
    unknown = set()
    with closing(sqlite3.connect(Path(path).resolve().as_uri()+'?mode=ro', uri=True)) as db:
        db.execute('BEGIN')
        tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        for asset in assets:
            receipts = db.execute('SELECT window FROM api_assessments WHERE tenant=? AND caller=? AND asset=?',
                                  (tenant, caller, asset)).fetchall()
            for (window,) in receipts:
                evidence = None
                if 'assessment_commit_evidence' in tables:
                    evidence = db.execute('''SELECT observed_at, committed_by FROM assessment_commit_evidence
                        WHERE tenant=? AND caller=? AND asset=? AND window=?''',
                        (tenant, caller, asset, window)).fetchone()
                if evidence is None:
                    unknown.add(asset)
                else:
                    known.append({'asset_id':asset,'observed_at':evidence[0],'persisted_at':evidence[1]})
    measured = reconcile(day, plant_timezone, assets, known, as_of)
    for item in measured['assets']:
        if item['status'] == 'LATE':
            item['status'] = 'TIMING_UNCERTAIN'
        elif item['status'] in ('MISSING','PENDING') and item['asset_id'] in unknown:
            item['status'] = 'TIMING_UNKNOWN'
    measured.update(timing_basis='post_commit_upper_bound', tenant=tenant, caller=caller,
                    legacy_timing_unknown_assets=sorted(unknown))
    return measured
