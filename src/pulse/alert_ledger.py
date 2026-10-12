"""Durable alert-event and acknowledgement component; no detector or transport.

Caller authorization and detector qualification belong to the integrating service.
This component is exercised offline only and is not enabled in the deployed API.
"""
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sqlite3


class AlertConflict(ValueError):
    pass


class AlertLedger:
    def __init__(self, path):
        if str(path) == ':memory:':
            raise ValueError('Durable alert storage requires a file')
        self.path = str(Path(path).resolve())
        with self.connection() as db:
            db.execute('PRAGMA journal_mode=WAL')
            db.execute('''CREATE TABLE IF NOT EXISTS alerts (
                event_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, asset TEXT NOT NULL,
                episode TEXT NOT NULL, policy TEXT NOT NULL, payload TEXT NOT NULL,
                created TEXT NOT NULL, acknowledged_by TEXT, acknowledged_at TEXT,
                UNIQUE(tenant,asset,episode,policy))''')
            db.execute('''CREATE TABLE IF NOT EXISTS alert_delivery_attempts (
                attempt_id TEXT PRIMARY KEY, event_id TEXT NOT NULL REFERENCES alerts(event_id),
                destination TEXT NOT NULL, outcome TEXT NOT NULL, recorded_at TEXT NOT NULL)''')

    @contextmanager
    def connection(self):
        db = sqlite3.connect(self.path, timeout=5)
        db.row_factory = sqlite3.Row
        try:
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('PRAGMA synchronous=FULL')
            with db:
                yield db
        finally:
            db.close()

    def record(self, tenant, asset, episode, policy, payload):
        if any(not isinstance(x, str) or not x or len(x) > 256 for x in (tenant, asset, episode, policy)):
            raise ValueError('Explicit bounded tenant, asset, episode and policy IDs required')
        encoded = json.dumps(payload, sort_keys=True, separators=(',', ':'), allow_nan=False)
        if len(encoded.encode()) > 16384:
            raise ValueError('Alert evidence exceeds 16 KiB')
        event_id = hashlib.sha256(json.dumps([tenant, asset, episode, policy]).encode()).hexdigest()
        with self.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            previous = db.execute('SELECT payload FROM alerts WHERE event_id=?', (event_id,)).fetchone()
            if previous:
                if previous['payload'] != encoded:
                    raise AlertConflict('Episode evidence changed; create a new version explicitly')
                return event_id
            db.execute('INSERT INTO alerts VALUES(?,?,?,?,?,?,?,NULL,NULL)',
                       (event_id, tenant, asset, episode, policy, encoded, datetime.now(timezone.utc).isoformat()))
        return event_id

    def acknowledge(self, tenant, asset, event_id, actor):
        if not isinstance(actor, str) or not actor or len(actor) > 256:
            raise ValueError('Acknowledgement requires an authenticated actor ID')
        with self.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT * FROM alerts WHERE event_id=? AND tenant=? AND asset=?',
                             (event_id, tenant, asset)).fetchone()
            if row is None:
                raise KeyError('Alert not found in this tenant and asset')
            if row['acknowledged_by'] is not None:
                if row['acknowledged_by'] != actor:
                    raise AlertConflict('An existing acknowledgement cannot be overwritten')
                return dict(row)
            db.execute('UPDATE alerts SET acknowledged_by=?, acknowledged_at=? WHERE event_id=?',
                       (actor, datetime.now(timezone.utc).isoformat(), event_id))
            return dict(db.execute('SELECT * FROM alerts WHERE event_id=?', (event_id,)).fetchone())

    def record_delivery_attempt(self, tenant, asset, event_id, attempt_id, destination, outcome):
        # This records a transport's result; it does not send messages or infer success.
        if outcome not in ('failed', 'delivered', 'unknown'):
            raise ValueError('Explicit transport outcome required')
        if any(not isinstance(x, str) or not x or len(x) > 256 for x in (attempt_id, destination)):
            raise ValueError('Bounded attempt and destination identifiers required')
        with self.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            if not db.execute('SELECT 1 FROM alerts WHERE event_id=? AND tenant=? AND asset=?',
                              (event_id, tenant, asset)).fetchone():
                raise KeyError('Alert not found in this tenant and asset')
            previous = db.execute('SELECT * FROM alert_delivery_attempts WHERE attempt_id=?', (attempt_id,)).fetchone()
            if previous:
                if (previous['event_id'], previous['destination'], previous['outcome']) != (event_id, destination, outcome):
                    raise AlertConflict('Delivery attempt ID was reused with different content')
                return
            db.execute('INSERT INTO alert_delivery_attempts VALUES(?,?,?,?,?)',
                       (attempt_id, event_id, destination, outcome, datetime.now(timezone.utc).isoformat()))
