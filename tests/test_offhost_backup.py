"""Offline fault injection for backup confirmation; never contacts Azure."""
import io
import runpy
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError

import pytest


UPLOAD = runpy.run_path(str(Path(__file__).resolve().parents[1] /
    'infra/single-node/upload-offhost-backup.py'))['upload']
NOW = datetime(2026, 10, 12, 1, 30, tzinfo=timezone.utc)


@pytest.fixture
def snapshot(tmp_path):
    path = tmp_path / 'snapshot.db'
    with sqlite3.connect(path) as db:
        db.execute('CREATE TABLE api_assessments (id INTEGER PRIMARY KEY)')
        db.execute('INSERT INTO api_assessments VALUES (1)')
    return path


def transport(monkeypatch, snapshot, failure=None):
    calls = []

    def open_request(request, timeout):
        calls.append(request.get_method())
        if len(calls) == 1:
            return io.BytesIO(b'{"access_token":"synthetic-test-token"}')
        if request.get_method() == 'PUT':
            if failure == 'upload':
                raise HTTPError(request.full_url, 503, 'Synthetic outage', {}, None)
            response = io.BytesIO()
            response.status = 201
            return response
        return io.BytesIO(b'corrupt' if failure == 'corrupt' else snapshot.read_bytes())

    monkeypatch.setattr('urllib.request.urlopen', open_request)
    return calls


def test_uploaded_snapshot_is_read_back_and_restored(monkeypatch, snapshot):
    calls = transport(monkeypatch, snapshot)
    result = UPLOAD('example', 'receipts', snapshot, 'synthetic-client', now=NOW)
    assert calls == ['GET', 'PUT', 'GET']
    assert result['restored_receipt_count'] == 1
    assert result['readback_verified'] is True
    assert result['host_loss_rpo_qualified'] is False
    assert result['blob'] == 'receipts/slot-03.db'


@pytest.mark.parametrize('failure, error', [('upload', HTTPError), ('corrupt', RuntimeError)])
def test_failure_never_returns_success_and_retry_recovers(monkeypatch, snapshot, failure, error):
    transport(monkeypatch, snapshot, failure)
    with pytest.raises(error):
        UPLOAD('example', 'receipts', snapshot, 'synthetic-client', now=NOW)
    transport(monkeypatch, snapshot)
    result = UPLOAD('example', 'receipts', snapshot, 'synthetic-client', now=NOW)
    assert result['readback_verified'] is True
    assert result['blob'] == 'receipts/slot-03.db'


def test_invalid_database_rejected_before_network(monkeypatch, tmp_path):
    path = tmp_path / 'invalid.db'
    path.write_bytes(b'not a database')
    def unexpected_network(*args, **kwargs):
        pytest.fail('Invalid backup must not access network')
    monkeypatch.setattr('urllib.request.urlopen', unexpected_network)
    with pytest.raises(sqlite3.DatabaseError):
        UPLOAD('example', 'receipts', path, 'synthetic-client', now=NOW)
