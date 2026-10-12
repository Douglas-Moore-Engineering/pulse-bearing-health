#!/usr/bin/env bash
set -euo pipefail
install -m 0750 /home/pulseadmin/pulse-release/check-runtime.py /usr/local/sbin/pulse-check-runtime.py
install -d -m 0700 /var/lib/pulse-ops
cat > /etc/systemd/system/pulse-health.service <<'EOF'
[Unit]
Description=Pulse reference health snapshot
After=k3s.service pulse-port-forward.service
[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /usr/local/sbin/pulse-check-runtime.py
TimeoutStartSec=40
StandardOutput=null
StandardError=journal
EOF
cat > /etc/systemd/system/pulse-health.timer <<'EOF'
[Unit]
Description=Check Pulse reference health every minute
[Timer]
OnBootSec=60
OnUnitActiveSec=60
AccuracySec=5
[Install]
WantedBy=timers.target
EOF
systemctl daemon-reload
systemctl enable --now pulse-health.timer
systemctl start pulse-health.service
cat /var/lib/pulse-ops/health.json
