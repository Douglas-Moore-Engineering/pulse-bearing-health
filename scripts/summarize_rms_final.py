"""Record the research outcome separately from unresolved release acceptance."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
results = []
for run in ("B12", "B17"):
    path = ROOT / f"governance/evidence/ldm-{run}-rms-v2-final.json"
    data = json.loads(path.read_text())
    results.append({"run": run, "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "monitoring_records": data["monitoring_records"],
                    "flagged_records": data["flagged_records"],
                    "episodes": data["bearing_alert_episodes"],
                    "lead_minutes_to_last_acquisition": data["descriptive_lead_minutes"],
                    "descriptive_proxy_met": data["descriptive_60min_proxy_met"]})
decision = {"candidate": "relative-rms-1p5x-3record-v2", "runs": results,
            "all_descriptive_proxies_met": all(r["descriptive_proxy_met"] for r in results),
            "physical_failure_warning_target": "NOT_EVALUABLE_FROM_AVAILABLE_LABELS",
            "nuisance_alert_target": "NOT_EVALUABLE_WITHOUT_VERIFIED_HEALTHY_EXPOSURE",
            "release_decision": "NOT_PROMOTED", "deployed_rule_changed": False,
            "UNSW_tests_3_4_consumed": False,
            "scope": "Evidence summary, not a technical deployment enforcement control"}
(ROOT / "governance/evidence/rms-v2-final-disposition.json").write_text(json.dumps(decision, indent=2)+'\n')
print(json.dumps(decision, indent=2))
