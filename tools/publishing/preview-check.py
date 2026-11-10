"""Check HTTP readiness and listener membership in the expected systemd cgroup."""
import json
from pathlib import Path
import re
import subprocess
import sys
import urllib.request

record = json.loads(Path(sys.argv[1]).read_text())
try:
    if record['status'] == 'retired':
        raise ValueError('retired')
    group = subprocess.check_output(['systemctl', '--user', 'show', record['unit'], '-p', 'ControlGroup', '--value'], text=True).strip()
    if not group:
        raise ValueError('No process group')
    listeners = subprocess.check_output(['ss', '-H', '-lntp', f'sport = :{record["internal_port"]}'], text=True)
    if not listeners or any('127.0.0.1:' not in line for line in listeners.splitlines()):
        raise ValueError('Listener must bind IPv4 loopback only')
    pids = re.findall(r'pid=(\d+)', listeners)
    if not pids or not all(any(line.split(':', 2)[-1].strip() == group or line.split(':', 2)[-1].strip().startswith(group + '/') for line in Path(f'/proc/{pid}/cgroup').read_text().splitlines()) for pid in pids):
        raise ValueError('Listener belongs to another service')
    request = urllib.request.Request(f'http://127.0.0.1:{record["internal_port"]}{record.get("health_path", "/")}', headers={'Host': record['host']})
    with urllib.request.urlopen(request, timeout=2) as response:
        if response.status >= 400:
            raise ValueError('HTTP failure')
except Exception:
    sys.exit(1)
