#!/usr/bin/env bash
set -euo pipefail
install -d -m 700 /var/lib/pulse-ops/reconciliation
cat > /etc/systemd/system/pulse-reconciliation.service <<'EOF'
[Unit]
Description=Pulse fictional fleet daily reconciliation
After=k3s.service
Requires=k3s.service
[Service]
Type=oneshot
UMask=0077
ExecStart=/usr/bin/python3 /home/pulseadmin/pulse-release/reconcile-runtime.py
TimeoutStartSec=90
EOF
cat > /etc/systemd/system/pulse-reconciliation.timer <<'EOF'
[Unit]
Description=Reconcile before the fictional 06:00 America/New_York deadline
[Timer]
OnCalendar=*-*-* 05:55:00 America/New_York
OnCalendar=*-*-* 06:00:00 America/New_York
Persistent=true
AccuracySec=1s
Unit=pulse-reconciliation.service
[Install]
WantedBy=timers.target
EOF
systemctl daemon-reload
systemctl enable --now pulse-reconciliation.timer
systemctl start pulse-reconciliation.service
systemctl list-timers pulse-reconciliation.timer --no-pager
