#!/usr/bin/bash
set -euo pipefail
[[ $EUID == 0 && $(hostname -s) == home-lab && $# == 0 ]] || exit 1
source_dir=$(cd -- "$(dirname -- "$0")" && pwd)
for tool in restic btrfs python3 findmnt; do command -v "$tool" >/dev/null; done
test -s /home/lab-backup/credentials/r2.json
test -s /home/lab-backup/credentials/restic-password
install -d -m 700 -o root -g root /var/lib/lab-agent-backup
install -m 755 -o root -g root "$source_dir/agents.py" /usr/local/sbin/lab-agent-backup
cat > /etc/systemd/system/lab-agent-backup.service <<'EOF'
[Unit]
Description=Back up home-lab agent sessions and restore-check local and R2 copies
Wants=network-online.target
After=network-online.target
OnFailure=lab-agent-backup-alert.service
[Service]
Type=oneshot
ExecStart=/usr/local/sbin/lab-agent-backup
TimeoutStartSec=4h
UMask=0077
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/var/lib/lab-agent-backup
RestrictSUIDSGID=yes
EOF
cat > /etc/systemd/system/lab-agent-backup.timer <<'EOF'
[Unit]
Description=Nightly home-lab agent session backup
[Timer]
OnCalendar=*-*-* 04:00:00 Europe/Zurich
Persistent=true
[Install]
WantedBy=timers.target
EOF
cat > /etc/systemd/system/lab-agent-backup-health.service <<'EOF'
[Unit]
Description=Check home-lab agent backup freshness
OnFailure=lab-agent-backup-alert.service
[Service]
Type=oneshot
ExecStart=/usr/local/sbin/lab-agent-backup health
UMask=0077
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=read-only
EOF
cat > /etc/systemd/system/lab-agent-backup-health.timer <<'EOF'
[Unit]
Description=Hourly home-lab agent backup freshness check
[Timer]
OnCalendar=hourly
[Install]
WantedBy=timers.target
EOF
cat > /etc/systemd/system/lab-agent-backup-alert.service <<'EOF'
[Unit]
Description=Local alert for home-lab agent backup failure
[Service]
Type=oneshot
ExecStart=/usr/bin/logger -p user.err Home-lab agent backup needs attention; inspect lab-agent-backup.service and lab-agent-backup-health.service
ExecStart=/usr/bin/wall -- "Home-lab agent backup needs attention. Inspect lab-agent-backup.service and lab-agent-backup-health.service."
EOF
systemctl daemon-reload
systemd-analyze verify /etc/systemd/system/lab-agent-backup{,-health}.{service,timer} /etc/systemd/system/lab-agent-backup-alert.service
systemctl start lab-agent-backup.service
systemctl start lab-agent-backup-health.service
systemctl enable --now lab-agent-backup.timer lab-agent-backup-health.timer
echo 'Agent-state local backup, R2 copy and restore checks passed. Nightly 04:00 Zurich schedule enabled.'
