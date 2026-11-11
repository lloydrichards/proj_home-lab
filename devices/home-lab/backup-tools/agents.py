#!/usr/bin/python3
"""Back up coder's agent state from a frozen home view; exclude project trees."""
import datetime
import fcntl
import json
import os
from pathlib import Path
import shutil
import socket
import sqlite3
import stat
import subprocess as sp
import sys
import tempfile
import time

BASE = Path('/var/lib/lab-agent-backup')
VIEW = BASE / 'home'
CREDENTIALS = Path('/home/lab-backup/credentials')
HOME = Path('/home/coder')
ROOTS = ['.codex', '.agents', '.config/opencode', '.local/share/opencode',
         '.local/state/opencode', '.t3/userdata', '.t3/service.env',
         '.local/state/rex', '.local/state/lab-skills']
EXCLUDED = ['.codex/worktrees', '.codex/tmp', '.codex/.tmp', '.codex/cache',
            '.codex/app-server-control', '.codex/thread-writer-locks',
            '.codex/tui-thread-reference-capabilities',
            '.local/share/opencode/repos', '.local/share/opencode/snapshot',
            '.local/state/opencode/locks', '.local/state/rex/tsnet',
            '.local/state/rex/terminal/.locks', '.local/state/rex/uploads/.locks']
STATUS = BASE / 'last-success.json'
TAG = 'agent-state'


def envs():
    config = json.loads((CREDENTIALS / 'r2.json').read_text())
    common = dict(os.environ, HOME='/root', XDG_CACHE_HOME=str(BASE / 'cache'),
                  RESTIC_PASSWORD_FILE=str(CREDENTIALS / 'restic-password'),
                  TZ='Europe/Zurich')
    local = dict(common, RESTIC_REPOSITORY=str(BASE / 'repository'))
    cloud = dict(common, AWS_ACCESS_KEY_ID=config['access_key_id'],
                 AWS_SECRET_ACCESS_KEY=config['secret_access_key'],
                 AWS_DEFAULT_REGION='auto',
                 RESTIC_REPOSITORY=f"s3:{config['endpoint']}/{config['bucket']}/home-lab")
    return local, cloud


def restic(env, *args, capture=False):
    return sp.run(['restic', *args], env=env, check=True, text=True,
                  stdout=sp.PIPE if capture else None)


def excluded(relative):
    return any(relative == name or relative.startswith(name + '/') for name in EXCLUDED)


def walk_error(error):
    raise error


def mounted_paths(path):
    output = sp.check_output(['findmnt', '--json', '-o', 'TARGET', '--submounts',
                              '--target', str(path)], text=True)
    pending = json.loads(output)['filesystems']
    paths = set()
    while pending:
        mount = pending.pop()
        paths.add(Path(mount['target']))
        pending.extend(mount.get('children', []))
    return paths


def included_roots(home, names, mounts, *, require_all=False):
    included = []
    for name in names:
        source = home / name
        # Check every prefix before following it, including the coder home.
        for current in (home, *(home / Path(*Path(name).parts[:i])
                                for i in range(1, len(Path(name).parts) + 1))):
            try:
                info = current.lstat()
            except FileNotFoundError:
                if require_all:
                    raise RuntimeError(f'Frozen agent root missing: {name}')
                break
            if stat.S_ISLNK(info.st_mode):
                raise RuntimeError('Agent path has a symlink ancestor or root; review scope')
            if current in mounts or os.path.ismount(current) or info.st_ino == 256:
                raise RuntimeError('Included agent path has nested storage; review scope')
            if current != source and not stat.S_ISDIR(info.st_mode):
                raise RuntimeError('Agent path ancestor must be a directory')
        else:
            if not source.resolve().is_relative_to(home.resolve()):
                raise RuntimeError('Agent root escapes the selected home view')
            if not source.is_file() and not source.is_dir():
                raise RuntimeError('Agent root must be a regular file or directory')
            for mounted in mounts:
                if mounted.is_relative_to(source) and not excluded(mounted.relative_to(home).as_posix()):
                    raise RuntimeError('Included agent data has mounted storage; review scope')
            if source.is_file():
                included.append(name)
                continue
            for directory, dirs, files in os.walk(source, followlinks=False, onerror=walk_error):
                current = Path(directory)
                if excluded(current.relative_to(home).as_posix()):
                    dirs[:] = []
                    continue
                if current in mounts or current.stat().st_ino == 256 or os.path.ismount(current):
                    raise RuntimeError('Included agent data has nested storage; review scope')
                dirs[:] = [d for d in dirs if not excluded((current / d).relative_to(home).as_posix())]
            included.append(name)
    return included


def preflight():
    if sp.check_output(['findmnt', '-no', 'FSTYPE', '-T', '/home'], text=True).strip() != 'btrfs':
        raise RuntimeError('Expected Btrfs home filesystem')
    roots = included_roots(HOME, ROOTS, mounted_paths('/home'))
    for required in ('.codex/sessions', '.local/share/opencode'):
        if not (HOME / required).is_dir():
            raise RuntimeError('Expected agent data missing')
    if shutil.disk_usage(BASE).free < 20 * 1024**3:
        raise RuntimeError('Less than 20 GiB free')
    return roots


def frozen_roots(expected):
    if VIEW.is_symlink() or not VIEW.is_dir():
        raise RuntimeError('Invalid frozen home view')
    home = VIEW / HOME.name
    names = included_roots(home, expected, mounted_paths(VIEW), require_all=True)
    for required in ('.codex/sessions', '.local/share/opencode'):
        if not (home / required).is_dir():
            raise RuntimeError('Expected frozen agent data missing')
    return [str(home / name) for name in names]


def verify_restore(env, snapshot):
    with tempfile.TemporaryDirectory(prefix='restore-', dir=BASE) as target:
        restic(env, 'restore', snapshot, '--target', target, '--verify')
        restored = Path(target) / VIEW.relative_to('/') / 'coder'
        # SQLite opens writable disposable copies so WAL/rollback recovery can run.
        databases = 0
        for directory, dirs, files in os.walk(restored, followlinks=False, onerror=walk_error):
            dirs[:] = [d for d in dirs if not (Path(directory) / d).is_symlink()]
            for name in files:
                path = Path(directory) / name
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                with path.open('rb') as src:
                    if src.read(16) != b'SQLite format 3\x00':
                        continue
                with sqlite3.connect(str(path), timeout=30) as db:
                    if db.execute('PRAGMA integrity_check').fetchall() != [('ok',)]:
                        raise RuntimeError('Restored agent database failed integrity check')
                    db.execute('SELECT count(*) FROM sqlite_master').fetchone()
                databases += 1
        transcripts = list((restored / '.codex/sessions').rglob('*.jsonl'))
        valid_transcripts = 0
        for path in transcripts:
            if path.is_symlink():
                continue
            with path.open() as src:
                first = src.readline()
            if first.strip():
                json.loads(first)
                valid_transcripts += 1
        if databases < 2 or valid_transcripts < 1:
            raise RuntimeError('Expected restored databases or session transcripts missing')
        return dict(sqlite_databases=databases, session_transcripts=valid_transcripts)


def health():
    result = json.loads(STATUS.read_text())
    if not -300 <= time.time() - result['completed_unix'] <= 26 * 3600:
        raise RuntimeError('No verified agent backup within 26 hours')
    print('Agent-state local and cloud backup freshness passed', flush=True)


def backup():
    with (BASE / 'backup.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        expected = preflight()
        if VIEW.exists() or VIEW.is_symlink():
            raise RuntimeError('Previous home snapshot remains; inspect before removing')
        local, cloud = envs()
        if not (BASE / 'repository/config').exists():
            restic(local, 'init')
        check = sp.run(['restic', 'snapshots', '--json'], env=cloud,
                       stdout=sp.DEVNULL, stderr=sp.PIPE)
        if check.returncode == 10:
            restic(cloud, 'init', '--copy-chunker-params',
                   '--from-repo', local['RESTIC_REPOSITORY'],
                   '--from-password-file', local['RESTIC_PASSWORD_FILE'])
        elif check.returncode != 0:
            raise RuntimeError('Cannot open cloud agent repository')
        sp.run(['btrfs', 'subvolume', 'snapshot', '-r', '/home', str(VIEW)], check=True)
        try:
            roots = frozen_roots(expected)
            if not roots:
                raise RuntimeError('Frozen agent data missing')
            exclusions = [arg for name in EXCLUDED
                          for arg in ('--exclude', str(VIEW / 'coder' / name))]
            restic(local, 'backup', '--host', 'home-lab', '--tag', TAG,
                   *exclusions, *roots)
            snapshots = json.loads(restic(local, 'snapshots', '--json', '--host',
                                         'home-lab', '--tag', TAG, capture=True).stdout)
            latest = max(snapshots, key=lambda item: item['time'])
            local_checks = verify_restore(local, latest['id'])
            restic(local, 'check')
            restic(cloud, 'copy', '--from-repo', local['RESTIC_REPOSITORY'],
                   '--from-password-file', local['RESTIC_PASSWORD_FILE'], latest['id'])
            cloud_snapshots = json.loads(restic(cloud, 'snapshots', '--json', '--host',
                                               'home-lab', '--tag', TAG, capture=True).stdout)
            copied = [item for item in cloud_snapshots
                      if item.get('original') == latest['id'] or item['id'] == latest['id']]
            if not copied:
                raise RuntimeError('Copied cloud snapshot identity not found')
            cloud_checks = verify_restore(cloud, copied[0]['id'])
            restic(cloud, 'check', '--read-data')
            for env in (local, cloud):
                restic(env, 'forget', '--host', 'home-lab', '--tag', TAG,
                       '--group-by', 'host,tags', '--keep-daily', '14',
                       '--keep-weekly', '8', '--keep-monthly', '6', '--prune')
                restic(env, 'check')
            result = dict(completed_unix=time.time(), local_snapshot=latest['id'],
                          cloud_snapshot=copied[0]['id'], local_checks=local_checks,
                          cloud_checks=cloud_checks)
            temporary = STATUS.with_suffix('.new')
            temporary.write_text(json.dumps(result, indent=2) + '\n')
            temporary.replace(STATUS)
            print(json.dumps(result), flush=True)
        finally:
            sp.run(['btrfs', 'subvolume', 'delete', str(VIEW)], check=True)
        health()


if __name__ == '__main__':
    os.umask(0o077)
    try:
        if socket.gethostname().split('.')[0] != 'home-lab' or os.geteuid() != 0:
            raise RuntimeError('Run as root on home-lab')
        if sys.argv[1:] == ['health']:
            health()
        elif not sys.argv[1:]:
            backup()
        else:
            raise RuntimeError('Unsupported operation')
    except Exception as exc:
        print(f'Agent-state backup failed: {type(exc).__name__}: {exc}', file=sys.stderr)
        raise SystemExit(1)
