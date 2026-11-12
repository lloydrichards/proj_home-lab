#!/usr/bin/bash
set -euo pipefail
[[ $EUID == 0 ]] || { echo 'Run this installer with sudo.' >&2; exit 1; }
[[ $# == 0 || ( $# == 1 && $1 == --refresh-services ) ]] || exit 1
source_dir=$(cd -- "$(dirname -- "$0")" && pwd)
repo_dir=$(cd -- "$source_dir/../../.." && pwd)
bootstrap="$repo_dir/local/backup-bootstrap"
[[ $(hostname) == home-lab ]] || { echo 'This installer is for home-lab only.' >&2; exit 1; }
# Validate migration input before replacing collector code or changing services.
remote_ip=$(python3 - "${BACKUP_EXPORTER_IP:-}" <<'PYTHON'
import ipaddress
from pathlib import Path
import sys
value = sys.argv[1]
if not value:
    path = Path('/home/lab-backup/credentials/remote-ip')
    if not path.is_file():
        raise SystemExit('Set BACKUP_EXPORTER_IP before installing or refreshing the collector.')
    value = path.read_text().strip()
try:
    print(ipaddress.IPv4Address(value))
except ipaddress.AddressValueError:
    raise SystemExit('The exporter address must be a valid IPv4 address.')
PYTHON
)
command -v restic >/dev/null || pacman -S --needed --noconfirm restic
id lab-backup >/dev/null 2>&1 || useradd --system --user-group --create-home --home-dir /home/lab-backup --shell /usr/bin/nologin lab-backup
install -d -m 700 -o lab-backup -g lab-backup /home/lab-backup /home/lab-backup/credentials /home/lab-backup/staging /home/lab-backup/repository
# Install the validated private input before the collector that requires it.
remote_ip_temp=$(mktemp /home/lab-backup/credentials/remote-ip.XXXXXX)
printf '%s\n' "$remote_ip" > "$remote_ip_temp"
chown lab-backup:lab-backup "$remote_ip_temp"
chmod 600 "$remote_ip_temp"
mv -f -- "$remote_ip_temp" /home/lab-backup/credentials/remote-ip
install -m 755 -o root -g root "$source_dir/collect.py" /usr/local/sbin/lab-backup-collect
for file in id_ed25519 id_ed25519.pub known_hosts; do
  if [[ ! -e /home/lab-backup/credentials/$file ]]; then
    install -m 600 -o lab-backup -g lab-backup "$bootstrap/$file" "/home/lab-backup/credentials/$file"
  fi
done
if [[ ! -s /home/lab-backup/credentials/restic-password ]]; then
  umask 077
  openssl rand -base64 48 > /home/lab-backup/credentials/restic-password
  chown lab-backup:lab-backup /home/lab-backup/credentials/restic-password
fi
cat > /etc/systemd/system/lab-backup-collect.service <<'EOF'
[Unit]
Description=Collect and restore-check remote-lab backups
Wants=network-online.target
After=network-online.target tailscaled.service
OnFailure=lab-backup-alert.service

[Service]
Type=oneshot
User=lab-backup
Group=lab-backup
Environment=TZ=Europe/Zurich
ExecStart=/usr/local/sbin/lab-backup-collect
TimeoutStartSec=2h
UMask=0077
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/home/lab-backup
RestrictSUIDSGID=yes
EOF
cat > /etc/systemd/system/lab-backup-collect.timer <<'EOF'
[Unit]
Description=Nightly remote-lab backup
[Timer]
OnCalendar=*-*-* 02:00:00 Europe/Zurich
Persistent=true
Unit=lab-backup-collect.service
[Install]
WantedBy=timers.target
EOF
cat > /etc/systemd/system/lab-backup-health.service <<'EOF'
[Unit]
Description=Check remote-lab backup freshness and storage
OnFailure=lab-backup-alert.service
[Service]
Type=oneshot
User=lab-backup
ExecStart=/usr/local/sbin/lab-backup-collect health
UMask=0077
NoNewPrivileges=yes
EOF
cat > /etc/systemd/system/lab-backup-health.timer <<'EOF'
[Unit]
Description=Hourly remote-lab backup freshness check
[Timer]
OnCalendar=hourly
Persistent=true
[Install]
WantedBy=timers.target
EOF
cat > /etc/systemd/system/lab-backup-alert.service <<'EOF'
[Unit]
Description=Local alert for remote-lab backup failure
[Service]
Type=oneshot
ExecStart=/usr/bin/logger -p user.err Remote-lab backup needs attention; inspect lab-backup-collect.service and lab-backup-health.service
ExecStart=/usr/bin/wall -- "Remote-lab backup needs attention. Check systemctl --failed and journalctl -u lab-backup-collect.service -u lab-backup-health.service"
EOF
systemctl daemon-reload
systemd-analyze verify /etc/systemd/system/lab-backup-{collect,health}.{service,timer} /etc/systemd/system/lab-backup-alert.service
if [[ ${1:-} == --refresh-services ]]; then
  echo 'Service definitions refreshed; schedules preserved, no backup or outage triggered.'
  exit 0
fi
# Keep timers disabled until the manual transfer and restore tests pass.
echo 'Installed. Starting one manual backup with repository restore and SQLite checks.'
systemctl start lab-backup-collect.service
systemctl enable --now lab-backup-collect.timer lab-backup-health.timer
systemctl start lab-backup-health.service
install -d -m 755 /var/lib/lab-backup-status
date -Is > /var/lib/lab-backup-status/installed
echo 'Backup and restore checks passed. Nightly and hourly timers enabled.'
echo 'Save /home/lab-backup/credentials/restic-password in your password manager using a trusted local terminal.'
