"""Execute a frozen research final test on LDM B12 or B17 without retuning."""
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
from validate_rms_candidate import replay, file_hash
ROOT = Path(__file__).resolve().parents[1]

def profile(protocol, run):
    path = ROOT / f"outputs/reference-dataset-review/{run}.zip"
    if file_hash(path, "md5") != protocol["runs"][run]["publisher_checksum"].removeprefix("md5:"):
        raise ValueError("Publisher checksum mismatch")
    cfg = protocol["runs"][run]
    rows = []
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        context = list(csv.DictReader(io.StringIO(archive.read(f"{run}/{run}_operatingConditions.csv").decode("utf-8-sig"))))
        temperatures = list(csv.DictReader(io.StringIO(archive.read(f"{run}/{run}_meanTemperatures.csv").decode("utf-8-sig"))))
        if len(context) != cfg["records"] or [r["Time"] for r in context] != [r["Time"] for r in temperatures]:
            raise ValueError("Context timelines disagree")
        mats = sorted([n for n in names if n.endswith(".mat")])
        if len(mats) != cfg["records"]:
            raise ValueError("Unexpected run member count")
        previous = None
        for i, name in enumerate(mats):
            match = re.search(rf"data_{run}_M(\d+)\.mat$", name)
            if not match or int(match[1]) != i+1:
                raise ValueError("Non-contiguous measurement ordinals")
            raw = archive.read(name)
            native = loadmat(io.BytesIO(raw))
            vectors = [np.asarray(native[k]).reshape(-1) for k in ("accHorizRear_A", "accHorizFrontal_C", "measTime")]
            if any(v.shape != (cfg["sample_count"],) or not np.isfinite(v).all() for v in vectors):
                raise ValueError("Invalid native vector")
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
                print(run, i+1, flush=True)
    return rows, {"archive_sha256": file_hash(path), "publisher_md5_verified": True, "units": "g"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run", choices=("B12", "B17"))
    args = parser.parse_args()
    path = ROOT / "config/rms-v2-ldm-final-protocol.json"
    freeze = json.loads((ROOT / "governance/evidence/rms-v2-ldm-final-freeze.json").read_text())
    if file_hash(path) != freeze["protocol_sha256"] or file_hash(ROOT / "scripts/validate_rms_candidate.py") != freeze["validation_replay_code_sha256"]:
        raise ValueError("Frozen protocol or replay code changed")
    policy = json.loads(path.read_text())
    rows, provenance = profile(policy, args.run)
    cfg = policy["runs"][args.run]
    result = replay(rows, cfg["reference_records"], policy["ratio"], policy["persistence"], cfg["maximum_gap_seconds"])
    result.update(run=args.run, protocol_sha256=freeze["protocol_sha256"], code_sha256=file_hash(Path(__file__)),
                  replay_code_sha256=freeze["validation_replay_code_sha256"], native_features=rows,
                  provenance=provenance, qualified_detector=False, nuisance_target_scorable=False,
                  failure_warning_acceptance_scorable=False)
    result["descriptive_60min_proxy_met"] = result["descriptive_lead_minutes"] is not None and result["descriptive_lead_minutes"] >= 60
    (ROOT / f"governance/evidence/ldm-{args.run}-rms-v2-final.json").write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ("decisions", "native_features")},indent=2))

if __name__ == "__main__":
    main()
