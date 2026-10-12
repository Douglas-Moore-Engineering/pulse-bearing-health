"""Compare RMS thresholds on consumed IMS and UNSW development experiments."""
import hashlib
import io
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from pulse.ims_baseline import evaluate


def main():
    reports = []
    for run, count, channels, previous in (
        ("1st_test", 2156, 8, "ims-run1-independent.json"),
        ("2nd_test", 984, 4, "ims-run2-baseline.json"),
    ):
        source = ROOT / "outputs/reference-dataset-review/IMS-sample" / run
        paths = sorted(p for p in source.rglob("*") if p.is_file())
        if len(paths) != count:
            raise ValueError(f"Unexpected {run} inventory: {len(paths)}")
        old = json.loads((ROOT / "governance/evidence" / previous).read_text())
        lineage = {r["member"]: r["sha256"] for r in old["lineage"]}
        features = []
        for index, path in enumerate(paths):
            raw = path.read_bytes()
            if hashlib.sha256(raw).hexdigest() != lineage[path.relative_to(source).as_posix()]:
                raise ValueError("Native source differs from previous verified run")
            values = np.loadtxt(io.BytesIO(raw))
            if values.shape != (20480, channels) or not np.isfinite(values).all():
                raise ValueError("Invalid source shape or values")
            features.append(np.sqrt(np.mean(values * values, axis=0)))
            if index % 500 == 0:
                print(run, index, flush=True)
        features = np.asarray(features)
        for ratio in (1.5, 2.0, 2.5, 3.0):
            summaries = []
            for offset in range(0, channels, 4):
                result = evaluate([p.name for p in paths], features[:, offset:offset+4],
                                  baseline_count=100, ratio=ratio, persistence=3,
                                  maximum_gap_seconds=900)
                for row in result["channels"]:
                    channel = row.pop("bearing") + offset
                    row.update(channel=channel, bearing=(channel+1)//2 if channels == 8 else channel)
                    summaries.append(row)
            reports.append({"dataset": "IMS", "run": run, "ratio": ratio,
                            "reference_recordings": 100, "channels": summaries,
                            "source_evidence_sha256": hashlib.sha256(
                                (ROOT / "governance/evidence" / previous).read_bytes()).hexdigest()})
    # UNSW uses shaft cycles; no invented wall-clock lead or timed gap handling.
    source = ROOT / "governance/evidence/unsw-test1-native-profile.json"
    rows = sorted((r for r in json.loads(source.read_text())["measurements"]
                   if "/6Hz/" in r["member"]), key=lambda r: r["shaft_cycle"])
    if len(rows) != 80 or any(b["shaft_cycle"] <= a["shaft_cycle"] for a,b in zip(rows, rows[1:])):
        raise ValueError("Unexpected UNSW development sequence")
    for ratio in (1.5, 2.0, 2.5, 3.0):
        summaries = []
        for channel in ("accH", "accV"):
            amplitudes = np.array([r[channel+"_rms_volts"] for r in rows])
            reference = float(np.median(amplitudes[:10]))
            streak = 0
            flags = []
            for index in range(10, len(rows)):
                streak = streak + 1 if amplitudes[index] / reference > ratio else 0
                if streak >= 3:
                    flags.append(index)
            summaries.append({"channel": channel, "reference_rms_volts": reference,
                              "flagged_recordings": len(flags),
                              "first_flag_shaft_cycle": rows[flags[0]]["shaft_cycle"] if flags else None,
                              "time_lead_available": False})
        reports.append({"dataset": "UNSW", "run": "Test 1 / 6Hz", "ratio": ratio,
                        "reference_recordings": 10, "sequence_recordings": 80,
                        "temporal_persistence_qualified": False, "channels": summaries,
                        "source_evidence_sha256": hashlib.sha256(source.read_bytes()).hexdigest()})
    result = {"purpose": "Post-result development threshold comparison; no held-out evaluation",
              "qualified_detector": False, "healthy_exposure_qualified": False,
              "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "baseline_code_sha256": hashlib.sha256((ROOT / "src/pulse/ims_baseline.py").read_bytes()).hexdigest(),
              "results": reports}
    (ROOT / "governance/evidence/development-threshold-comparison.json").write_text(
        json.dumps(result, indent=2) + "\n")
    print("Wrote development comparison", flush=True)


if __name__ == "__main__":
    main()
