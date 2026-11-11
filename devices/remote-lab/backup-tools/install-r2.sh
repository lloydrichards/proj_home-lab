#!/usr/bin/bash
set -euo pipefail
[[ $EUID == 0 && $(hostname -s) == home-lab && $# == 0 ]] || exit 1
source_dir=$(cd -- "$(dirname -- "$0")" && pwd)
test -s /home/lab-backup/credentials/r2.json
test -s /home/lab-backup/credentials/restic-password
systemctl cat lab-backup-collect.service >/dev/null
install -m 755 -o root -g root "$source_dir/r2.py" /usr/local/sbin/lab-backup-r2
cat > /etc/systemd/system/lab-backup-r2.service <<'EOF'
[Unit]
Description=Copy local remote-lab snapshots to Cloudflare R2
Wants=network-online.target
After=network-online.target
OnFailure=lab-backup-alert.service
[Service]
Type=oneshot
User=lab-backup
Group=lab-backup
ExecStart=/usr/local/sbin/lab-backup-r2
TimeoutStartSec=4h
UMask=0077
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/home/lab-backup
RestrictSUIDSGID=yes
EOF
cat > /etc/systemd/system/lab-backup-r2.timer <<'EOF'
[Unit]
Description=Retry R2 snapshot copy daily
[Timer]
OnCalendar=*-*-* 03:00:00 Europe/Zurich
Persistent=true
[Install]
WantedBy=timers.target
EOF
cat > /etc/systemd/system/lab-backup-r2-health.service <<'EOF'
[Unit]
Description=Check R2 backup freshness
OnFailure=lab-backup-alert.service
[Service]
Type=oneshot
User=lab-backup
ExecStart=/usr/local/sbin/lab-backup-r2 health
UMask=0077
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=read-only
EOF
cat > /etc/systemd/system/lab-backup-r2-health.timer <<'EOF'
[Unit]
Description=Hourly R2 backup freshness check
[Timer]
OnCalendar=hourly
[Install]
WantedBy=timers.target
EOF
install -d -m 755 /etc/systemd/system/lab-backup-collect.service.d
cat > /etc/systemd/system/lab-backup-collect.service.d/r2.conf <<'EOF'
[Unit]
OnSuccess=lab-backup-r2.service
EOF
systemctl daemon-reload
systemd-analyze verify /etc/systemd/system/lab-backup-r2{,-health}.{service,timer}
systemctl start lab-backup-r2.service
systemctl start lab-backup-r2-health.service
systemctl enable --now lab-backup-r2.timer lab-backup-r2-health.timer
echo 'R2 copy and health checks passed; automatic copying enabled. No Pi backup was triggered.'
