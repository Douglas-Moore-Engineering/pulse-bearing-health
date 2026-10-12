"""Native adapter for the inspected LDM-UPB B02 sample, not a training dataset."""
from __future__ import annotations

import csv
from datetime import datetime
import hashlib
import math
from pathlib import Path
import re
import statistics

import numpy as np
from scipy.io import loadmat

from pulse.core import features

MONTHS = {name: i + 1 for i, name in enumerate(
    ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))}


def local_timestamp(value):
    match = re.fullmatch(r'(\d{2})-([A-Za-z]{3})-(\d{4}) (\d{2}):(\d{2}):(\d{2})', value)
    if not match or match[2] not in MONTHS:
        raise ValueError('Unrecognized source timestamp; no UTC timezone may be inferred')
    return datetime(int(match[3]), MONTHS[match[2]], int(match[1]),
                    int(match[4]), int(match[5]), int(match[6]))


def profile_b02(source_dir, manifest):
    """Verify and profile only members pinned in the reviewed B02 sample manifest.

    This separate source-adapter product does not admit data to the JSON-window
    store or approve a dataset/model. It preserves native-file hashes and avoids
    manufacturing operational labels or UTC timestamps.
    """
    if manifest.get('dataset_id') != 'DS-LDM-UPB-RTF' or manifest.get('record_id') != 10868257:
        raise ValueError('Unexpected dataset/record; adapter scope is the reviewed B02 sample')
    inspection = manifest['b02_inspection']
    calibration = inspection['calibration']
    rate = float(calibration['sample_rate_hz'])
    factor = float(calibration['g_per_volt'])
    duration = float(calibration['duration_seconds'])
    if (rate, factor, duration, calibration['gain_db']) != (128000.0, 10.0, 1.6, 0):
        raise ValueError('Calibration differs from the reviewed B02 log')
    folder = Path(source_dir).resolve()
    members = {}
    for entry in inspection['selected_members']:
        name = Path(entry['member']).name
        if name in members:
            raise ValueError('Ambiguous duplicate member basename')
        path = (folder / name).resolve()
        if path.parent != folder or not path.is_file():
            raise ValueError('Missing member or path outside source folder')
        if path.stat().st_size > 12_000_000:
            raise ValueError('Member exceeds bounded inspection size')
        raw = path.read_bytes()
        if len(raw) != entry['bytes'] or hashlib.sha256(raw).hexdigest() != entry['sha256']:
            raise ValueError('Native member digest or size mismatch: ' + name)
        members[name] = (path, entry['sha256'])
    for required in ('B02_log.pdf', 'B02_operatingConditions.csv', 'B02_meanTemperatures.csv'):
        if required not in members:
            raise ValueError('Missing required calibration/context member')

    def read_context(name, required):
        with members[name][0].open(encoding='utf-8-sig', newline='') as stream:
            reader = csv.DictReader(stream)
            if reader.fieldnames is None or set(reader.fieldnames) != set(required) or len(reader.fieldnames) != len(required):
                raise ValueError('Unexpected source CSV header: ' + name)
            rows = list(reader)
        if len(rows) < 2:
            raise ValueError('Source context requires at least two timestamps')
        for row in rows:
            if None in row or any(value is None for value in row.values()):
                raise ValueError('Malformed CSV row')
            for key in required:
                if key != 'Time' and not math.isfinite(float(row[key])):
                    raise ValueError('Nonfinite source context')
        times = [local_timestamp(row['Time']) for row in rows]
        if any(b <= a for a, b in zip(times, times[1:])):
            raise ValueError('Source timestamps must be unique and increasing')
        return rows, times

    operating, times = read_context('B02_operatingConditions.csv', (
        'Time', 'setDynLoad / N', 'peak_dynLoad / N', 'setStatLoad / N',
        'meanAbs_statLoad / N', 'setSpeed / rpm', 'meanAbs_speed / rpm'))
    temperatures, temperature_times = read_context('B02_meanTemperatures.csv', (
        'Time', 'Mean Abs. Temp. T1 / °C', 'Mean Abs. Temp. T2 / °C', 'Mean Room Temp. / °C'))
    if times != temperature_times or len(times) != inspection['csv_time_profile']['rows_per_csv']:
        raise ValueError('CSV timelines or expected row counts differ')
    gaps = [(b-a).total_seconds() for a, b in zip(times, times[1:])]
    outputs = []
    mat_names = sorted(name for name in members if name.endswith('.mat'))
    if not mat_names:
        raise ValueError('No pinned MAT samples')
    for name in mat_names:
        match = re.fullmatch(r'data_B02_M(\d{4,})\.mat', name)
        if not match or not 1 <= int(match[1]) <= len(times):
            raise ValueError('Measurement identity outside reviewed B02 timeline')
        ordinal = int(match[1])
        data = loadmat(members[name][0])
        required = ('accHorizRear_A', 'accHorizFrontal_C', 'measTime')
        arrays = {}
        for key in required:
            if key not in data:
                raise ValueError('Missing MAT variable: ' + key)
            value = np.asarray(data[key])
            if value.ndim != 2 or 1 not in value.shape or value.dtype.kind not in 'fi':
                raise ValueError('Expected numeric MAT vector: ' + key)
            value = value.reshape(-1).astype(float)
            if len(value) != round(rate * duration) or not np.isfinite(value).all():
                raise ValueError('Invalid MAT length or nonfinite samples: ' + key)
            arrays[key] = value
        sample_times = arrays['measTime']
        if abs(sample_times[0]) > 1e-10 or not np.allclose(np.diff(sample_times), 1/rate, rtol=1e-7, atol=1e-12):
            raise ValueError('MAT sample time does not match reviewed sampling rate')
        context = operating[ordinal-1]
        warmup = float(context['setSpeed / rpm']) < 1500
        for channel in required[:2]:
            acceleration_g = arrays[channel] * factor
            if np.max(np.abs(acceleration_g)) > 50:
                raise ValueError('Sample exceeds documented accelerometer measurement range')
            outputs.append({
                'dataset_id': manifest['dataset_id'], 'bearing_id': 'B02',
                'measurement_id': match[1], 'channel': channel,
                'native_source_sha256': members[name][1],
                'calibration_log_sha256': members['B02_log.pdf'][1],
                'operating_conditions_sha256': members['B02_operatingConditions.csv'][1],
                'temperature_table_sha256': members['B02_meanTemperatures.csv'][1],
                'sample_rate_hz': rate, 'sample_count': len(acceleration_g),
                'original_unit': 'V', 'g_per_volt': factor,
                'source_timestamp': context['Time'], 'source_timezone': None,
                'elapsed_wall_clock_seconds': (times[ordinal-1]-times[0]).total_seconds(),
                'context_join_basis': 'Measurement ordinal to CSV row; candidate mapping, full-run verification pending',
                'regime_flag': 'warmup_or_low_speed' if warmup else 'main_test_speed_range',
                'set_speed_rpm': float(context['setSpeed / rpm']),
                'features': features(acceleration_g, 'g'),
                'fault_label': None, 'rul_hours': None, 'site_validated': False,
            })
    return {
        'adapter_version': 'ldm-b02-sample-0.1', 'status': 'PARTIAL_INSPECTION_ONLY',
        'license': manifest['license'], 'attribution': {'creator': 'Osarenren Kennedy Aimiyekagbon',
            'dataset_doi': manifest['doi'], 'title': manifest['title'],
            'license_url': 'https://creativecommons.org/licenses/by/4.0/',
            'changes': 'Selected members profiled; voltage converted using B02 log; RMS/kurtosis computed'},
        'full_archive_checksum_verified': False, 'training_qualified': False,
        'site_validated': False, 'context_rows': len(times),
        'timestamp_gap_seconds': {'min': min(gaps), 'median': statistics.median(gaps), 'max': max(gaps)},
        'records': outputs,
    }
