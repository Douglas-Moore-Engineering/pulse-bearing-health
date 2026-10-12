import hashlib
import json
import math
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from pulse.core import ReferenceStore, encode, features
from pulse.release import verify_bundle

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def store(tmp_path):
    instance = ReferenceStore(tmp_path / "reference.sqlite", ROOT / "data/contracts")
    yield instance
    instance.close()


def window(store, bearing="bearing-a", split="train", **changes):
    if not store.db.execute("SELECT split FROM groups WHERE dataset=? AND bearing=?", ("fixture", bearing)).fetchone():
        store.assign_groups([("fixture", bearing, split)])
    value = {"schema_version": "0.1", "dataset_id": "fixture", "bearing_id": bearing,
             "run_id": "run-a", "window_id": "w1", "sample_rate_hz": 100, "unit": "m/s2",
             "samples": [-1, 1, -1, 1], "time_basis": "source-relative",
             "source_offset_seconds": 0, "split": split}
    value.update(changes)
    value["source_sha256"] = store.register_source(encode(value), value["dataset_id"],
        value["bearing_id"], value["run_id"], "generated fixture")
    return value


def test_features_known_signal_and_units():
    assert features([-1, 1], "m/s2")["rms_m_s2"] == 1
    assert features([-1, 1], "m/s2")["pearson_kurtosis"] == 1
    assert features([0, 0], "g")["pearson_kurtosis"] is None
    assert features([-1, 1], "g")["rms_m_s2"] == pytest.approx(9.80665)


def test_end_to_end_abstention_and_human_trace(store):
    item = window(store)
    assert store.ingest(item)["accepted"]
    evidence = store.advisory("fixture", "bearing-a", "run-a", "w1")
    assert evidence["status"] == "unavailable"
    assert evidence["rul_hours"] is None and evidence["model_sha256"] is None
    assert evidence["site_validated"] is False
    decision = store.decide(evidence["evidence_id"], "test-actor", "approve", "Acknowledge only")
    assert decision["mock_cmms_proposal"] is None
    assert store.summary()["decisions"] == 1
    trace = json.loads(store.db.execute("SELECT trace FROM evidence").fetchone()[0])
    assert trace["threshold_version"] == "disabled-no-validated-threshold"
    assert trace["data_manifest"]["source_sha256"] == item["source_sha256"]


@pytest.mark.parametrize("changes", [{"unit": "rpm"}, {"sample_rate_hz": 0},
    {"samples": [1]}, {"unexpected": True}, {"time_basis": "utc", "timestamp_utc": "yesterday"}])
def test_contract_failures_quarantined(store, changes):
    result = store.ingest(window(store, **changes))
    assert not result["accepted"]
    assert store.summary()["windows"] == 0
    assert store.summary()["quarantine"] == 1
    with pytest.raises(ValueError):
        store.advisory("fixture", "bearing-a", "run-a", "w1")


def test_unregistered_and_modified_samples_rejected(store):
    item = window(store)
    item["source_sha256"] = "0" * 64
    assert not store.ingest(item)["accepted"]
    item = window(store)
    item["samples"] = [2, 3]
    assert not store.ingest(item)["accepted"]


def test_source_tamper_rejected(store):
    item = window(store)
    store.db.execute("UPDATE sources SET bytes=?", (b"tampered",))
    store.db.commit()
    assert not store.ingest(item)["accepted"]


def test_bearing_not_just_run_disjoint(store):
    assert store.ingest(window(store))["accepted"]
    assert not store.ingest(window(store, split="test", run_id="different-run"))["accepted"]
    assert store.ingest(window(store, bearing="bearing-b", split="test"))["accepted"]


def test_partition_required_before_ingestion_and_cannot_change(store):
    item = window(store)
    with pytest.raises(ValueError, match="reassigned"):
        store.assign_groups([("fixture", "bearing-a", "test")])
    store.db.execute("DELETE FROM groups")
    store.db.commit()
    assert not store.ingest(item)["accepted"]


def test_replay_and_identity_conflict(store):
    item = window(store)
    assert not store.ingest(item)["replayed"]
    assert store.ingest(item)["replayed"]
    assert not store.ingest(window(store, samples=[2, -2]))["accepted"]
    assert store.summary()["windows"] == 1


def test_decision_requires_evidence_and_actor(store):
    with pytest.raises(ValueError):
        store.decide("missing", "actor", "approve", "reason")
    with pytest.raises(ValueError):
        store.decide("missing", "", "approve", "reason")


def test_nonfinite_json_rejected(store):
    item = window(store)
    item["samples"] = [math.nan, 1]
    with pytest.raises(ValueError, match="finite"):
        store.ingest(item)


def test_backup_restores_evidence(store, tmp_path):
    store.ingest(window(store))
    evidence = store.advisory("fixture", "bearing-a", "run-a", "w1")
    backup = tmp_path / "backup.sqlite"
    store.backup(backup)
    restored = ReferenceStore(backup, ROOT / "data/contracts")
    try:
        assert restored.summary() == store.summary()
        assert restored.advisory("fixture", "bearing-a", "run-a", "w1") == evidence
        assert restored.db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    finally:
        restored.close()


@pytest.fixture
def bundle(tmp_path):
    payload = b'{"kind":"fixture"}'
    (tmp_path / "artifact.json").write_bytes(payload)
    manifest = encode({"scope": "offline-reference", "target": "local",
                       "artifacts": {"artifact.json": hashlib.sha256(payload).hexdigest()}})
    now = datetime.now(timezone.utc)
    approval = {"actor": "simulated-reviewer", "scope": "offline-reference", "target": "local",
                "revoked": False, "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
                "issued_at": (now - timedelta(minutes=1)).isoformat(),
                "expires_at": (now + timedelta(minutes=1)).isoformat()}
    return tmp_path, manifest, approval, now


def test_bundle_integrity(bundle):
    root, manifest, approval, now = bundle
    assert verify_bundle(root, manifest, approval, now=now)["target"] == "local"
    (root / "artifact.json").write_text("tampered")
    with pytest.raises(ValueError, match="digest"):
        verify_bundle(root, manifest, approval, now=now)


@pytest.mark.parametrize("field,value", [("revoked", True), ("target", "cloud"),
    ("manifest_sha256", "0" * 64), ("actor", ""), ("scope", "site"),
    ("expires_at", "2000-01-01T00:00:00+00:00"), ("issued_at", "2100-01-01T00:00:00+00:00")])
def test_approval_negative_paths(bundle, field, value):
    root, manifest, approval, now = bundle
    approval[field] = value
    with pytest.raises(ValueError):
        verify_bundle(root, manifest, approval, now=now)


def test_missing_approval_and_escape(bundle):
    root, manifest, approval, now = bundle
    with pytest.raises(ValueError):
        verify_bundle(root, manifest, None, now=now)
    escaped = encode({"scope": "offline-reference", "target": "local", "artifacts": {"../escape.json": "0" * 64}})
    approval["manifest_sha256"] = hashlib.sha256(escaped).hexdigest()
    with pytest.raises(ValueError, match="outside"):
        verify_bundle(root, escaped, approval, now=now)
