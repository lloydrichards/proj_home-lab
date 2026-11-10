#!/usr/bin/env bash
set -euo pipefail
umask 077
[[ $(hostname -s) == home-lab && $(id -un) == coder ]] || { echo 'Run on home-lab as coder.' >&2; exit 1; }
source_dir=$(cd -- "$(dirname -- "$0")" && pwd)
lib=$HOME/.local/lib/lab-publish
root=$HOME/.local/share/lab-publish
mkdir -p "$lib" "$root"/{state/previews,staging,public,launches} "$HOME/.config/systemd/user"
for name in common.sh publish-report.sh delete-report.sh start-preview.sh stop-preview.sh preview-status.sh report-files.py report-server.py service-files.py preview-runner.py preview-check.py; do
  install -m 700 "$source_dir/$name" "$lib/$name.new"
  mv "$lib/$name.new" "$lib/$name"
done
if ss -H -lnt 'sport = :8379' | grep -q .; then
  check=$(mktemp "$root/staging/install-check.XXXXXX")
  printf '%s' '{"status":"allocated","unit":"lab-reports.service","internal_port":8379,"host":"localhost"}' >"$check"
  if ! python3 "$lib/preview-check.py" "$check"; then
    rm -f "$check"
    echo 'Port 8379 belongs to another service; refusing to replace it.' >&2
    exit 1
  fi
  rm -f "$check"
fi
python3 - "$lib" "$root" <<'PY'
from pathlib import Path
import sys
# The quote function is deliberately repeated here to avoid executing the service writer.
def q(s):
    if any(c in s for c in '\n\r\0'): raise ValueError('Invalid path')
    return '"'+s.replace('\\','\\\\').replace('"','\\"').replace('%','%%').replace('$','$$')+'"'
p=Path.home()/'.config/systemd/user/lab-reports.service'
p.write_text('[Unit]\nDescription=Private development report server\n[Service]\nExecStart=/usr/bin/python3 '+q(sys.argv[1]+'/report-server.py')+' '+q(sys.argv[2])+'\nRestart=on-failure\nRestartSec=5\n[Install]\nWantedBy=default.target\n')
PY
systemctl --user daemon-reload
systemctl --user enable lab-reports.service
systemctl --user restart lab-reports.service
curl --fail --silent --show-error --retry 5 --retry-connrefused --retry-delay 1 http://127.0.0.1:8379/ >/dev/null
if [[ -x /usr/local/sbin/lab-publish-route ]]; then
  sudo -n /usr/local/sbin/lab-publish-route reports
else
  echo 'Report server is ready locally. An administrator must install lab-publish-route and its narrow sudoers rule.' >&2
fi
