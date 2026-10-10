"""Offline consistency review; no cloud calls, runtime tests or gate approval."""
from pathlib import Path
import csv
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
checks = []

def rows(name):
    with (ROOT / name).open(newline='') as f:
        return list(csv.DictReader(f))

requirements = rows('requirements/requirements.csv')
ids = {r['Requirement_ID'] for r in requirements}
if len(ids) != len(requirements):
    errors.append('Duplicate requirement IDs')
for r in requirements:
    for field in ['Statement', 'Source', 'Component', 'Verification_Method', 'Acceptance_Criterion', 'Gate', 'Owner']:
        if not r[field].strip():
            errors.append(f"Missing {field}: {r['Requirement_ID']}")
trace = rows('requirements/traceability.csv')
vv = rows('governance/verification_validation_matrix.csv')
if {r['Requirement_ID'] for r in trace} != ids:
    errors.append('Traceability requirement coverage mismatch')
if {r['Requirement_ID'] for r in vv} != ids:
    errors.append('V&V requirement coverage mismatch')
if {r['Test_ID'] for r in trace} != {r['Test_ID'] for r in vv}:
    errors.append('Trace/V&V test-ID mismatch')
derived = rows('requirements/functional_requirements.csv') + rows('requirements/nonfunctional_requirements.csv')
if sorted(derived, key=lambda r:r['Requirement_ID']) != sorted(requirements, key=lambda r:r['Requirement_ID']):
    errors.append('Derived requirements differ from authoritative register')
checks.append({'check':'requirement and V&V referential integrity','count':len(ids)})

link_count = 0
for p in ROOT.rglob('*.md'):
    for target in re.findall(r'\]\(([^)]+)\)', p.read_text()):
        if target.startswith(('https:', 'http:', 'mailto:', '#')):
            continue
        target = target.split('#')[0]
        generated_report = ROOT / 'governance/evidence/design-validation.json'
        if target and not (p.parent / target).resolve().exists() and (p.parent / target).resolve() != generated_report:
            errors.append(f'Broken link {p.relative_to(ROOT)} -> {target}')
        link_count += 1
checks.append({'check':'local Markdown links exist','count':link_count})

for p in ROOT.rglob('*.json'):
    try:
        json.loads(p.read_text())
    except Exception as exc:
        errors.append(f'JSON parse failure {p.relative_to(ROOT)}: {exc}')
checks.append({'check':'JSON syntax','scope':'Includes draft contracts; not schema runtime validation'})

for r in rows('architecture/architecture_viewpoints.csv'):
    source = ROOT / r['View']
    if not source.exists():
        errors.append(f"Missing viewpoint source {r['View']}")
    for rid in r['Requirements'].split(';'):
        if rid not in ids:
            errors.append(f'Unknown diagram requirement {rid}')
    for ext in ['.svg', '.png']:
        if not source.with_suffix(ext).exists():
            errors.append(f'Missing rendered preview {source.with_suffix(ext).name}')
checks.append({'check':'view sources, requirement references and rendered exports exist','count':10})

for r in rows('governance/cloud_entry_criteria.csv'):
    if r['Status'] != 'BLOCKED':
        errors.append(f"Unexpected cloud entry state {r['Criterion_ID']}")
if 'Stop before any Azure connection or provisioning' not in (ROOT/'README.md').read_text():
    errors.append('Missing root stop boundary')
checks.append({'check':'design-only boundary retained','scope':'Documentation consistency; not technical enforcement'})

digests = {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
           for p in sorted(ROOT.rglob('*')) if p.is_file()
           and p.relative_to(ROOT).as_posix() not in ['governance/evidence/design-validation.json']
           and '.git' not in p.parts and '__pycache__' not in p.parts}
report = {'package':'Pulse pre-Azure v0.1','result':'PASS' if not errors else 'FAIL',
          'scope':'Offline design consistency only; no runtime V&V, independent assurance or cloud gate approval',
          'checks':checks,'errors':errors,'artifact_sha256':digests}
output = ROOT/'governance/evidence/design-validation.json'
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps({'result':report['result'],'checks':checks,'errors':errors},indent=2))
sys.exit(bool(errors))
