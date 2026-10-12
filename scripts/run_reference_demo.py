"""Generate fixture-only end-to-end evidence; no downloads, training or cloud calls."""
import argparse
import html
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from pulse.core import ReferenceStore, encode


def run(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    database = output / "reference.sqlite"
    if database.exists():
        raise ValueError("Use a fresh output directory to preserve previous evidence")
    store = ReferenceStore(database, ROOT / "data/contracts")
    evidences = []
    try:
        store.assign_groups([("GENERATED-FIXTURE", f"fixture-bearing-{i}", split)
                             for i, split in enumerate(("train", "validation", "test"))])
        for index, split in enumerate(("train", "validation", "test")):
            window = {
                "schema_version": "0.1", "dataset_id": "GENERATED-FIXTURE",
                "bearing_id": f"fixture-bearing-{index}", "run_id": f"run-{index}",
                "window_id": "window-0", "sample_rate_hz": 1024, "unit": "m/s2",
                "samples": [math.sin(2 * math.pi * 32 * n / 1024) for n in range(1024)],
                "time_basis": "source-relative", "source_offset_seconds": 0, "split": split,
            }
            window["source_sha256"] = store.register_source(
                encode(window), window["dataset_id"], window["bearing_id"], window["run_id"],
                "Generated mathematical fixture; no customer or benchmark bytes")
            result = store.ingest(window)
            if not result["accepted"]:
                raise RuntimeError(result)
            evidence = store.advisory(window["dataset_id"], window["bearing_id"], window["run_id"], window["window_id"])
            evidences.append({"advisory": evidence, "features": result["features"]})
            store.decide(evidence["evidence_id"], "simulated-reviewer", "reject",
                         "Fixture exercise only; no operational maintenance decision")
        store.ingest({"schema_version": "wrong"})
        store.backup(output / "backup.sqlite")
        report = {"scope": "Generated-fixture software exercise only", "site_validated": False,
                  "model_trained": False, "cloud_deployed": False, "counts": store.summary(),
                  "results": evidences}
        (output / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        cards = "".join("<article><h2>" + html.escape(e["advisory"]["asset_id"]) + "</h2><strong>Unavailable</strong><p>"
                        + html.escape(e["advisory"]["reason"]) + "</p><pre>"
                        + html.escape(json.dumps(e["features"], indent=2)) + "</pre><small>Evidence: "
                        + e["advisory"]["evidence_id"] + "</small></article>" for e in evidences)
        (output / "index.html").write_text(
            '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
            '<title>Pulse reference evidence</title><style>body{font:17px Arial;background:#f4f7fa;color:#152c3a;'
            'max-width:1000px;margin:40px auto;padding:20px}article{background:white;border:1px solid #ccd8df;'
            'padding:24px;margin:20px 0}strong{color:#876a2d}small{overflow-wrap:anywhere}</style>'
            '<h1>Pulse · Reference evidence</h1><p>Generated fixtures · No trained model · Unvalidated for customer site</p>'
            '<p>RMS and kurtosis describe these generated signals. They do not establish equipment health, fault diagnosis or RUL.</p>'
            + cards + '</html>', encoding="utf-8")
        return report
    finally:
        store.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output)["counts"], indent=2))
