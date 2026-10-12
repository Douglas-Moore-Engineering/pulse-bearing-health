"""Offline intake checks. Reference strings are not proof of permission."""
import math
from jsonschema import Draft202012Validator, FormatChecker

REFERENCES = ('asset_id', 'sensor_id', 'calibration_ref', 'data_use_ref', 'provenance_ref')


def validate_intake(document, window_schema):
    reasons = []
    if not isinstance(document, dict):
        return {'status': 'REJECTED', 'reasons': ['INVALID_ENVELOPE']}
    if set(document) != {'metadata', 'window'}:
        reasons.append('INVALID_ENVELOPE_FIELDS')
    metadata = document.get('metadata')
    if not isinstance(metadata, dict):
        reasons.append('INVALID_METADATA')
    else:
        if set(metadata) != set(REFERENCES): reasons.append('INVALID_METADATA_FIELDS')
        for name in REFERENCES:
            value = metadata.get(name)
            if not isinstance(value, str) or not value.strip() or len(value) > 256:
                reasons.append('INVALID_'+name.upper())
    window = document.get('window')
    validator = Draft202012Validator(window_schema, format_checker=FormatChecker())
    if not validator.is_valid(window):
        reasons.append('WINDOW_SCHEMA_INVALID')
    if isinstance(window, dict):
        values = window.get('samples')
        if isinstance(values, list):
            if len(values) > 1000000: reasons.append('WINDOW_TOO_LARGE')
            if any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) for v in values):
                reasons.append('NONFINITE_OR_INVALID_SAMPLES')
        rate=window.get('sample_rate_hz')
        if isinstance(rate,(int,float)) and not math.isfinite(rate): reasons.append('NONFINITE_SAMPLE_RATE')
        # Initial customer intake supports explicit UTC windows only.
        if window.get('time_basis') != 'utc': reasons.append('UTC_TIMESTAMP_REQUIRED')
        timestamp=window.get('timestamp_utc','')
        if not isinstance(timestamp,str) or not timestamp.endswith(('Z','+00:00')):
            reasons.append('UTC_OFFSET_REQUIRED')
        for name in ('dataset_id','bearing_id','run_id','window_id'):
            if not isinstance(window.get(name),str) or not window[name].strip():
                reasons.append('INVALID_'+name.upper())
    return {'status':'REJECTED' if reasons else 'STRUCTURALLY_VALID_PENDING_REVIEW',
            'reasons':sorted(set(reasons)), 'permission_verified':False,
            'calibration_verified':False, 'source_hash_verified':False,
            'detector_qualified':False}
