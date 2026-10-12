import sqlite3
import pytest
from pulse.adjudication import AdjudicationLedger

def test_corrections_preserve_original_and_survive_reopen(tmp_path):
    path=tmp_path/'reviews.db';ledger=AdjudicationLedger(path)
    first=ledger.append('alert-1','synthetic-reviewer','unresolved','Inspection pending',[])
    second=ledger.append('alert-1','synthetic-reviewer','nuisance','Inspection found no bearing damage',['fixture:inspection'],first)
    ledger.close();ledger=AdjudicationLedger(path)
    rows=ledger.history('alert-1')
    assert [r['outcome'] for r in rows]==['unresolved','nuisance']
    assert rows[1]['supersedes']==first and rows[1]['id']==second
    assert not rows[1]['identity_verified'] and not rows[1]['evidence_verified']
    ledger.close()

def test_stale_and_cross_subject_corrections_rejected(tmp_path):
    ledger=AdjudicationLedger(tmp_path/'reviews.db')
    first=ledger.append('a','r','unresolved','pending',[])
    ledger.append('a','r','unresolved','still pending',[],first)
    for subject,prior in [('a',first),('b',first),('b','missing'),('a',None)]:
        with pytest.raises(ValueError):ledger.append(subject,'r','unresolved','pending',[],prior)
    assert len(ledger.history('a'))==2
    ledger.close()

def test_resolved_assertion_requires_evidence(tmp_path):
    ledger=AdjudicationLedger(tmp_path/'reviews.db')
    with pytest.raises(ValueError):ledger.append('a','r','confirmed_fault','claimed',[])
    assert ledger.history('a')==[]
    ledger.close()

def test_database_rejects_in_place_mutation(tmp_path):
    ledger=AdjudicationLedger(tmp_path/'reviews.db')
    ledger.append('a','r','unresolved','pending',[])
    for sql in ["UPDATE reviews SET outcome='nuisance'",'DELETE FROM reviews']:
        with pytest.raises(sqlite3.IntegrityError):ledger.db.execute(sql)
        ledger.db.rollback()
    assert ledger.history('a')[0]['outcome']=='unresolved'
    ledger.close()
