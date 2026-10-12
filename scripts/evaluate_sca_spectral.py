"""Case-1-only exploratory envelope features; frequency units unresolved."""
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.io import loadmat
from scipy.signal import hilbert

ROOT = Path(__file__).resolve().parents[1]


def feature(x, fs, frequency):
    if not 0 < frequency < fs/2:
        return None
    envelope = np.abs(hilbert(x-np.mean(x)))
    power = np.abs(np.fft.rfft((envelope-envelope.mean())*np.hanning(len(x))))**2
    frequencies = np.fft.rfftfreq(len(x), 1/fs)
    scores = []
    for harmonic in (1, 2, 3):
        center = frequency*harmonic
        width = max(2*fs/len(x), center*0.02)
        if center+4*width >= fs/2:
            continue
        signal = np.abs(frequencies-center) <= width
        background = (np.abs(frequencies-center) > 2*width) & (np.abs(frequencies-center) <= 4*width)
        if signal.any() and background.any():
            scores.append(float(power[signal].mean()/max(power[background].mean(), np.finfo(float).tiny)))
    return float(np.mean(scores)) if scores else None


def main():
    results = []
    source = ROOT/'outputs/reference-dataset-review/sca'
    inventory = json.loads((ROOT/'data/qualification/sca-source-inventory.json').read_text())
    case = next(r for r in inventory['files'] if r['case'] == '1')
    inputs = {}
    for item in case['files']:
        p = source/('case1-'+item['name'])
        assert hashlib.sha256(p.read_bytes()).hexdigest() == item['sha256']
        inputs[item['name']] = loadmat(p, simplify_cells=True)
    # Both interpretations reported, never silently corrected using fault labels.
    for interpretation, divisor in [('documented_Hz_multiple', 60), ('hypothesis_RPM_coefficient', 1)]:
        for placement in ['DS', 'FS']:
            for fault in ['BPFIMultiple', 'BPFOMultiple', 'BPFMultiple']:
                scores = {}
                for name, data in inputs.items():
                    d = data[placement]
                    rows = []
                    for x, fs, rpm, label in zip(d['rawData'],d['samplingRate'],d['RPM'],d['label']):
                        if label == -1 or not np.isfinite(rpm) or rpm <= 0:
                            continue
                        score = feature(x, fs, rpm/divisor*d['faultFrequencies'][fault])
                        if score is not None: rows.append((int(label),score))
                    scores[name] = rows
                normal = [s for label,s in scores['train.mat'] if label == 0]
                threshold = float(np.quantile(normal,0.99))
                rows = scores['test.mat']
                results.append({'frequency_interpretation':interpretation,'placement':placement,'feature':fault,
                    'threshold_train_99percentile':threshold,'train_normal_records':len(normal),
                    'tp':sum(l>0 and s>threshold for l,s in rows), 'fn':sum(l>0 and s<=threshold for l,s in rows),
                    'fp':sum(l==0 and s>threshold for l,s in rows), 'tn':sum(l==0 and s<=threshold for l,s in rows)})
    report = {'scope':'Exploratory case1 development; post-replacement reference; no independent validation',
        'frequency_units_resolved':False,'qualified_detector':False,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'method':'Unfiltered demeaned Hilbert envelope; Hann spectrum; mean harmonic local power contrast; 2% or 2-bin width; per-feature train-normal 99th percentile',
        'results':results}
    (ROOT/'governance/evidence/sca-case1-spectral.json').write_text(json.dumps(report,indent=2)+'\n')
    for r in results: print(json.dumps(r))


if __name__ == '__main__': main()
