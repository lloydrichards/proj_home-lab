"""Write one user unit. Arguments remain JSON data, never shell source."""
import json
from pathlib import Path
import sys


def quote(value):
    if '\n' in value or '\r' in value or '\x00' in value:
        raise ValueError('Newlines and NUL are not supported in service paths')
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"').replace('%', '%%').replace('$', '$$') + '"'


root, record, lib = map(Path, sys.argv[1:])
data = json.loads(record.read_text())
units = Path.home() / '.config/systemd/user'
units.mkdir(parents=True, exist_ok=True)
unit = f'''[Unit]
Description=Home-lab preview {data['id']}
[Service]
Type=simple
ExecStart=/usr/bin/python3 {quote(str(lib / 'preview-runner.py'))} {quote(str(record))}
KillMode=control-group
TimeoutStopSec=15
Restart=no
[Install]
WantedBy=default.target
'''
(units / data['unit']).write_text(unit)
