import csv
import hashlib

import pytest

np = pytest.importorskip('numpy')
scipy_io = pytest.importorskip('scipy.io')
from pulse.ldm import profile_b02


@pytest.fixture
def sample(tmp_path):
    (tmp_path/'B02_log.pdf').write_bytes(b'generated fixture calibration reference; not a real PDF')
    contexts = {
        'B02_operatingConditions.csv': ['Time','setDynLoad / N','peak_dynLoad / N','setStatLoad / N','meanAbs_statLoad / N','setSpeed / rpm','meanAbs_speed / rpm'],
        'B02_meanTemperatures.csv': ['Time','Mean Abs. Temp. T1 / °C','Mean Abs. Temp. T2 / °C','Mean Room Temp. / °C'],
    }
    for name, fields in contexts.items():
        with (tmp_path/name).open('w',encoding='utf-8',newline='') as f:
            writer=csv.writer(f);writer.writerow(fields)
            for timestamp in ['25-Oct-2021 08:59:35','25-Oct-2021 09:04:17']:
                writer.writerow([timestamp]+[750]*(len(fields)-1))
    values=np.ones((204800,1))*0.1
    times=(np.arange(204800)/128000).reshape(-1,1)
    scipy_io.savemat(tmp_path/'data_B02_M0001.mat',{'accHorizRear_A':values,'accHorizFrontal_C':values,'measTime':times})
    manifest={'dataset_id':'DS-LDM-UPB-RTF','record_id':10868257,'doi':'10.5281/zenodo.10868257','title':'Generated test fixture','license':{'id':'cc-by-4.0'},'b02_inspection':{'calibration':{'sample_rate_hz':128000,'g_per_volt':10,'duration_seconds':1.6,'gain_db':0},'csv_time_profile':{'rows_per_csv':2},'selected_members':[]}}
    for p in tmp_path.iterdir():
        manifest['b02_inspection']['selected_members'].append({'member':'B02/'+p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    return tmp_path,manifest


def rehash(folder,manifest,name):
    member=next(x for x in manifest['b02_inspection']['selected_members'] if x['member'].endswith('/'+name))
    raw=(folder/name).read_bytes();member.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def test_sample_calibration_lineage_and_abstention(sample):
    folder,manifest=sample
    report=profile_b02(folder,manifest)
    assert report['training_qualified'] is False
    assert report['timestamp_gap_seconds']['max']==282
    assert len(report['records'])==2
    for row in report['records']:
        assert row['features']['rms_m_s2']==pytest.approx(9.80665)
        assert row['rul_hours'] is None and row['fault_label'] is None
        assert row['source_timezone'] is None
        assert row['regime_flag']=='warmup_or_low_speed'
        assert len(row['native_source_sha256'])==64


def test_native_tamper_denied_before_parsing(sample):
    folder,manifest=sample
    (folder/'data_B02_M0001.mat').write_bytes(b'tampered')
    with pytest.raises(ValueError,match='digest'):
        profile_b02(folder,manifest)


def test_unreviewed_calibration_rejected(sample):
    folder,manifest=sample
    manifest['b02_inspection']['calibration']['g_per_volt']=1
    with pytest.raises(ValueError,match='Calibration'):
        profile_b02(folder,manifest)


def test_context_mismatch_rejected(sample):
    folder,manifest=sample
    name='B02_meanTemperatures.csv'
    p=folder/name;p.write_text(p.read_text(encoding='utf-8').replace('09:04:17','09:04:18'),encoding='utf-8')
    rehash(folder,manifest,name)
    with pytest.raises(ValueError,match='timelines'):
        profile_b02(folder,manifest)


@pytest.mark.parametrize('mutation',['time_rate','nonfinite','matrix'])
def test_invalid_waveform_rejected(sample,mutation):
    folder,manifest=sample
    name='data_B02_M0001.mat';data=scipy_io.loadmat(folder/name)
    if mutation=='time_rate': data['measTime']*=2
    elif mutation=='nonfinite': data['accHorizRear_A'][0,0]=np.nan
    else: data['accHorizRear_A']=np.zeros((400,512))
    scipy_io.savemat(folder/name,{k:v for k,v in data.items() if not k.startswith('__')})
    rehash(folder,manifest,name)
    with pytest.raises(ValueError):profile_b02(folder,manifest)
