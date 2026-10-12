import pytest
from pulse.alert_ledger import AlertLedger,AlertConflict
from pulse.trailing_median import TrailingMedian

def test_detector_clear_and_gap_never_close_incident(tmp_path):
 ledger=AlertLedger(tmp_path/'alerts.db');event=ledger.record('t','a','episode','policy',{})
 detector=TrailingMedian([1],window=1,persistence=1)
 assert detector.update(0,[2])['flagged']
 assert not detector.update(1,[1])['flagged']
 assert ledger.incident_state('t','a',event)=='OPEN'
 assert detector.update(902,[1])['available']
 assert ledger.incident_state('t','a',event)=='OPEN'
 with pytest.raises(AlertConflict):ledger.close_incident('t','a',event,'actor','done',['fixture'])
 ledger.acknowledge('t','a',event,'actor')
 assert ledger.incident_state('t','a',event)=='ACKNOWLEDGED'
 closed=ledger.close_incident('t','a',event,'actor','Synthetic disposition',['fixture'])
 restarted=AlertLedger(tmp_path/'alerts.db')
 assert restarted.incident_state('t','a',event)=='CLOSED'
 assert restarted.close_incident('t','a',event,'actor','Synthetic disposition',['fixture'])==closed
 with pytest.raises(AlertConflict):restarted.close_incident('t','a',event,'actor','changed',['fixture'])
 with pytest.raises(KeyError):restarted.incident_state('other','a',event)
 with pytest.raises(KeyError):restarted.close_incident('t','other',event,'actor','done',['fixture'])
 new=ledger.record('t','a','new-episode','policy',{})
 assert ledger.incident_state('t','a',new)=='OPEN'

def test_closure_requires_evidence_and_cannot_be_rewritten(tmp_path):
 import sqlite3
 ledger=AlertLedger(tmp_path/'alerts.db');event=ledger.record('t','a','e','p',{})
 ledger.acknowledge('t','a',event,'actor')
 with pytest.raises(ValueError):ledger.close_incident('t','a',event,'actor','done',[])
 ledger.close_incident('t','a',event,'actor','done',['fixture'])
 with pytest.raises(sqlite3.IntegrityError):
  with ledger.connection() as db:db.execute('DELETE FROM alert_closures')
