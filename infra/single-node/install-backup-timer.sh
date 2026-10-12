#!/usr/bin/env bash
set -euo pipefail
install -m 0750 /home/pulseadmin/pulse-release/backup-runtime.py /usr/local/sbin/pulse-backup-runtime.py
install -d -m 0700 /var/lib/pulse-ops/backups
cat > /etc/systemd/system/pulse-backup.service <<'EOF'
[Unit]
Description=Pulse bounded on-host receipt snapshot
After=k3s.service
[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /usr/local/sbin/pulse-backup-runtime.py
TimeoutStartSec=150
StandardOutput=null
StandardError=journal
EOF
cat > /etc/systemd/system/pulse-backup.timer <<'EOF'
[Unit]
Description=Half-hourly Pulse reference snapshot
[Timer]
OnCalendar=*-*-* *:00,30:00 UTC
AccuracySec=1s
Persistent=true
[Install]
WantedBy=timers.target
EOF
systemctl daemon-reload
systemctl enable --now pulse-backup.timer
systemctl restart pulse-backup.timer
systemctl start pulse-backup.service
cat /var/lib/pulse-ops/backup-status.json
