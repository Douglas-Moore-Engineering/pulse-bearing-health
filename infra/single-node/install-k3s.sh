#!/usr/bin/env bash
set -euo pipefail
version='v1.37.1+k3s1'
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
cd "$work"
curl --fail --location --retry 3 --output k3s "https://github.com/k3s-io/k3s/releases/download/${version}/k3s"
curl --fail --location --retry 3 --output sha256sum-amd64.txt "https://github.com/k3s-io/k3s/releases/download/${version}/sha256sum-amd64.txt"
sha256sum --check --ignore-missing sha256sum-amd64.txt
install -m 0755 k3s /usr/local/bin/k3s
modprobe overlay
modprobe br_netfilter
cat > /etc/sysctl.d/90-pulse-kubernetes.conf <<'EOF'
net.ipv4.ip_forward = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sysctl --system >/dev/null
cat > /etc/systemd/system/k3s.service <<'EOF'
[Unit]
Description=Pulse single-node K3s
After=network-online.target
Wants=network-online.target
[Service]
Type=notify
ExecStart=/usr/local/bin/k3s server --disable=traefik --disable=servicelb --secrets-encryption --write-kubeconfig-mode=600
KillMode=process
Delegate=yes
LimitNOFILE=1048576
LimitNPROC=infinity
TasksMax=infinity
Restart=always
RestartSec=5
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now k3s
for attempt in $(seq 1 90); do
  if /usr/local/bin/k3s kubectl get nodes >/dev/null 2>&1; then
    /usr/local/bin/k3s kubectl wait --for=condition=Ready node --all --timeout=180s
    exit 0
  fi
  sleep 2
done
echo 'K3s API did not become available' >&2
exit 1
