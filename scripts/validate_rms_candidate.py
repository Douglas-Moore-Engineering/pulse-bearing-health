"""Execute the frozen RMS candidate protocol on reserved validation experiments."""
import argparse
import csv
from datetime import datetime
import hashlib
import io
import json
from pathlib import Path
import re
import zipfile

import numpy as np
from scipy.io import loadmat

ROOT = Path(__file__).resolve().parents[1]


def file_hash(path, algorithm="sha256"):
    digest = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(4194304), b""):
            digest.update(chunk)
    return digest.hexdigest()


def replay(rows, count, ratio, persistence, gap_seconds=None):
    eligible_indices = [i for i, row in enumerate(rows) if row["eligible"]]
    if len(eligible_indices) <= count:
        raise ValueError("Insufficient eligible reference and monitoring records")
    end_reference = eligible_indices[count-1]
    reference = np.median([rows[i]["rms"] for i in eligible_indices[:count]], axis=0)
    if not np.isfinite(reference).all() or (reference <= 0).any():
        raise ValueError("Invalid reference RMS")
    streak = [0, 0]
    decisions = []
    active = False
    episodes = 0
    for i in range(end_reference+1, len(rows)):
        row = rows[i]
        gap = (datetime.fromisoformat(row["timestamp"]) - datetime.fromisoformat(rows[i-1]["timestamp"])).total_seconds() if gap_seconds else 0
        if not row["eligible"] or (gap_seconds and gap > gap_seconds):
            streak = [0, 0]
            active = False
        ratios = np.asarray(row["rms"]) / reference
        for channel in range(2):
            streak[channel] = streak[channel]+1 if row["eligible"] and ratios[channel] > ratio else 0
        flagged = max(streak) >= persistence
        if flagged and not active:
            episodes += 1
        active = flagged
        decisions.append({"identity": row["identity"], "eligible": row["eligible"],
                          "ratios": ratios.tolist(), "channel_flags": [s >= persistence for s in streak],
                          "flagged": flagged, "timestamp": row.get("timestamp")})
    flags = [d for d in decisions if d["flagged"]]
    first = flags[0] if flags else None
    lead = (datetime.fromisoformat(rows[-1]["timestamp"])-datetime.fromisoformat(first["timestamp"])).total_seconds()/60 if first and gap_seconds else None
    return {"reference_rms": reference.tolist(), "reference_records": count,
            "monitoring_records": len(decisions), "excluded_regime_records_total": sum(not r["eligible"] for r in rows),
            "flagged_records": len(flags), "bearing_alert_episodes": episodes,
            "first_flag": first, "descriptive_lead_minutes": lead,
            "channel_flagged_records": [sum(d["channel_flags"][c] for d in decisions) for c in (0,1)],
            "decisions": decisions}


def ldm(protocol):
    path = ROOT / "outputs/reference-dataset-review/B04.zip"
    if file_hash(path, "md5") != "9d7c11dc6a83424b440ae6d184064dcb":
        raise ValueError("B04 publisher checksum mismatch")
    cfg = protocol["ldm_b04"]
    rows = []
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        context = list(csv.DictReader(io.StringIO(archive.read("B04/B04_operatingConditions.csv").decode("utf-8-sig"))))
        temperatures = list(csv.DictReader(io.StringIO(archive.read("B04/B04_meanTemperatures.csv").decode("utf-8-sig"))))
        if len(context) != 1114 or [r["Time"] for r in context] != [r["Time"] for r in temperatures]:
            raise ValueError("Context timelines disagree")
        mats = sorted([n for n in names if n.endswith(".mat")])
        if len(mats) != 1114:
            raise ValueError("Unexpected B04 member count")
        previous = None
        for i, name in enumerate(mats):
            match = re.search(r"data_B04_M(\d+)\.mat$", name)
            if not match or int(match[1]) != i+1:
                raise ValueError("Non-contiguous measurement ordinals")
            raw = archive.read(name)
            native = loadmat(io.BytesIO(raw))
            vectors = [np.asarray(native[k]).reshape(-1) for k in ("accHorizRear_A", "accHorizFrontal_C", "measTime")]
            if any(v.shape != (cfg["sample_count"],) or not np.isfinite(v).all() for v in vectors):
                raise ValueError("Invalid B04 vector")
            if not np.allclose(vectors[2], np.arange(cfg["sample_count"])/cfg["sample_rate_hz"], atol=1e-10, rtol=0):
                raise ValueError("Unexpected sampling times")
            timestamp = datetime.strptime(context[i]["Time"], "%d-%b-%Y %H:%M:%S")
            if previous and timestamp <= previous:
                raise ValueError("Non-increasing acquisition time")
            previous = timestamp
            speed, load = float(context[i]["setSpeed / rpm"]), float(context[i]["setDynLoad / N"])
            if not np.isfinite([speed, load]).all():
                raise ValueError("Invalid operating condition")
            rows.append({"identity": name, "sha256": hashlib.sha256(raw).hexdigest(),
                         "timestamp": timestamp.isoformat(), "eligible": speed >= 1500 and load > 0,
                         "set_speed_rpm": speed, "set_dynamic_load_N": load,
                         "rms": [float(np.sqrt(np.mean(v*v))*cfg["g_per_volt"]) for v in vectors[:2]]})
            if (i+1) % 200 == 0:
                print("B04", i+1, flush=True)
    return rows, {"archive_sha256": file_hash(path), "publisher_md5_verified": True, "units": "g"}


def unsw(protocol):
    source = ROOT / "outputs/reference-dataset-review/h4df4mgrfb/test2-native"
    paths = sorted(source.rglob("*.mat"))
    selected = []
    for path in paths:
        if path.parent.name != "6Hz":
            continue
        match = re.fullmatch(r"vib_(\d+)_06\.mat", path.name)
        if not match:
            raise ValueError("Unexpected 6Hz identity")
        selected.append((int(match[1]), path))
    selected.sort()
    inventory = json.loads((ROOT / "outputs/reference-dataset-review/unsw-test2-inventory.json").read_text())
    expected = {r["name"] for r in inventory if "/6Hz/" in r["name"] and r["name"].endswith(".mat")}
    if {p.relative_to(source).as_posix() for _, p in selected} != expected:
        raise ValueError("Extracted sequence does not match complete archive inventory")
    if not selected or any(b[0] <= a[0] for a,b in zip(selected, selected[1:])):
        raise ValueError("Invalid cycle chronology")
    archive = source.parent / "Test 2.7z"
    if file_hash(archive) != "f60dfcb97ee5ca0ec2635a1a44b7ba9adcd02988001fc30a1d85970cb0da4b8a":
        raise ValueError("UNSW archive mismatch")
    rows = []
    for cycle, path in selected:
        raw = path.read_bytes()
        data = loadmat(io.BytesIO(raw))
        rate = float(np.asarray(data["Fs"]).item())
        if rate != protocol["unsw_test2"]["sample_rate_hz"]:
            raise ValueError("Unexpected sample rate")
        vectors = [np.asarray(data[k]).reshape(-1) for k in protocol["unsw_test2"]["expected_channels"]]
        if not len(vectors[0]) or any(v.shape != vectors[0].shape or not np.isfinite(v).all() for v in vectors):
            raise ValueError("Invalid native channels")
        rows.append({"identity": path.relative_to(source).as_posix(), "shaft_cycle": cycle,
                     "sha256": hashlib.sha256(raw).hexdigest(), "samples": len(vectors[0]),
                     "sample_rate_hz": rate, "eligible": True,
                     "rms": [float(np.sqrt(np.mean(v*v))) for v in vectors[:2]]})
    return rows, {"publisher_sha256_verified": True, "archive_sha256": file_hash(archive),
                  "units": "volts", "time_lead_scorable": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", choices=("ldm_b04", "unsw_test2"))
    args = parser.parse_args()
    policy_path = ROOT / "config/rms-v2-validation-protocol.json"
    freeze = json.loads((ROOT / "governance/evidence/rms-v2-validation-freeze.json").read_text())
    if file_hash(policy_path) != freeze["protocol_sha256"]:
        raise ValueError("Frozen protocol changed")
    policy = json.loads(policy_path.read_text())
    rows, provenance = (ldm if args.dataset == "ldm_b04" else unsw)(policy)
    cfg = policy[args.dataset]
    result = replay(rows, cfg["reference_records"], policy["ratio_strictly_greater_than"],
                    policy["consecutive_eligible_records"], cfg["maximum_gap_seconds"])
    result.update(dataset=args.dataset, protocol_sha256=freeze["protocol_sha256"],
                  code_sha256=file_hash(Path(__file__)), native_features=rows, provenance=provenance,
                  qualified_detector=False, nuisance_alert_target_validated=False,
                  endpoint_failure_warning_validated=False)
    output = ROOT / f"governance/evidence/{args.dataset}-rms-v2-validation.json"
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ("native_features", "decisions")}, indent=2))


if __name__ == "__main__":
    main()
