"""Local-only synthetic application recovery helper, invoked by recovery tests."""
import json
import os
from pathlib import Path
import runpy
import subprocess
import uuid
from urllib.parse import urlparse

import yaml


def exercise(image, database, fixture, probe):
    namespace = 'pulse-app-recovery-' + uuid.uuid4().hex[:10]
    def call(*args, data=None):
        result = subprocess.run(['kubectl', '--context', 'docker-desktop', '--request-timeout=60s',
            *args], input=data, capture_output=True, timeout=65)
        if result.returncode:
            raise RuntimeError(result.stderr.decode())
        return result.stdout.decode()
    config = json.loads(call('config', 'view', '--minify', '-o', 'json'))
    if urlparse(config['clusters'][0]['cluster']['server']).hostname not in ('127.0.0.1', 'localhost', '::1'):
        raise RuntimeError('Only loopback Kubernetes is allowed')
    def pod(name):
        return {'apiVersion': 'v1', 'kind': 'Pod', 'metadata': {'name': name, 'namespace': namespace},
            'spec': {'restartPolicy': 'Never', 'terminationGracePeriodSeconds': 1, 'automountServiceAccountToken': False,
                'securityContext': {'runAsUser': 10001, 'runAsGroup': 10001, 'fsGroup': 10001,
                    'runAsNonRoot': True, 'seccompProfile': {'type': 'RuntimeDefault'}},
                'containers': [{'name': 'api', 'image': image, 'imagePullPolicy': 'Never',
                    'command': ['python', '-c', 'import time; time.sleep(600)'],
                    'securityContext': {'readOnlyRootFilesystem': True, 'allowPrivilegeEscalation': False,
                        'capabilities': {'drop': ['ALL']}},
                    'resources': {'limits': {'cpu': '1', 'memory': '512Mi'}},
                    'volumeMounts': [{'name': 'data', 'mountPath': '/data'}]}],
                'volumes': [{'name': 'data', 'persistentVolumeClaim': {'claimName': 'receipts'}}]}}
    def apply(document):
        call('apply', '-f', '-', data=yaml.safe_dump(document).encode())
    def upload(name, path, data):
        call('-n', namespace, 'exec', '-i', name, '--', 'python', '-c',
             'import sys; from pathlib import Path; Path(sys.argv[1]).write_bytes(sys.stdin.buffer.read())',
             path, data=data)
    try:
        apply({'apiVersion': 'v1', 'kind': 'Namespace', 'metadata': {'name': namespace,
            'labels': {'pod-security.kubernetes.io/enforce': 'restricted'}}})
        apply({'apiVersion': 'v1', 'kind': 'PersistentVolumeClaim',
            'metadata': {'name': 'receipts', 'namespace': namespace},
            'spec': {'storageClassName': 'standard', 'accessModes': ['ReadWriteOnce'],
                'resources': {'requests': {'storage': '16Mi'}}}})
        apply(pod('restore'))
        call('-n', namespace, 'wait', '--for=condition=Ready', 'pod/restore', '--timeout=45s')
        upload('restore', '/data/restored.db', database.read_bytes())
        upload('restore', '/data/fixture.json', fixture.read_bytes())
        call('-n', namespace, 'delete', 'pod', 'restore', '--wait=true', '--timeout=40s')
        apply(pod('recovered'))
        call('-n', namespace, 'wait', '--for=condition=Ready', 'pod/recovered', '--timeout=45s')
        result = json.loads(call('-n', namespace, 'exec', 'recovered', '--', 'python', '-c',
            probe.read_text(), '/data/fixture.json', '/data/restored.db'))
        if result['result'] != 'PASS':
            raise RuntimeError('Recovered application probe failed')
        call('-n', namespace, 'exec', 'recovered', '--', 'python', '-c',
            'import sqlite3; a=sqlite3.connect("/data/restored.db"); b=sqlite3.connect("/data/assessments.db"); a.backup(b); b.close(); a.close()')
        call('-n', namespace, 'delete', 'pod', 'recovered', '--wait=true', '--timeout=40s')
        render = runpy.run_path(str(Path(__file__).resolve().parent / 'render_single_node_manifests.py'))['render']
        documents = render(image, '00000000-0000-0000-0000-000000000001',
            '00000000-0000-0000-0000-000000000002',
            ['00000000-0000-0000-0000-000000000003'], pilot_components=True)
        for document in documents:
            if document['kind'] not in ('ServiceAccount', 'ConfigMap', 'Deployment', 'Service'):
                continue
            document['metadata']['namespace'] = namespace
            if document['kind'] == 'Deployment':
                document['spec']['template']['spec']['volumes'][0]['persistentVolumeClaim']['claimName'] = 'receipts'
            apply(document)
        previous_uid = None
        for iteration in range(2):
            call('-n', namespace, 'rollout', 'status', 'deployment/pulse-api', '--timeout=45s')
            pods = json.loads(call('-n', namespace, 'get', 'pods', '-l', 'app=pulse-api', '-o', 'json'))['items']
            current = next(p for p in pods if not p['metadata'].get('deletionTimestamp'))
            if current['metadata']['uid'] == previous_uid:
                raise RuntimeError('Deployment did not replace the pod')
            checks = '''import sqlite3,urllib.request,urllib.error
for path in ('/health/live','/health/ready'):
 with urllib.request.urlopen('http://127.0.0.1:8000'+path,timeout=3) as response: assert response.status==200
try:
 urllib.request.urlopen('http://127.0.0.1:8000/v1/reference/alerts',timeout=3)
 raise AssertionError('Anonymous access accepted')
except urllib.error.HTTPError as error: assert error.code==401
with sqlite3.connect('file:/data/assessments.db?mode=ro',uri=True) as db:
 assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 assert db.execute('SELECT COUNT(*) FROM api_assessments').fetchone()[0]==1
print('DEPLOYMENT_READY_AND_RECEIPT_RESTORED')
'''
            output = call('-n', namespace, 'exec', current['metadata']['name'], '--', 'python', '-c', checks)
            if 'DEPLOYMENT_READY_AND_RECEIPT_RESTORED' not in output:
                raise RuntimeError('Deployment verification incomplete')
            previous_uid = current['metadata']['uid']
            if iteration == 0:
                call('-n', namespace, 'delete', 'pod', current['metadata']['name'], '--wait=true', '--timeout=40s')
        result['default_deployment_recovered'] = True
        apply(pod('service-client'))
        call('-n', namespace, 'wait', '--for=condition=Ready', 'pod/service-client', '--timeout=45s')
        service = json.loads(call('-n', namespace, 'get', 'service', 'pulse-api', '-o', 'json'))
        service_checks = '''import json,socket,sys,urllib.request,urllib.error
name='pulse-api.'+sys.argv[1]+'.svc.cluster.local'
address=sys.argv[2]
assert socket.gethostbyname(name)==address
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
for host in (name,address):
 for path in ('/health/live','/health/ready'):
  with opener.open('http://'+host+path,timeout=5) as response: assert response.status==200
 try:
  opener.open('http://'+host+'/v1/reference/alerts',timeout=5)
  raise AssertionError('Anonymous Service request accepted')
 except urllib.error.HTTPError as error: assert error.code==401
print('SERVICE_DNS_ROUTING_PASS')
'''
        output = call('-n', namespace, 'exec', 'service-client', '--', 'python', '-c',
            service_checks, namespace, service['spec']['clusterIP'])
        if 'SERVICE_DNS_ROUTING_PASS' not in output:
            raise RuntimeError('Service routing verification incomplete')
        result['service_dns_and_routing_verified'] = True
        if os.environ.get('PULSE_VERIFY_NETWORK_POLICY') == '1':
            target = pod('egress-target')
            target['spec']['securityContext']['sysctls'] = [{'name': 'net.ipv4.ip_unprivileged_port_start', 'value': '0'}]
            target['spec']['containers'][0]['command'] = ['python', '-c',
                'import http.server,threading; a=http.server.ThreadingHTTPServer(("0.0.0.0",443),http.server.SimpleHTTPRequestHandler); threading.Thread(target=a.serve_forever,daemon=True).start(); http.server.ThreadingHTTPServer(("0.0.0.0",8080),http.server.SimpleHTTPRequestHandler).serve_forever()']
            target['spec']['containers'][0]['readinessProbe'] = {'httpGet': {'path': '/', 'port': 8080}, 'periodSeconds': 1}
            apply(target)
            call('-n', namespace, 'wait', '--for=condition=Ready', 'pod/egress-target', '--timeout=45s')
            target_ip = json.loads(call('-n', namespace, 'get', 'pod', 'egress-target', '-o', 'json'))['status']['podIP']
            reachable = 'import sys,urllib.request; opener=urllib.request.build_opener(urllib.request.ProxyHandler({})); responses=[opener.open("http://"+sys.argv[1]+":"+str(port)+"/",timeout=3) for port in (8080,443)]; assert all(r.status==200 for r in responses)'
            call('-n', namespace, 'exec', current['metadata']['name'], '--', 'python', '-c', reachable, target_ip)
            policy = next(d for d in documents if d['kind'] == 'NetworkPolicy')
            policy['metadata']['namespace'] = namespace
            apply(policy)
            isolation_probe = '''import json,socket,sys,time,urllib.request
time.sleep(5)
results=[]
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
for attempt in range(3):
 try:
  with opener.open('http://'+sys.argv[1]+'/health/ready',timeout=2) as response:
   results.append({'http_status':response.status,'blocked':False})
 except Exception as error:
  results.append({'error_type':type(error).__name__,'blocked':True})
 time.sleep(2)
print(json.dumps(results))
'''
            attempts = json.loads(call('-n', namespace, 'exec', 'service-client', '--', 'python', '-c',
                isolation_probe, service['spec']['clusterIP']))
            # Confirm the target remained healthy; connectivity failure alone is not enforcement proof.
            call('-n', namespace, 'exec', current['metadata']['name'], '--', 'python', '-c', checks)
            outbound_probe = '''import json,socket,sys,urllib.request
assert socket.gethostbyname(sys.argv[2])==sys.argv[3]
results=[]
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
for port in (8080,443):
 for attempt in range(3):
  try:
   with opener.open('http://'+sys.argv[1]+':'+str(port)+'/',timeout=2) as response:
    results.append({'port':port,'blocked':False,'http_status':response.status})
  except urllib.error.URLError as error:
   results.append({'port':port,'blocked':True,'error_type':type(error.reason).__name__})
print(json.dumps(results))
'''
            outbound = json.loads(call('-n', namespace, 'exec', current['metadata']['name'], '--',
                'python', '-c', outbound_probe, target_ip,
                f'pulse-api.{namespace}.svc.cluster.local', service['spec']['clusterIP']))
            call('-n', namespace, 'exec', 'service-client', '--', 'python', '-c', reachable, target_ip)
            result['network_policy'] = {'attempts': attempts,
                'ingress_denied': all(item['blocked'] for item in attempts),
                'baseline_service_reachable': True, 'target_healthy_after_policy': True,
                'egress_attempts': outbound, 'private_egress_denied': all(item['blocked'] for item in outbound),
                'dns_resolution_after_policy': True, 'egress_target_reachable_before_and_after': True,
                'target_pod_ip': target_ip,
                'scope': 'Local Service ingress, private pod-IP TCP 8080 and 443 egress and DNS; plaintext test traffic, public HTTPS and other paths untested'}
            result['application_recovery_result'] = result['result']
            result['result'] = 'PASS' if result['network_policy']['ingress_denied'] and result['network_policy']['private_egress_denied'] else 'FAIL'
            if os.environ.get('PULSE_VERIFY_PUBLIC_HTTPS') == '1':
                public_probe = '''import ipaddress,json,socket,ssl,urllib.request
host='docs.python.org'
addresses=sorted({item[4][0] for item in socket.getaddrinfo(host,443,type=socket.SOCK_STREAM)})
assert addresses and all(ipaddress.ip_address(address).is_global for address in addresses)
context=ssl.create_default_context()
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs): return None
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPSHandler(context=context),NoRedirect())
with opener.open('https://docs.python.org/3/',timeout=10) as response:
 assert response.status==200
 size=len(response.read(1024))
 assert size>0
print(json.dumps({'url':'https://docs.python.org/3/','status':200,'bytes_sampled':size,'resolved_addresses':addresses,'certificate_verification':True,'proxy_disabled':True,'redirects_disabled':True}))
'''
                result['network_policy']['public_https'] = json.loads(call('-n', namespace, 'exec',
                    current['metadata']['name'], '--', 'python', '-c', public_probe))
                result['network_policy']['scope'] = 'Local Service ingress, private pod-IP TCP 8080/443 egress, DNS and one certificate-verified public HTTPS endpoint; other paths untested'
    finally:
        call('delete', 'namespace', namespace, '--ignore-not-found=true', '--wait=true', '--timeout=45s')
    result.update(namespace_removed=True, pod_replaced=True, storage_class='standard')
    if os.environ.get('PULSE_NETWORK_POLICY_EVIDENCE'):
        Path(os.environ['PULSE_NETWORK_POLICY_EVIDENCE']).write_text(json.dumps(result, indent=2)+'\n')
    return result
