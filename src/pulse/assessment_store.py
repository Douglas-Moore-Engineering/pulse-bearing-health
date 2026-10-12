"""Single-node durable assessment receipts; deliberately not a notification system."""
from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from datetime import datetime, timezone


class WindowConflict(Exception):
    """An already accepted window was submitted with different content."""


class AssessmentStore:
    def __init__(self, path: str):
        if path == ':memory:':
            raise ValueError('Durable assessment storage requires a file')
        self.path = str(Path(path).resolve())
        if not Path(self.path).parent.is_dir():
            raise ValueError('Assessment directory must already exist')
        with self.connect() as db:
            db.execute('PRAGMA journal_mode=WAL')
            db.execute('''CREATE TABLE IF NOT EXISTS api_assessments (
                tenant TEXT NOT NULL, caller TEXT NOT NULL, asset TEXT NOT NULL,
                window TEXT NOT NULL, request_sha TEXT NOT NULL, response TEXT NOT NULL,
                PRIMARY KEY (tenant, caller, asset, window))''')
            db.execute('''CREATE TABLE IF NOT EXISTS assessment_commit_evidence (
                tenant TEXT NOT NULL, caller TEXT NOT NULL, asset TEXT NOT NULL,
                window TEXT NOT NULL, observed_at TEXT NOT NULL,
                committed_by TEXT NOT NULL,
                PRIMARY KEY (tenant, caller, asset, window))''')

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=5)
        try:
            db.execute('PRAGMA synchronous=FULL')
            with db:
                yield db
        finally:
            db.close()

    def healthy(self):
        with self.connect() as db:
            db.execute('SELECT 1 FROM api_assessments LIMIT 1').fetchone()

    def save(self, tenant, caller, result, observed_at=None):
        key = (tenant, caller, result['asset_id'], result['window_id'])
        saved = dict(result, persisted=True)
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            previous = db.execute('''SELECT request_sha, response FROM api_assessments
                WHERE tenant=? AND caller=? AND asset=? AND window=?''', key).fetchone()
            if previous:
                if previous[0] != result['request_sha256']:
                    raise WindowConflict()
                return json.loads(previous[1])
            db.execute('INSERT INTO api_assessments VALUES (?, ?, ?, ?, ?, ?)',
                       (*key, result['request_sha256'], json.dumps(saved, allow_nan=False)))
        # Sample only AFTER the FULL-synchronous receipt transaction commits.
        # This is a conservative upper bound, not the exact commit instant.
        # A crash before this separate write leaves evidence missing; retries
        # must not invent historical timing for already existing receipts.
        if observed_at is not None:
            committed_by = datetime.now(timezone.utc).isoformat()
            with self.connect() as db:
                db.execute('INSERT INTO assessment_commit_evidence VALUES (?, ?, ?, ?, ?, ?)',
                           (*key, observed_at, committed_by))
        return saved
