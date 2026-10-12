"""Local reviewer-assertion ledger; filesystem access is the trust boundary."""
import json
import sqlite3
import uuid
from datetime import datetime, timezone

OUTCOMES = {'confirmed_fault', 'nuisance', 'unresolved'}


class AdjudicationLedger:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.execute('PRAGMA foreign_keys=ON')
        self.db.executescript('''
        CREATE TABLE IF NOT EXISTS reviews (
          id TEXT PRIMARY KEY, subject TEXT NOT NULL, reviewer TEXT NOT NULL,
          outcome TEXT NOT NULL, rationale TEXT NOT NULL, evidence TEXT NOT NULL,
          recorded_at TEXT NOT NULL, supersedes TEXT UNIQUE REFERENCES reviews(id));
        CREATE TRIGGER IF NOT EXISTS reviews_no_update BEFORE UPDATE ON reviews
          BEGIN SELECT RAISE(ABORT, 'append-only reviews'); END;
        CREATE TRIGGER IF NOT EXISTS reviews_no_delete BEFORE DELETE ON reviews
          BEGIN SELECT RAISE(ABORT, 'append-only reviews'); END;
        ''')

    def close(self):
        self.db.close()

    def append(self, subject, reviewer, outcome, rationale, evidence, supersedes=None):
        for value in (subject, reviewer, rationale):
            if not isinstance(value, str) or not value.strip() or len(value)>4096:
                raise ValueError('Nonblank bounded subject, reviewer and rationale required')
        if outcome not in OUTCOMES: raise ValueError('Unknown outcome')
        if not isinstance(evidence,list) or len(evidence)>100 or any(not isinstance(v,str) or not v.strip() or len(v)>2048 for v in evidence):
            raise ValueError('Invalid evidence references')
        if outcome!='unresolved' and not evidence:
            raise ValueError('Resolved assertions require evidence references')
        if supersedes is not None and (not isinstance(supersedes,str) or not supersedes.strip()):
            raise ValueError('Invalid superseded identifier')
        try:
            self.db.execute('BEGIN IMMEDIATE')
            if supersedes is None:
                if self.db.execute('SELECT 1 FROM reviews WHERE subject=?',(subject,)).fetchone():
                    raise ValueError('Existing subject requires an explicit correction')
            else:
                prior=self.db.execute('SELECT subject FROM reviews WHERE id=?',(supersedes,)).fetchone()
                if prior is None or prior[0]!=subject: raise ValueError('Correction subject mismatch or missing original')
                if self.db.execute('SELECT 1 FROM reviews WHERE supersedes=?',(supersedes,)).fetchone():
                    raise ValueError('Correct the latest revision, not a stale revision')
            identifier=str(uuid.uuid4())
            self.db.execute('INSERT INTO reviews VALUES (?,?,?,?,?,?,?,?)',
                (identifier,subject,reviewer,outcome,rationale,json.dumps(evidence),datetime.now(timezone.utc).isoformat(),supersedes))
            self.db.commit()
            return identifier
        except Exception:
            self.db.rollback()
            raise

    def history(self, subject):
        fields=('id','subject','reviewer','outcome','rationale','evidence','recorded_at','supersedes')
        rows=self.db.execute('SELECT * FROM reviews WHERE subject=? ORDER BY rowid',(subject,)).fetchall()
        result=[]
        for row in rows:
            item=dict(zip(fields,row));item['evidence']=json.loads(item['evidence'])
            item['identity_verified']=False;item['evidence_verified']=False
            result.append(item)
        return result
