"""Transactional, explicitly unqualified reference RMS detector and simulated inbox."""
from datetime import datetime
import hashlib
import json
import math
from pulse.alert_ledger import AlertLedger, AlertConflict

POLICY = 'research-rms-3x-3snap-v1'
ASSET = 'ims-run2-bearing1-reference'
BASELINE_RMS = 0.07765955594342575
BASELINE_SOURCE = '79d4e65957b02ed7b71c31ace93ee332f29f817e023b67f22e019b51d70f0db7'


class ReferenceOrderError(ValueError):
    pass


class ReferenceDetector(AlertLedger):
    def __init__(self, path):
        super().__init__(path)
        with self.connection() as db:
            db.execute('''CREATE TABLE IF NOT EXISTS reference_windows (
                scope TEXT NOT NULL, asset TEXT NOT NULL, window TEXT NOT NULL,
                request_sha TEXT NOT NULL, response TEXT NOT NULL,
                PRIMARY KEY(scope,asset,window))''')
            db.execute('''CREATE TABLE IF NOT EXISTS reference_state (
                scope TEXT NOT NULL, asset TEXT NOT NULL, policy TEXT NOT NULL,
                observed TEXT NOT NULL, streak INTEGER NOT NULL, event_id TEXT,
                PRIMARY KEY(scope,asset,policy))''')

    def assess(self, tenant, caller, payload):
        if payload['asset_id'] != ASSET or not math.isfinite(payload['rms_native']) or payload['rms_native'] < 0:
            raise ValueError('Unsupported reference asset or RMS')
        observed = datetime.strptime(payload['source_timestamp'], '%Y.%m.%d.%H.%M.%S')
        encoded = json.dumps(payload, sort_keys=True, separators=(',', ':'), allow_nan=False)
        request_sha = hashlib.sha256(encoded.encode()).hexdigest()
        scope = json.dumps([tenant, caller], separators=(',', ':'))
        key = (scope, ASSET, payload['window_id'])
        ratio = payload['rms_native']/BASELINE_RMS
        with self.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            old = db.execute('SELECT request_sha,response FROM reference_windows WHERE scope=? AND asset=? AND window=?', key).fetchone()
            if old:
                if old['request_sha'] != request_sha:
                    raise AlertConflict('Reference window content changed')
                return json.loads(old['response'])
            state = db.execute('SELECT * FROM reference_state WHERE scope=? AND asset=? AND policy=?',
                               (scope, ASSET, POLICY)).fetchone()
            streak, event = 0, None
            if state:
                gap = (observed-datetime.strptime(state['observed'], '%Y.%m.%d.%H.%M.%S')).total_seconds()
                if gap <= 0:
                    raise ReferenceOrderError('Reference windows must arrive in source-time order')
                if gap <= 900:
                    streak, event = state['streak'], state['event_id']
            if ratio > 3:
                streak += 1
            else:
                streak, event = 0, None
            if streak >= 3 and event is None:
                episode = payload['source_timestamp']
                event = hashlib.sha256(json.dumps([scope, ASSET, episode, POLICY]).encode()).hexdigest()
                evidence = json.dumps({'scope': 'unqualified_reference_only',
                    'source_timestamp': episode, 'source_timezone': 'unknown',
                    'rms_ratio': ratio, 'source_sha256': payload['source_sha256'],
                    'source_integrity': 'caller_asserted_not_verified',
                    'baseline_plan_sha256': BASELINE_SOURCE,
                    'destination': 'simulated_maintenance_inbox', 'external_notification_sent': False}, sort_keys=True)
                from datetime import timezone
                db.execute('INSERT INTO alerts VALUES(?,?,?,?,?,?,?,NULL,NULL)',
                           (event, scope, ASSET, episode, POLICY, evidence, datetime.now(timezone.utc).isoformat()))
            result = {'asset_id': ASSET, 'window_id': payload['window_id'],
                'request_sha256': request_sha, 'policy_version': POLICY,
                'rms_ratio': ratio, 'consecutive_exceedances': streak,
                'reference_status': 'reference_anomaly' if streak >= 3 else 'no_reference_flag',
                'event_id': event, 'persisted': True,
                'qualified_detector': False, 'site_validated': False,
                'notification_destination': 'simulated_maintenance_inbox',
                'external_notification_sent': False, 'source_timezone': 'unknown',
                'reason': 'Research RMS rule; fictional acceptance targets not met; no failure prediction'}
            db.execute('INSERT OR REPLACE INTO reference_state VALUES(?,?,?,?,?,?)',
                       (scope, ASSET, POLICY, payload['source_timestamp'], streak, event))
            db.execute('INSERT INTO reference_windows VALUES(?,?,?,?,?)',
                       (*key, request_sha, json.dumps(result, allow_nan=False)))
        return result

    def inbox(self, tenant, caller, asset):
        scope = json.dumps([tenant, caller], separators=(',', ':'))
        with self.connection() as db:
            rows = db.execute('SELECT * FROM alerts WHERE tenant=? AND asset=? ORDER BY created DESC LIMIT 100',
                              (scope, asset)).fetchall()
        return [dict(row) for row in rows]

    def acknowledge_reference(self, tenant, caller, asset, event):
        scope = json.dumps([tenant, caller], separators=(',', ':'))
        return self.acknowledge(scope, asset, event, caller)
