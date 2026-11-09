#!/usr/bin/python3
"""Run as the home-lab lab-backup account; never as coder."""
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess as sp
import sys
import tarfile
import tempfile
import time

BASE = Path('/home/lab-backup')
STAGING = BASE / 'staging'
REPO = BASE / 'repository'
ENV = dict(os.environ, RESTIC_REPOSITORY=str(REPO),
           RESTIC_PASSWORD_FILE=str(BASE / 'credentials/restic-password'))


def run(args, **kw):
    return sp.run(args, check=True, env=ENV, **kw)


def verify(path):
    for line in (path / 'SHA256SUMS').read_text().splitlines():
        expected, name = line.split('  ', 1)
        candidate = (path / name).resolve()
        if not candidate.is_relative_to(path.resolve()):
            raise RuntimeError('Unsafe checksum path')
        with candidate.open('rb') as src:
            if hashlib.file_digest(src, 'sha256').hexdigest() != expected:
                raise RuntimeError('Backup checksum mismatch')
    manifest = json.loads((path / 'manifest.json').read_text())
    created = datetime.datetime.strptime(manifest['created_utc'], '%Y%m%dT%H%M%SZ').replace(
        tzinfo=datetime.timezone.utc).timestamp()
    if manifest['host'] != 'remote-lab' or not -300 < time.time() - created < 3600:
        raise RuntimeError('Backup source or freshness check failed')
    return manifest


def sqlite_checks(data_tar):
    checked = 0
    with tempfile.TemporaryDirectory(dir=STAGING) as temp, tarfile.open(data_tar) as archive:
        for member in archive:
            if not member.isfile():
                continue
            with archive.extractfile(member) as src:
                header = src.read(16)
                if header != b'SQLite format 3\x00':
                    continue
                target = Path(temp) / str(checked)
                with target.open('wb') as dst:
                    dst.write(header)
                    shutil.copyfileobj(src, dst)
            with sqlite3.connect('file:' + str(target) + '?mode=ro', uri=True) as db:
                if db.execute('PRAGMA integrity_check').fetchall() != [('ok',)]:
                    raise RuntimeError('Restored SQLite integrity check failed')
                db.execute('SELECT count(*) FROM sqlite_master').fetchone()
            checked += 1
    if checked < 5:
        raise RuntimeError('Expected at least five application SQLite databases')
    return checked


def health():
    result = json.loads((BASE / 'last-success.json').read_text())
    if time.time() - result['completed_unix'] > 26 * 3600:
        raise RuntimeError('No successful backup within 26 hours')
    if shutil.disk_usage(BASE).free < 20 * 1024**3:
        raise RuntimeError('Less than 20 GiB free on home-lab')
    if int(sp.check_output(['du', '-sb', str(REPO)]).split()[0]) > 100 * 1024**3:
        raise RuntimeError('Backup repository exceeded the 100 GiB review threshold')
    print('Remote-lab backup freshness and capacity checks passed')


def collect():
    if shutil.disk_usage(BASE).free < 20 * 1024**3:
        raise RuntimeError('Less than 20 GiB free on home-lab')
    incoming = STAGING / 'incoming.tar.partial'
    new = STAGING / 'new'
    shutil.rmtree(new, ignore_errors=True)
    new.mkdir(mode=0o700)
    ssh = ['ssh', '-F', '/dev/null', '-p', '2222', '-o', 'BatchMode=yes',
           '-o', 'StrictHostKeyChecking=yes', '-o', 'IdentitiesOnly=yes',
           '-o', 'UserKnownHostsFile=' + str(BASE / 'credentials/known_hosts'),
           '-o', 'ConnectTimeout=20', '-o', 'ServerAliveInterval=30',
           '-o', 'ServerAliveCountMax=30', '-i', str(BASE / 'credentials/id_ed25519'),
           'lab-backup@100.107.227.75', 'export']
    with incoming.open('wb') as dst:
        run(ssh, stdout=dst, timeout=1800)
    with tarfile.open(incoming) as archive:
        for member in archive:
            target = (new / member.name).resolve()
            if not target.is_relative_to(new.resolve()) or not (member.isfile() or member.isdir()):
                raise RuntimeError('Unsafe transfer archive entry')
            archive.extract(member, new)
    manifest = verify(new)
    current = STAGING / 'current'
    shutil.rmtree(current, ignore_errors=True)
    new.rename(current)
    incoming.unlink()
    if not (REPO / 'config').exists():
        run(['restic', 'init'])
    run(['restic', 'backup', '--host', 'remote-lab', '--tag', 'cold-backup', str(current)])
    # Restore from the repository, not from staging, and verify every transferred byte.
    with tempfile.TemporaryDirectory(dir=STAGING) as restored:
        run(['restic', 'restore', 'latest', '--host', 'remote-lab', '--tag', 'cold-backup',
             '--target', restored])
        copy = Path(restored) / current.relative_to('/')
        verify(copy)
        sqlite_count = sqlite_checks(copy / 'data.tar')
    run(['restic', 'check'])
    # Full repository data read on the first successful run and each Sunday.
    if not (BASE / 'last-success.json').exists() or datetime.date.today().weekday() == 6:
        run(['restic', 'check', '--read-data'])
    run(['restic', 'forget', '--host', 'remote-lab', '--tag', 'cold-backup',
         '--keep-daily', '14', '--keep-weekly', '8', '--keep-monthly', '6', '--prune'])
    run(['restic', 'check'])
    result = {'completed_unix': time.time(), 'source': manifest,
              'restored_sqlite_databases_checked': sqlite_count}
    temp = BASE / 'last-success.json.new'
    temp.write_text(json.dumps(result, indent=2))
    temp.replace(BASE / 'last-success.json')
    (BASE / 'last-failure.txt').unlink(missing_ok=True)
    health()
    print(json.dumps({'backup': 'verified', 'sqlite_databases': sqlite_count,
                      'maintenance_seconds': manifest['maintenance_seconds']}))


if __name__ == '__main__':
    os.umask(0o077)
    try:
        if sys.argv[1:] == ['health']:
            health()
        elif not sys.argv[1:]:
            with (BASE / 'collector.lock').open('w') as lock:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                collect()
        else:
            raise RuntimeError('Unsupported operation')
    except Exception as exc:
        # No raw database output or credentials in status messages.
        message = f'{datetime.datetime.now(datetime.timezone.utc).isoformat()} {type(exc).__name__}: {exc}\n'
        (BASE / 'last-failure.txt').write_text(message)
        print(message, file=sys.stderr)
        raise SystemExit(1)
