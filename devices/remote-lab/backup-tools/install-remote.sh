#!/bin/bash
set -euo pipefail
[[ $EUID == 0 && $(hostname) == remote-lab ]] || exit 1
source_dir=$(cd -- "$(dirname -- "$0")" && pwd)
[[ -s "$source_dir/id_ed25519.pub" ]] || exit 1
id lab-backup >/dev/null 2>&1 || useradd --system --user-group --create-home --home-dir /var/lib/lab-backup --shell /bin/sh lab-backup
install -d -m 755 /etc/lab-backup
install -d -m 700 /var/lib/lab-backup-export
install -m 755 "$source_dir/export.py" /usr/local/sbin/lab-backup-export
{
  printf 'restrict,from="100.73.122.94" '
  cat "$source_dir/id_ed25519.pub"
} > /etc/lab-backup/authorized_keys
chmod 644 /etc/lab-backup/authorized_keys
cat > /usr/local/sbin/lab-backup-dispatch <<'EOF'
#!/bin/sh
[ "${SSH_ORIGINAL_COMMAND:-}" = export ] || { echo 'Only the backup export command is permitted.' >&2; exit 1; }
exec /usr/bin/sudo -n /usr/local/sbin/lab-backup-export
EOF
chmod 755 /usr/local/sbin/lab-backup-dispatch
cat > /usr/local/sbin/lab-backup-shell <<'EOF'
#!/bin/sh
# Tailscale SSH on port 22 must not become an alternate interactive entry point.
[ "$#" -eq 2 ] && [ "$1" = -c ] && [ "$2" = /usr/local/sbin/lab-backup-dispatch ] || exit 1
exec /usr/local/sbin/lab-backup-dispatch
EOF
chmod 755 /usr/local/sbin/lab-backup-shell
usermod --shell /usr/local/sbin/lab-backup-shell lab-backup
printf 'lab-backup ALL=(root) NOPASSWD: /usr/local/sbin/lab-backup-export ""\n' > /etc/sudoers.d/lab-backup
chmod 440 /etc/sudoers.d/lab-backup
visudo -cf /etc/sudoers.d/lab-backup
cat > /etc/lab-backup/sshd_config <<'EOF'
Port 2222
ListenAddress 100.107.227.75
HostKey /etc/ssh/ssh_host_ed25519_key
PidFile /run/lab-backup-sshd.pid
UsePAM yes
AllowUsers lab-backup
AuthorizedKeysFile /etc/lab-backup/authorized_keys
AuthenticationMethods publickey
PubkeyAuthentication yes
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitRootLogin no
PermitTTY no
DisableForwarding yes
PermitUserEnvironment no
ForceCommand /usr/local/sbin/lab-backup-dispatch
LogLevel VERBOSE
EOF
/usr/sbin/sshd -t -f /etc/lab-backup/sshd_config
cat > /etc/systemd/system/lab-backup-sshd.service <<'EOF'
[Unit]
Description=Restricted SSH backup export over Tailscale
After=network-online.target tailscaled.service
Wants=network-online.target tailscaled.service
[Service]
ExecStart=/usr/sbin/sshd -D -e -f /etc/lab-backup/sshd_config
Restart=on-failure
RestartSec=10
[Install]
WantedBy=multi-user.target
EOF
cat > /etc/systemd/system/lab-backup-produce.service <<'EOF'
[Unit]
Description=Consistent cold backup of remote-lab containers
After=docker.service
Requires=docker.service
OnFailure=lab-backup-alert.service
[Service]
Type=oneshot
ExecStart=/usr/local/sbin/lab-backup-export produce
ExecStopPost=/usr/local/sbin/lab-backup-export recover
TimeoutStartSec=15min
TimeoutStopSec=3min
UMask=0077
EOF
cat > /etc/systemd/system/lab-backup-recover.service <<'EOF'
[Unit]
Description=Recover containers interrupted during a backup by a host reboot
After=docker.service
Requires=docker.service
Before=lab-backup-sshd.service
[Service]
Type=oneshot
ExecStart=/usr/local/sbin/lab-backup-export recover
[Install]
WantedBy=multi-user.target
EOF
cat > /etc/systemd/system/lab-backup-alert.service <<'EOF'
[Unit]
Description=Local alert for backup or container recovery failure
[Service]
Type=oneshot
ExecStart=/usr/bin/logger -p user.err Remote-lab backup failed; inspect lab-backup-produce.service and container recovery state
ExecStart=/usr/bin/wall Remote-lab backup failed. Check lab-backup-produce.service and container state.
EOF
systemctl daemon-reload
systemd-analyze verify /etc/systemd/system/lab-backup-{sshd,produce,recover,alert}.service
systemctl enable --now lab-backup-recover.service lab-backup-sshd.service
echo 'Restricted backup exporter installed. This installer does not create a backup.'
