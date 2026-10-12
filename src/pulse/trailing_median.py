"""Fixed-reference trailing median anomaly experiment; no health diagnosis."""
from collections import deque
import math
from statistics import median

class TrailingMedian:
    def __init__(self, references, window=15, threshold=1.5, persistence=3, max_gap=900):
        if not references or any(not math.isfinite(x) or x<=0 for x in references):raise ValueError('Positive finite references required')
        if type(window) is not int or window<1 or type(persistence) is not int or persistence<1:raise ValueError('Invalid window or persistence')
        if not math.isfinite(threshold) or threshold<=0 or not math.isfinite(max_gap) or max_gap<=0:raise ValueError('Invalid threshold or gap')
        self.references=tuple(references);self.buffers=[deque(maxlen=window) for _ in references]
        self.streak=[0]*len(references);self.last=None
        self.window=window;self.threshold=threshold;self.persistence=persistence;self.max_gap=max_gap
    def update(self,timestamp,values):
        if not math.isfinite(timestamp) or (self.last is not None and timestamp<=self.last):raise ValueError('Increasing finite timestamp required')
        if len(values)!=len(self.references) or any(not math.isfinite(v) or v<0 for v in values):raise ValueError('Invalid features')
        if self.last is not None and timestamp-self.last>self.max_gap:
            for b in self.buffers:b.clear()
            self.streak=[0]*len(self.references)
        self.last=timestamp
        for i,(b,v,ref) in enumerate(zip(self.buffers,values,self.references)):
            b.append(v/ref)
            self.streak[i]=self.streak[i]+1 if len(b)==self.window and median(b)>self.threshold else 0
        ready=all(len(b)==self.window for b in self.buffers)
        return {'available':ready,'flagged':any(s>=self.persistence for s in self.streak) if ready else None}
