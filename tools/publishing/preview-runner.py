"""Run a stored argument vector with a bounded consecutive failure budget."""
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

record = Path(sys.argv[1])
data = json.loads(record.read_text())
child = None
stopping = False


def state(status, **extra):
    temporary = record.with_suffix('.runtime.tmp')
    temporary.write_text(json.dumps(dict(status=status, **extra)))
    os.replace(temporary, record.with_suffix('.runtime'))


def stop(signum, frame):
    global stopping
    stopping = True
    if child and child.poll() is None:
        child.terminate()


def change_route(operation):
    helper = Path('/usr/local/sbin/lab-publish-route')
    if not helper.exists() or not data.get("external_port"):
        return False
    try:
        result = subprocess.run(['sudo', '-n', str(helper), operation,
                                 str(data['external_port']), str(data['internal_port'])],
                                stdout=sys.stderr, stderr=sys.stderr, timeout=15)
        return result.returncode == 0
    except (OSError, subprocess.TimeoutExpired) as error:
        print(f'Route operation failed: {error}', flush=True)
        return False


signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGINT, stop)
change_route('stop')
if data['status'] == 'retired':
    state('retired')
    sys.exit('Preview is retired')
if not Path(data['worktree']).is_dir():
    state('failed', reason='worktree missing')
    sys.exit('Recorded worktree is missing; refusing to substitute another checkout')
env = dict(os.environ)
env["PATH"] = data.get("launch_path", env.get("PATH", "/usr/bin:/bin"))
env.update(LAB_PREVIEW_URL=data.get('url', ''), LAB_PREVIEW_HOST=data['host'], PORT=str(data['internal_port']), LAB_PREVIEW_PORT=str(data['internal_port']),
           __VITE_ADDITIONAL_SERVER_ALLOWED_HOSTS=data['host'])
if data.get('environment'):
    env.update(json.loads(Path(data['environment']).read_text()))
argv = [arg.replace('{port}', str(data['internal_port'])) for arg in data['argv']]
failures = 0
while not stopping:
    try:
        child = subprocess.Popen(argv, cwd=data['worktree'], env=env)
        state('running', pid=child.pid, attempt=failures+1)
        routed = False
        while child.poll() is None:
            try:
                code = child.wait(timeout=2)
            except subprocess.TimeoutExpired:
                if not routed and not stopping and Path('/usr/local/sbin/lab-publish-route').exists():
                    ready = subprocess.run([sys.executable, str(Path(__file__).with_name('preview-check.py')), str(record)], timeout=10)
                    if ready.returncode == 0:
                        routed = change_route('preview')
                continue
        code = child.returncode
    except OSError as error:
        print(f'Launch failed: {error}', flush=True)
        code = 1
    change_route('stop')
    if stopping:
        state('stopped')
        sys.exit(0)
    # Long-lived processes still consume the budget. Repair requires an explicit restart.
    failures += 1
    print(f'Preview exited with {code}; failure {failures}/4', flush=True)
    if failures >= 4:
        state('failed', reason='retry budget exhausted', exit_code=code)
        sys.exit(1)
    state('retrying', failures=failures)
    time.sleep(3)
