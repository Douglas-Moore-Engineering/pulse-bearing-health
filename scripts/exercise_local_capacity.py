"""Bounded synthetic loopback HTTP load; never accepts a remote target or live DB."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing, contextmanager
from datetime import datetime, timezone
import hashlib
import json
import math
import multiprocessing
import os
import queue
from pathlib import Path
import runpy
import sqlite3
import tempfile
import threading
import time
import httpx

from pulse.api import Settings, create_app
from pulse.assessment_store import AssessmentStore


class ReusedConnectionStore(AssessmentStore):
    """Experiment only: bounded, exclusively leased connections; close after workers stop."""
    def __init__(self, path, factory=sqlite3.Connection):
        self.factory = factory
        self.pool = queue.LifoQueue(maxsize=8)
        self.closed = False
        for _ in range(8):
            self.pool.put(None)
        super().__init__(path)

    @contextmanager
    def connect(self):
        if self.closed:
            raise RuntimeError('Experiment store closed')
        db = self.pool.get(timeout=5)
        try:
            if db is None:
                db = sqlite3.connect(self.path, timeout=5, check_same_thread=False, factory=self.factory)
                db.execute('PRAGMA synchronous=FULL')
            with db:
                yield db
        except BaseException:
            # A failed setup/transaction must not return a suspect connection.
            if db is not None:
                try:
                    db.close()
                finally:
                    db = None
            raise
        finally:
            self.pool.put(db)

    def close(self):
        # Caller must first join all request workers; never close a leased connection.
        if self.pool.qsize() != 8:
            raise RuntimeError('Connections still leased')
        self.closed = True
        while not self.pool.empty():
            db = self.pool.get_nowait()
            if db is not None:
                db.close()


def summarize(values):
    values = sorted(values)
    return {'count':len(values),'mean_ms':sum(values)/len(values) if values else None,
            'p50_ms':values[math.ceil(.5*len(values))-1] if values else None,
            'p95_ms':values[math.ceil(.95*len(values))-1] if values else None}


@contextmanager
def process_cpu_samples():
    """Process CPU seconds per wall second; 1.0 is one busy logical CPU."""
    finished = threading.Event()
    samples = []
    def sample():
        wall, cpu = time.perf_counter(), time.process_time()
        origin = wall
        while True:
            done = finished.wait(1)
            now, used = time.perf_counter(), time.process_time()
            samples.append({'elapsed_seconds':now-origin,
                            'cpu_seconds':used-cpu,'wall_seconds':now-wall,
                            'logical_cpu_equivalents':(used-cpu)/(now-wall)})
            wall, cpu = now, used
            if done:
                return
    worker = threading.Thread(target=sample, daemon=True)
    worker.start()
    try:
        yield samples
    finally:
        finished.set()
        worker.join(5)
        if worker.is_alive():
            raise RuntimeError('CPU sampler did not stop')


def api_worker(path, connection, stop, reuse, duration, serialize):
    # Inherited deployment variables must never redirect a synthetic run to live storage.
    for key in list(os.environ):
        if key.startswith('PULSE_'):
            del os.environ[key]
    serve = runpy.run_path(str(Path(__file__).resolve().parents[1]/'tests/recovery_process_probe.py'))['local_http_client']
    save_times = []
    stages = {}
    active = threading.local()
    def record(name, started):
        if getattr(active, 'saving', False):
            stages.setdefault(name, []).append((time.perf_counter()-started)*1000)
    class TimedConnection(sqlite3.Connection):
        def execute(self, sql, *args, **kwargs):
            normalized = sql.strip().upper()
            name = ('begin_immediate' if normalized.startswith('BEGIN IMMEDIATE') else
                    'synchronous_pragma' if normalized.startswith('PRAGMA') else
                    'evidence_insert' if 'INSERT INTO ASSESSMENT_COMMIT_EVIDENCE' in normalized else
                    'receipt_insert' if normalized.startswith('INSERT') else 'select')
            started = time.perf_counter()
            try:
                return super().execute(sql, *args, **kwargs)
            finally:
                record(name, started)
        def __exit__(self, *args):
            started = time.perf_counter()
            try:
                return super().__exit__(*args)
            finally:
                record('transaction_exit', started)
        def close(self):
            started = time.perf_counter()
            try:
                return super().close()
            finally:
                record('connection_close', started)
    class TimedStore(AssessmentStore):
        @contextmanager
        def connect(self):
            # Mirror production boundaries; retain both FULL-synchronous transactions.
            started = time.perf_counter()
            db = sqlite3.connect(self.path, timeout=5, factory=TimedConnection)
            record('connection_open', started)
            try:
                db.execute('PRAGMA synchronous=FULL')
                with db:
                    yield db
            finally:
                db.close()
        def save(self,*args,**kwargs):
            started = time.perf_counter()
            active.saving = True
            try:
                return AssessmentStore.save(self,*args,**kwargs)
            finally:
                save_times.append((time.perf_counter()-started)*1000)
                active.saving = False
    writer_lock = threading.Lock()
    class TimedReusedStore(ReusedConnectionStore):
        def save(self, *args, **kwargs):
            if not serialize:
                return TimedStore.save(self, *args, **kwargs)
            started = time.perf_counter()
            with writer_lock:
                stages.setdefault('writer_lock_wait', []).append((time.perf_counter()-started)*1000)
                return TimedStore.save(self, *args, **kwargs)
    store = TimedReusedStore(path, factory=TimedConnection) if reuse else TimedStore(path)
    app = create_app(Settings('tenant','audience',('client',),asset_grants={'client':('synthetic-capacity',)}),
        lambda _: {'oid':'caller','azp':'client','roles':['Pulse.Assess']}, store=store)
    @app.middleware('http')
    async def diagnostic_duration(request,call_next):
        started = time.perf_counter()
        response = await call_next(request)
        response.headers['X-Pulse-Test-Handler-Ms'] = str((time.perf_counter()-started)*1000)
        return response
    with process_cpu_samples() as cpu_samples, serve(app) as client:
        connection.send(str(client.base_url))
        stop.wait(duration + 60)
    if reuse:
        store.close()
    Path(path).with_suffix('.timings.json').write_text(json.dumps({
        'save':summarize(save_times), 'process_cpu_samples':cpu_samples,
        'operations':{name:summarize(values) for name,values in stages.items()}}))
    connection.close()


@contextmanager
def isolated_server(path, reuse=False, duration=60, serialize=False):
    context = multiprocessing.get_context('spawn')
    receiver, sender = context.Pipe(duplex=False)
    stop = context.Event()
    process = context.Process(target=api_worker, args=(path,sender,stop,reuse,duration,serialize))
    process.start()
    sender.close()
    try:
        if not receiver.poll(20):
            raise RuntimeError('Isolated API startup timed out')
        url = receiver.recv()
        with httpx.Client(base_url=url,timeout=5,trust_env=False) as client:
            yield client
    finally:
        stop.set()
        process.join(10)
        if process.is_alive():
            process.terminate();process.join(5)
        receiver.close()
        if process.exitcode != 0:
            raise RuntimeError('Isolated API did not shut down cleanly')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--reuse-connections', action='store_true', help='Local experimental pool; production unchanged')
    parser.add_argument('--retain-late-slots', action='store_true', help='Submit late slots within existing queue/storage bounds; record schedule delay')
    parser.add_argument('--duration-seconds', type=int, choices=(60,180), default=60)
    parser.add_argument('--serialize-writes', action='store_true')
    args = parser.parse_args()
    if args.serialize_writes and not args.reuse_connections:
        parser.error('--serialize-writes requires --reuse-connections')
    rate, duration = 70, args.duration_seconds
    offered = rate * duration
    payload = {'schema_version':'1','asset_id':'synthetic-capacity',
        'observed_at':datetime.now(timezone.utc).isoformat(),'source_sha256':'a'*64,
        'unit':'g','sample_rate_hz':12800.0,'samples':[-1.0,1.0]*2048}
    results = []
    dropped = 0
    drop_reasons = {'scheduler_late':0,'queue_full':0,'storage_stop':0}
    storage_stop = False
    peak_bytes = 0
    intervals = [{'scheduled_start_seconds':start,'offered':0,'submitted':0,
                  'queue_full_drops':0,'scheduler_late_drops':0,'peak_pending_before_submit':0}
                 for start in range(0,duration,10)]
    with tempfile.TemporaryDirectory(prefix='pulse-capacity-') as directory:
        path = Path(directory)/'receipts.db'
        with isolated_server(path,args.reuse_connections,duration,args.serialize_writes) as client, process_cpu_samples() as client_cpu, ThreadPoolExecutor(max_workers=8) as pool:
            def request(index,enqueued,scheduled):
                started = time.perf_counter()
                timings = {'queue_wait_ms':(started-enqueued)*1000}
                try:
                    body = json.dumps(dict(payload,window_id=f'window-{index}'),ensure_ascii=False,
                                      allow_nan=False,separators=(',',':')).encode()
                    timings['json_prepare_ms'] = (time.perf_counter()-started)*1000
                    sent = time.perf_counter()
                    response = client.post('/v1/degradation/assess', headers={'Authorization':'Bearer synthetic','Content-Type':'application/json'},
                                           content=body)
                    timings['http_roundtrip_ms'] = (time.perf_counter()-sent)*1000
                    timings['server_handler_ms'] = float(response.headers['X-Pulse-Test-Handler-Ms'])
                    ok = response.status_code == 200 and response.json().get('persisted') is True
                    timings['scheduled_to_completion_ms'] = (time.perf_counter()-scheduled)*1000
                    return {'index':index,'ok':ok,'status':response.status_code,'seconds':time.perf_counter()-started,'timings':timings}
                except Exception as error:
                    return {'index':index,'ok':False,'error_type':type(error).__name__,'seconds':time.perf_counter()-started}
            futures, pending = [], set()
            started = time.perf_counter()
            schedule_delays = []
            for index in range(offered):
                scheduled = started + index/rate
                delay = scheduled-time.perf_counter()
                if delay > 0: time.sleep(delay)
                pending = {future for future in pending if not future.done()}
                interval = intervals[index//(rate*10)]
                interval['offered'] += 1
                interval['peak_pending_before_submit'] = max(interval['peak_pending_before_submit'],len(pending))
                size = sum(file.stat().st_size for file in Path(directory).iterdir() if file.is_file())
                peak_bytes = max(peak_bytes,size)
                if size >= 50*1024*1024:
                    storage_stop = True
                    dropped += offered-index
                    drop_reasons['storage_stop'] += offered-index
                    break
                if len(pending)>=32:
                    dropped += 1
                    drop_reasons['queue_full'] += 1
                    interval['queue_full_drops'] += 1
                    continue
                if not args.retain_late_slots and time.perf_counter()-scheduled > 1/rate:
                    dropped += 1
                    drop_reasons['scheduler_late'] += 1
                    interval['scheduler_late_drops'] += 1
                    continue
                enqueued = time.perf_counter()
                schedule_delays.append((enqueued-scheduled)*1000)
                future = pool.submit(request,index,enqueued,scheduled)
                futures.append(future);pending.add(future)
                interval['submitted'] += 1
            results = [future.result() for future in futures]
            elapsed = time.perf_counter()-started
        with closing(sqlite3.connect(path)) as database:
            count = database.execute('SELECT COUNT(*) FROM api_assessments').fetchone()[0]
            integrity = database.execute('PRAGMA integrity_check').fetchone()[0]
            evidence_count = database.execute('SELECT COUNT(*) FROM assessment_commit_evidence').fetchone()[0]
        final_bytes = sum(file.stat().st_size for file in Path(directory).iterdir() if file.is_file())
        peak_bytes = max(peak_bytes,final_bytes)
        succeeded = sum(result['ok'] for result in results)
        latencies = sorted(result['seconds']*1000 for result in results if result['ok'])
        assert count == succeeded == evidence_count and integrity == 'ok'
        for number, interval in enumerate(intervals):
            cohort = [result for result in results if result['index']//(rate*10) == number]
            interval['successful'] = sum(result['ok'] for result in cohort)
            interval['failed'] = len(cohort)-interval['successful']
            interval['timings'] = {key:summarize([result['timings'][key] for result in cohort if result['ok']])
                                  for key in ('queue_wait_ms','server_handler_ms','scheduled_to_completion_ms')}
        report = {'observed_at':datetime.now(timezone.utc).isoformat(),
            'scope':f'{duration}-second synthetic local HTTP/SQLite smoke load; separate API process on shared host, injected identity, no detector or full alert workflow',
            'offered_rps':rate,'scheduled_seconds':duration,'offered_requests':offered,
            'connection_reuse_experiment':args.reuse_connections,
            'serialized_writes_experiment':args.serialize_writes,
            'retain_late_slots':args.retain_late_slots,
            'submission_schedule_delay_ms':summarize(schedule_delays),
            'scheduled_cohorts_10_seconds':intervals,
            'commit_evidence_count':evidence_count,
            'submitted':len(results),'successful':succeeded,'failed':len(results)-succeeded,'dropped':dropped,
            'drop_reasons':drop_reasons,'server_process_isolated':True,
            'timings':{key:summarize([result['timings'][key] for result in results if result['ok']])
                       for key in ('queue_wait_ms','json_prepare_ms','http_roundtrip_ms','server_handler_ms','scheduled_to_completion_ms')},
            'store_save_timing':json.loads(path.with_suffix('.timings.json').read_text())['save'],
            'client_process_cpu_samples':client_cpu,
            'server_process_cpu_samples':json.loads(path.with_suffix('.timings.json').read_text())['process_cpu_samples'],
            'store_operation_timings':json.loads(path.with_suffix('.timings.json').read_text())['operations'],
            'elapsed_seconds':elapsed,'successful_rps':succeeded/elapsed,
            'successful_p95_ms':latencies[math.ceil(.95*len(latencies))-1] if latencies else None,
            'samples_per_request':4096,'persisted_receipt_count':count,'sqlite_integrity':integrity,
            'final_storage_bytes':final_bytes,'peak_sampled_storage_bytes':peak_bytes,'storage_stop':storage_stop,
            'receipt_reconciliation_passed':True,'daily_capacity_qualified':False,
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    report['temporary_storage_removed'] = True
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
