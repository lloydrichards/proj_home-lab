#!/usr/bin/python3
"""Copy verified local snapshots to R2 as home-lab's lab-backup account."""
import datetime
import fcntl
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time

BASE = Path('/home/lab-backup')
STATUS = BASE / 'r2-last-success.json'
RETENTION = ['--host', 'remote-lab', '--tag', 'cold-backup',
             '--keep-daily', '14', '--keep-weekly', '8', '--keep-monthly', '6']


def environment():
    config = json.loads((BASE / 'credentials/r2.json').read_text())
    return dict(os.environ, HOME=str(BASE),
                AWS_ACCESS_KEY_ID=config['access_key_id'],
                AWS_SECRET_ACCESS_KEY=config['secret_access_key'],
                AWS_DEFAULT_REGION='auto',
                RESTIC_PASSWORD_FILE=str(BASE / 'credentials/restic-password'),
                RESTIC_REPOSITORY=f"s3:{config['endpoint']}/{config['bucket']}/remote-lab")


def health():
    status = json.loads(STATUS.read_text())
    for key in ('completed_unix', 'snapshot_unix'):
        age = time.time() - status[key]
        if not -300 <= age <= 26 * 3600:
            raise RuntimeError('R2 copy or source snapshot is stale')
    print('R2 copy and source snapshot are within 26 hours', flush=True)


def retention_preview():
    with (BASE / 'collector.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        print('R2 retention preview only; no snapshots will be deleted.', flush=True)
        subprocess.run([
            'restic', 'forget', '--dry-run', '--verbose',
            *RETENTION
        ], env=environment(), check=True)


def copy():
    env = environment()
    # The local collector also holds this lock through retention and pruning.
    with (BASE / 'collector.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        def run(*args, capture=False):
            return subprocess.run(['restic', *args], env=env, check=True,
                                  stdout=subprocess.PIPE if capture else None,
                                  text=True)
        run('copy', '--from-repo', str(BASE / 'repository'),
            '--from-password-file', str(BASE / 'credentials/restic-password'),
            '--host', 'remote-lab', '--tag', 'cold-backup')
        previous = json.loads(STATUS.read_text()) if STATUS.exists() else {}
        full = (not previous or
                time.time() - previous.get('full_check_unix', 0) >= 7 * 86400)
        run('check', *(['--read-data'] if full else []))
        snapshots = json.loads(run('snapshots', '--json', '--host', 'remote-lab',
                                   '--tag', 'cold-backup', capture=True).stdout)
        if not snapshots:
            raise RuntimeError('No R2 snapshots found')
        latest = max(snapshots, key=lambda snapshot: snapshot['time'])
        snapshot_time = datetime.datetime.fromisoformat(
            latest['time'].replace('Z', '+00:00')).timestamp()
        if not -300 <= time.time() - snapshot_time <= 26 * 3600:
            raise RuntimeError('Newest cloud snapshot is stale; retention skipped')
        run('forget', *RETENTION, '--prune')
        run('check')
        snapshots = json.loads(run('snapshots', '--json', '--host', 'remote-lab',
                                   '--tag', 'cold-backup', capture=True).stdout)
        if not snapshots:
            raise RuntimeError('No R2 snapshots remain after retention')
        result = dict(completed_unix=time.time(), snapshot_unix=snapshot_time,
                      snapshot_id=latest['id'], snapshot_count=len(snapshots),
                      full_check_unix=time.time() if full else previous['full_check_unix'])
        temporary = STATUS.with_suffix('.new')
        temporary.write_text(json.dumps(result, indent=2) + '\n')
        temporary.replace(STATUS)
        health()
        print('R2 snapshot copy and repository check passed', flush=True)


if __name__ == '__main__':
    os.umask(0o077)
    try:
        if socket.gethostname().split('.')[0] != 'home-lab':
            raise RuntimeError('Run only on home-lab')
        if sys.argv[1:] == ['health']:
            health()
        elif sys.argv[1:] == ['retention-preview']:
            retention_preview()
        elif not sys.argv[1:]:
            copy()
        else:
            raise RuntimeError('Unsupported operation')
    except Exception as exc:
        # Credentials stay out of status messages and the journal.
        print(f'R2 backup failed: {type(exc).__name__}; inspect service status.',
              file=sys.stderr)
        raise SystemExit(1)
