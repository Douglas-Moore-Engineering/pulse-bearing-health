"""Verify the KAIST archive and profile three development snapshots, without extraction."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import zipfile

import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--all", action="store_true", help="Inspect every development recording")
    args = parser.parse_args()
    expected = "7deeafed7334ed18b4da552075ef73391c15bc6b206dcdf6c0c7ec3e4e2657c6"
    digest = hashlib.sha256()
    with args.archive.open("rb") as stream:
        for chunk in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            digest.update(chunk)
    if digest.hexdigest() != expected:
        raise ValueError("Archive does not match publisher SHA-256")
    profiles = []
    with zipfile.ZipFile(args.archive) as archive:
        members = sorted(archive.infolist(), key=lambda member: member.filename)
        if len(members) != 129 or any(not m.filename.endswith(".csv") for m in members):
            raise ValueError("Unexpected archive inventory")
        for index in (range(len(members)) if args.all else (0, 64, 128)):
            member = members[index]
            if member.file_size > 160_000_000:
                raise ValueError("Snapshot exceeds inspection bound")
            raw = archive.read(member)  # CRC is checked by zipfile.
            # The inspected native CSV is headerless; never discard its first sample.
            values = np.loadtxt(io.BytesIO(raw), delimiter=",")
            if values.ndim != 2 or values.shape[1] != 4:
                raise ValueError("Expected four native columns")
            finite = np.isfinite(values)
            columns = [values[:, i][finite[:, i]] for i in range(4)]
            if any(len(column) == 0 for column in columns):
                raise ValueError("Column has no finite samples")
            profiles.append({
                "member": member.filename, "sha256": hashlib.sha256(raw).hexdigest(),
                "crc_verified": True, "shape": list(values.shape),
                "header": None,
                "nonfinite_per_column": (~finite).sum(axis=0).tolist(),
                "nonfinite_runs_per_column": [
                    [[int(run[0]), int(run[-1]) + 1] for run in
                     np.split(indices, np.flatnonzero(np.diff(indices) != 1) + 1) if len(run)]
                    for indices in [np.flatnonzero(~finite[:, i]) for i in range(4)]
                ],
                "all_samples_finite": bool(finite.all()),
                "nominal_2000000_sample_count_matches": len(values) == 2_000_000,
                "statistics_scope": "finite samples only; no imputation; not detector input",
                "column_mean": [float(c.mean()) for c in columns],
                "column_rms": [float(np.sqrt(np.mean(c ** 2))) for c in columns],
                "column_min": [float(c.min()) for c in columns],
                "column_max": [float(c.max()) for c in columns],
            })
            print("Profiled", member.filename, values.shape, flush=True)
    result = {
        "dataset": "5hcdd3tdvb", "version": 6, "archive_sha256": expected,
        "publisher_sha256_verified": True, "csv_members": 129,
        "profiled_members": profiles, "partition": "development",
        "sample_rate_hz_documented": 25600,
        "column_units_documented": ["g", "g", "degree_C", "degree_C"],
        "units_source": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11039934/",
        "all_signal_members_inspected": args.all,
        "all_signal_members_validated": False, "detector_evaluated": False,
        "healthy_exposure_qualified": False,
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
