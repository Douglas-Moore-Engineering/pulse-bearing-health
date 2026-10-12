#!/usr/bin/env bash
set -euo pipefail
cd /home/pulseadmin/pulse-release
python3 - <<'PY'
import hashlib,json
from pathlib import Path
r=json.loads(Path('release.json').read_text())
for name,key in [('pulse-api.tar','archiveSha256'),('application.yaml','manifestsSha256')]:
    h=hashlib.sha256()
    with Path(name).open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''):h.update(chunk)
    if h.hexdigest()!=r[key]:raise SystemExit('Release checksum mismatch: '+name)
print('Release archive and manifests verified')
PY
k3s ctr images import --platform linux/amd64 pulse-api.tar
# Namespace must exist for namespaced server-side dry runs.
k3s kubectl create namespace pulse --dry-run=client -o yaml | k3s kubectl apply -f -
k3s kubectl apply --dry-run=server -f application.yaml
k3s kubectl apply -f application.yaml
k3s kubectl -n pulse rollout status deployment/pulse-api --timeout=240s
cat > /etc/systemd/system/pulse-port-forward.service <<'EOF'
[Unit]
Description=Pulse API loopback access
After=k3s.service
Requires=k3s.service
[Service]
ExecStart=/usr/local/bin/k3s kubectl -n pulse port-forward service/pulse-api 18080:80 --address=127.0.0.1
Restart=always
RestartSec=3
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now pulse-port-forward
systemctl restart pulse-port-forward
k3s kubectl -n pulse get pods,pvc
