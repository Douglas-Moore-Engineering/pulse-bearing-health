"""Profile the complete verified UNSW development experiment; no detector fitting."""
import argparse
import hashlib
import json
from pathlib import Path
import re

import numpy as np
from scipy.io import loadmat


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    paths = sorted(args.source.rglob("*.mat"))
    if len(paths) != 108:
        raise ValueError("Expected all 108 Test 1 MAT files")
    rows = []
    for path in paths:
        match = re.fullmatch(r"vib_(\d+)_(\d+)\.mat", path.name)
        if not match:
            raise ValueError("Unrecognized native filename")
        raw = path.read_bytes()
        data = loadmat(path)
        rate = float(np.asarray(data["Fs"]).item())
        if rate != 51200:
            raise ValueError("Unexpected sample rate")
        row = {"member": path.relative_to(args.source).as_posix(),
               "sha256": hashlib.sha256(raw).hexdigest(),
               "shaft_cycle": int(match[1]), "shaft_speed_hz": int(match[2]),
               "sample_rate_hz": rate}
        for name in ("accH", "accV", "enc1", "enc2", "loadCell", "tacho"):
            values = np.asarray(data[name])
            if values.shape != (614400, 1) or not np.isfinite(values).all():
                raise ValueError(f"Invalid native channel: {path.name}/{name}")
            if name in ("accH", "accV"):
                row[name + "_rms_volts"] = float(np.sqrt(np.mean(values ** 2)))
        row["samples"] = 614400
        row["duration_seconds"] = 614400 / rate
        rows.append(row)
    result = {"dataset": "h4df4mgrfb", "version": 3, "experiment": "Test 1",
              "partition": "development", "measurements": rows,
              "native_channels_finite": True, "detector_evaluated": False,
              "calibration_nominal_m_s2_per_volt": 100,
              "acquisition_gain_verified": False,
              "wall_clock_timestamps_available": False,
              "healthy_exposure_qualified": False}
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Validated", len(rows), "native MAT measurements", flush=True)


if __name__ == "__main__":
    main()
