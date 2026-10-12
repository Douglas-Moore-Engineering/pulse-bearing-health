"""Evaluate existing extracted IMS run 2 bytes without publishing raw data."""
import argparse
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from pulse.ims_baseline import evaluate, snapshot_features


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest() if hasattr(hashlib, "file_digest") else hashlib.sha256(stream.read()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plan_path = Path("data/qualification/ims-baseline-plan.json")
    plan = json.loads(plan_path.read_text())
    paths = sorted(p for p in args.data.rglob("*") if p.is_file())
    if len(paths) != 984:
        raise ValueError(f"Expected 984 run 2 snapshots, found {len(paths)}")
    lineage = []
    features = []
    for p in paths:
        features.append(snapshot_features(np.loadtxt(p)))
        lineage.append({"member": p.relative_to(args.data).as_posix(), "sha256": digest(p)})
    result = evaluate([p.name for p in paths], features,
                      plan["baseline_snapshots"], plan["threshold_ratio"],
                      plan["consecutive_snapshots"], plan["maximum_gap_seconds"])
    result.update(executed_at=datetime.now(timezone.utc).isoformat(),
                  plan=plan, plan_sha256=digest(plan_path),
                  code_sha256={str(p): digest(p) for p in [Path(__file__), Path("src/pulse/ims_baseline.py")]},
                  environment={"python": platform.python_version(), "numpy": np.__version__},
                  lineage=lineage, numerical_schema_validated=True,
                  qualified_detector=False, fault_onset_known=False,
                  amplitude_units="unknown", sample_rate_hz=20000,
                  documented_endpoint="Bearing 1 outer-race failure at experiment end; onset unknown")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k != "lineage"}, indent=2))


if __name__ == "__main__":
    main()
