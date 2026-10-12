"""Offline reference processing. No trained model or equipment/CMMS connection."""
from __future__ import annotations

import hashlib
import json
import math
import sqlite3
import statistics
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(encode(value)).hexdigest()


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def features(samples, unit):
    """Population Pearson kurtosis; convert acceleration to m/s² first."""
    scale = 9.80665 if unit == "g" else 1.0
    values = [float(v) * scale for v in samples]
    mean = statistics.fmean(values)
    variance = statistics.fmean((v - mean) ** 2 for v in values)
    return {
        "rms_m_s2": math.sqrt(statistics.fmean(v * v for v in values)),
        "pearson_kurtosis": (
            statistics.fmean((v - mean) ** 4 for v in values) / variance ** 2
            if variance > 0 else None
        ),
        "feature_version": "rms-pearson-kurtosis-1",
    }


class ReferenceStore:
    """Local single-operator store; file access is the trust boundary, not cloud IAM."""

    def __init__(self, path, contracts):
        self.db = sqlite3.connect(path)
        self.db.execute("PRAGMA foreign_keys=ON")
        self.contracts = Path(contracts)
        self.validators = {}
        for name in ("vibration-window", "advisory"):
            schema = json.loads((self.contracts / f"{name}.schema.json").read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            self.validators[name] = Draft202012Validator(schema, format_checker=FormatChecker())
        self.db.executescript("""
          CREATE TABLE IF NOT EXISTS sources (
            digest TEXT PRIMARY KEY, dataset TEXT NOT NULL, bearing TEXT NOT NULL,
            run TEXT NOT NULL, rights_ref TEXT NOT NULL, bytes BLOB NOT NULL);
          CREATE TABLE IF NOT EXISTS groups (
            dataset TEXT NOT NULL, bearing TEXT NOT NULL, split TEXT NOT NULL,
            PRIMARY KEY(dataset,bearing));
          CREATE TABLE IF NOT EXISTS windows (
            dataset TEXT NOT NULL, bearing TEXT NOT NULL, run TEXT NOT NULL,
            window TEXT NOT NULL, payload TEXT NOT NULL, features TEXT NOT NULL,
            source TEXT NOT NULL REFERENCES sources(digest),
            PRIMARY KEY(dataset,bearing,run,window));
          CREATE TABLE IF NOT EXISTS quarantine (
            id INTEGER PRIMARY KEY, recorded_at TEXT NOT NULL,
            payload_digest TEXT NOT NULL, reasons TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS evidence (
            id TEXT PRIMARY KEY, payload TEXT NOT NULL, trace TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS decisions (
            id TEXT PRIMARY KEY, evidence TEXT NOT NULL REFERENCES evidence(id),
            actor TEXT NOT NULL, recorded_at TEXT NOT NULL,
            disposition TEXT NOT NULL, rationale TEXT NOT NULL, proposal TEXT);
        """)

    def close(self):
        self.db.close()

    def assign_groups(self, assignments):
        """Freeze bearing partitions before window ingestion; conflicting reassignment fails."""
        if not assignments:
            raise ValueError("A nonempty bearing split manifest is required")
        with self.db:
            for item in assignments:
                dataset, bearing, split = item
                if not all(isinstance(x, str) and x.strip() for x in item) or split not in ("train", "validation", "test"):
                    raise ValueError("Invalid bearing split assignment")
                existing = self.db.execute("SELECT split FROM groups WHERE dataset=? AND bearing=?", (dataset, bearing)).fetchone()
                if existing and existing[0] != split:
                    raise ValueError("Frozen bearing partition cannot be reassigned")
                self.db.execute("INSERT OR IGNORE INTO groups VALUES (?,?,?)", (dataset, bearing, split))

    def register_source(self, raw, dataset, bearing, run, rights_ref):
        for value in (dataset, bearing, run, rights_ref):
            if not isinstance(value, str) or not value.strip() or value.strip().upper() == "TBD":
                raise ValueError("Explicit source identifiers and rights reference required")
        sha = hashlib.sha256(raw).hexdigest()
        row = (sha, dataset, bearing, run, rights_ref, raw)
        existing = self.db.execute("SELECT * FROM sources WHERE digest=?", (sha,)).fetchone()
        if existing and existing != row:
            raise ValueError("Source digest already bound to different provenance")
        with self.db:
            self.db.execute("INSERT OR IGNORE INTO sources VALUES (?,?,?,?,?,?)", row)
        return sha

    def _quarantine(self, record, reasons):
        # No raw signals or sensitive payloads in diagnostic logs.
        with self.db:
            self.db.execute("INSERT INTO quarantine(recorded_at,payload_digest,reasons) VALUES (?,?,?)",
                            (utc_now(), digest(record), json.dumps(reasons)))
        return {"accepted": False, "reasons": reasons}

    def ingest(self, record):
        try:
            encode(record)
        except (ValueError, TypeError) as exc:
            raise ValueError("Input must be finite JSON") from exc
        errors = [e.message for e in self.validators["vibration-window"].iter_errors(record)]
        if errors:
            return self._quarantine(record, errors)
        if record["time_basis"] == "utc":
            try:
                timestamp = datetime.fromisoformat(record["timestamp_utc"].replace("Z", "+00:00"))
                if timestamp.tzinfo is None or timestamp.utcoffset().total_seconds() != 0:
                    raise ValueError("UTC offset required")
            except ValueError:
                return self._quarantine(record, ["timestamp_utc must be a valid UTC timestamp"])
        # Guard arithmetic range and work size in addition to the versioned schema.
        if len(record["samples"]) > 1_000_000 or any(abs(x) > 1e6 for x in record["samples"]):
            return self._quarantine(record, ["Reference processing range exceeded"])
        source = self.db.execute("SELECT dataset,bearing,run,bytes FROM sources WHERE digest=?",
                                 (record["source_sha256"],)).fetchone()
        identity = (record["dataset_id"], record["bearing_id"], record["run_id"])
        if source is None or source[:3] != identity:
            return self._quarantine(record, ["Unregistered source or provenance mismatch"])
        if hashlib.sha256(source[3]).hexdigest() != record["source_sha256"]:
            return self._quarantine(record, ["Source bytes failed integrity check"])
        try:
            source_window = json.loads(source[3])
        except (ValueError, UnicodeError):
            return self._quarantine(record, ["Reference adapter requires one JSON source window"])
        if source_window != {k: v for k, v in record.items() if k != "source_sha256"}:
            return self._quarantine(record, ["Window differs from registered source bytes"])
        group = identity[:2]
        split = self.db.execute("SELECT split FROM groups WHERE dataset=? AND bearing=?", group).fetchone()
        if split is None:
            return self._quarantine(record, ["Bearing partition must be assigned before ingestion"])
        if split[0] != record["split"]:
            return self._quarantine(record, ["Bearing group leakage across partitions"])
        key = (*identity, record["window_id"])
        payload = encode(record).decode()
        existing = self.db.execute("SELECT payload FROM windows WHERE dataset=? AND bearing=? AND run=? AND window=?", key).fetchone()
        if existing and existing[0] != payload:
            return self._quarantine(record, ["Window identity reused with changed content"])
        computed = features(record["samples"], record["unit"])
        with self.db:
            self.db.execute("INSERT OR IGNORE INTO windows VALUES (?,?,?,?,?,?,?)",
                            (*key, payload, encode(computed).decode(), record["source_sha256"]))
        return {"accepted": True, "replayed": existing is not None, "features": computed}

    def advisory(self, dataset, bearing, run, window):
        row = self.db.execute("SELECT payload,features FROM windows WHERE dataset=? AND bearing=? AND run=? AND window=?",
                              (dataset, bearing, run, window)).fetchone()
        if row is None:
            raise ValueError("Only accepted windows can generate evidence")
        record, computed = map(json.loads, row)
        trace = {
            "input_digest": digest(record), "source_sha256": record["source_sha256"],
            "features": computed, "threshold_version": "disabled-no-validated-threshold",
            "policy_version": "reference-abstain-1", "model_sha256": None,
            "scope": "offline-reference", "site_validated": False,
        }
        source = self.db.execute("SELECT rights_ref FROM sources WHERE digest=?", (record["source_sha256"],)).fetchone()
        manifest = {"dataset_id": dataset, "bearing_id": bearing, "run_id": run,
                    "source_sha256": record["source_sha256"], "rights_evidence": source[0]}
        evidence = {
            "evidence_id": digest({"trace": trace, "manifest": manifest}), "asset_id": bearing,
            "status": "unavailable",
            "reason": "Reference only; unvalidated for customer site. No qualified anomaly model, fault classes or RUL method.",
            "data_manifest_sha256": digest(manifest), "feature_version": computed["feature_version"],
            "model_sha256": None, "policy_version": trace["policy_version"],
            "site_validated": False, "rul_hours": None, "rul_interval_hours": None,
        }
        self.validators["advisory"].validate(evidence)
        trace["data_manifest"] = manifest
        with self.db:
            self.db.execute("INSERT OR IGNORE INTO evidence VALUES (?,?,?)",
                            (evidence["evidence_id"], encode(evidence).decode(), encode(trace).decode()))
        return evidence

    def decide(self, evidence_id, actor, disposition, rationale):
        if disposition not in ("approve", "modify", "reject"):
            raise ValueError("Disposition must be approve, modify or reject")
        if not all(isinstance(x, str) and x.strip() for x in (actor, rationale)):
            raise ValueError("Actor and rationale are required")
        row = self.db.execute("SELECT payload FROM evidence WHERE id=?", (evidence_id,)).fetchone()
        if row is None:
            raise ValueError("Evidence does not exist")
        # A user may acknowledge unavailable evidence; no work proposal follows it.
        timestamp = utc_now()
        decision = {"evidence_id": evidence_id, "actor": actor, "time": timestamp,
                    "disposition": disposition, "rationale": rationale,
                    "mock_cmms_proposal": None, "site_validated": False}
        decision["decision_id"] = digest(decision)
        with self.db:
            self.db.execute("INSERT INTO decisions VALUES (?,?,?,?,?,?,?)",
                            (decision["decision_id"], evidence_id, actor, timestamp, disposition, rationale, None))
        return decision

    def backup(self, destination):
        with sqlite3.connect(destination) as target:
            self.db.backup(target)

    def summary(self):
        return {table: self.db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                for table in ("sources", "windows", "quarantine", "evidence", "decisions")}
