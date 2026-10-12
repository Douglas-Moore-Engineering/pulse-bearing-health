"""Bounded loopback HTTP test; generated signed tokens, no cloud or dataset access."""
import argparse
import asyncio
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import multiprocessing
import socket
import sys
import threading
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
import httpx
import jwt
import uvicorn
from cryptography.hazmat.primitives.asymmetric import rsa
from pulse.api import Settings, EntraVerifier, create_app


def serve(sock, settings, public_jwk, stopped, started):
    verifier = EntraVerifier(settings)
    verifier.keys = {'fixture': jwt.PyJWK.from_json(public_jwk).key}
    verifier.loaded_at = verifier.last_attempt = time.monotonic()
    server = uvicorn.Server(uvicorn.Config(create_app(settings, verifier), log_level='error',
                                          access_log=False, limit_concurrency=128))
    def watch():
        while not server.started:
            time.sleep(.05)
        started.set()
        stopped.wait()
        server.should_exit = True
    threading.Thread(target=watch, daemon=True).start()
    server.run(sockets=[sock])


async def exercise(urls, token, rate, seconds, samples):
    payload = {'schema_version': '1', 'asset_id': 'generated-fixture', 'window_id': 'fixture',
               'observed_at': datetime.now(timezone.utc).isoformat(), 'source_sha256': 'a'*64,
               'unit': 'g', 'sample_rate_hz': 25600.0, 'samples': [-.1, .1]*(samples//2)}
    body = json.dumps(payload)
    latencies, failures, dropped, inflight = [], 0, 0, set()
    async with httpx.AsyncClient(timeout=5, limits=httpx.Limits(max_connections=128),
                                 headers={'Authorization': 'Bearer '+token, 'Content-Type': 'application/json'}) as client:
        async def one(index):
            nonlocal failures
            start = time.perf_counter()
            try:
                response = await client.post(urls[index % len(urls)]+'/v1/degradation/assess', content=body)
                if response.status_code != 200 or response.json().get('alert_status') != 'unavailable':
                    failures += 1
            except (httpx.HTTPError, ValueError):
                failures += 1
            latencies.append(time.perf_counter()-start)
        start = time.perf_counter()
        for i in range(int(rate*seconds)):
            await asyncio.sleep(max(0, start+i/rate-time.perf_counter()))
            if len(inflight) >= 128 or time.perf_counter() > start+seconds:
                dropped += 1
                continue
            task = asyncio.create_task(one(i)); inflight.add(task); task.add_done_callback(inflight.discard)
        await asyncio.gather(*inflight)
        elapsed = time.perf_counter()-start
    ordered = sorted(latencies)
    p95 = ordered[min(len(ordered)-1, int(len(ordered)*.95))] if ordered else None
    return {'offered_rps': rate, 'duration_seconds': seconds, 'elapsed_seconds': elapsed,
            'request_bytes': len(body.encode()), 'samples': samples, 'completed': len(latencies),
            'failed': failures, 'dropped': dropped, 'achieved_rps': len(latencies)/elapsed,
            'p95_ms': p95*1000 if p95 is not None else None,
            'provisional_check_passed': p95 is not None and p95 < .5 and
                (failures+dropped)/max(1, rate*seconds) < .001 and len(latencies)/elapsed >= rate*.99}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--seconds', type=int, default=20)
    parser.add_argument('--replicas', type=int, choices=(1, 3), default=1)
    args = parser.parse_args()
    if not 5 <= args.seconds <= 120:
        parser.error('seconds must be between 5 and 120')
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    settings = Settings('00000000-0000-0000-0000-000000000001', 'fixture-api', ('fixture-client',))
    now = int(time.time())
    token = jwt.encode({'iss': settings.issuer, 'aud': settings.audience, 'tid': settings.tenant,
                        'ver': '2.0', 'oid': 'fixture', 'azp': 'fixture-client', 'roles': ['Pulse.Assess'],
                        'iat': now, 'nbf': now, 'exp': now+1800}, private, algorithm='RS256', headers={'kid': 'fixture'})
    servers, urls = [], []
    for _ in range(args.replicas):
        sock = socket.socket(); sock.bind(('127.0.0.1', 0)); port = sock.getsockname()[1]
        stopped, started = multiprocessing.Event(), multiprocessing.Event()
        process = multiprocessing.Process(target=serve, args=(sock, settings,
            jwt.algorithms.RSAAlgorithm.to_jwk(private.public_key()), stopped, started))
        process.start(); servers.append((process, sock, stopped, started)); urls.append(f'http://127.0.0.1:{port}')
    try:
        if not all(started.wait(15) for _, _, _, started in servers): raise RuntimeError('Local server startup failed')
        results = []
        for rate, samples in [(70, 4096), (174, 4096), (350, 4096)]:
            result = asyncio.run(exercise(urls, token, rate, args.seconds, samples))
            results.append(result); print(json.dumps(result), flush=True)
        report = {'recorded_at': datetime.now(timezone.utc).isoformat(), 'runtime': platform.platform(),
                  'python': platform.python_version(), 'replicas': args.replicas,
                  'scope': 'Separate API and load-generator processes over loopback; round-robin client; generated RS256 tokens and signals',
                  'limitations': ['No AKS/container resource limits, TLS, ingress or remote identity-key retrieval',
                                  'No model, durable persistence or notification delivery',
                                  'Load generator shares host with server; not a six-hour soak'],
                  'api_source_sha256': hashlib.sha256(Path('src/pulse/api.py').read_bytes()).hexdigest(), 'stages': results}
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    finally:
        for process, sock, stopped, _ in servers:
            stopped.set(); process.join(timeout=10)
            if process.is_alive(): process.terminate(); process.join()
            sock.close()


if __name__ == '__main__': main()
