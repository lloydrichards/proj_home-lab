#!/usr/bin/python3
"""Root-only cold backup producer. Never accepts client-selected paths or commands."""
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess as sp
import sys
import time

BASE = Path('/var/lib/lab-backup-export')
STATE = BASE / 'stopped.json'


def run(args, **kw):
    return sp.run(args, check=True, **kw)


def docker_json(*args):
    return json.loads(sp.check_output(['docker', *args]))


def recover():
    if not STATE.exists():
        return
    containers = json.loads(STATE.read_text())
    databases = [c for c in containers if c['postgres']]
    others = [c for c in containers if not c['postgres']]
    for group in (databases, others):
        if group:
            run(['docker', 'start', *[c['id'] for c in group]], stdout=sp.DEVNULL)
        if group == databases:
            for c in group:
                for _ in range(60):
                    result = sp.run(['docker', 'exec', c['id'], 'sh', '-c',
                                     'pg_isready -U "${POSTGRES_USER:-postgres}"'],
                                    stdout=sp.DEVNULL, stderr=sp.DEVNULL)
                    if result.returncode == 0:
                        break
                    time.sleep(1)
                else:
                    raise RuntimeError('Database did not restart: ' + c['name'])
    current = docker_json('inspect', *[c['id'] for c in containers])
    if not all(c['State']['Running'] for c in current):
        raise RuntimeError('Some original containers are still stopped')
    STATE.unlink()


def produce():
    BASE.mkdir(mode=0o700, parents=True, exist_ok=True)
    with (BASE / 'producer.lock').open('w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        recover()
        if shutil.disk_usage(BASE).free < 5 * 1024**3:
            raise RuntimeError('Less than 5 GiB free on remote-lab')
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        work = BASE / (stamp + '.partial')
        work.mkdir(mode=0o700)
        (work / 'postgres').mkdir()
        ids = sp.check_output(['docker', 'ps', '-aq'], text=True).split()
        inventory = docker_json('inspect', *ids)
        # Contains environment values and recovery secrets: root-only, never log it.
        (work / 'containers.json').write_text(json.dumps(inventory, indent=2))
        running = []
        for c in inventory:
            if not c['State']['Running']:
                continue
            env = dict(v.split('=', 1) for v in c['Config'].get('Env', []) if '=' in v)
            pg = any(m['Destination'] == '/var/lib/postgresql/data' for m in c['Mounts'])
            running.append({'id': c['Id'], 'name': c['Name'].lstrip('/'),
                            'postgres': pg, 'user': env.get('POSTGRES_USER', 'postgres')})
        STATE.write_text(json.dumps(running))
        started = time.time()
        try:
            others = [c['id'] for c in running if not c['postgres']]
            if others:
                run(['docker', 'stop', '--timeout', '60', *others], stdout=sp.DEVNULL)
            for c in running:
                if not c['postgres']:
                    continue
                with (work / 'postgres' / (c['name'] + '.sql')).open('wb') as out:
                    run(['docker', 'exec', c['id'], 'pg_dumpall', '-U', c['user']], stdout=out)
                if c['name'] == 'coolify-db':
                    with (work / 'postgres' / 'coolify.dmp').open('wb') as out:
                        run(['docker', 'exec', c['id'], 'pg_dump', '-U', c['user'],
                             '-Fc', 'coolify'], stdout=out)
            pgids = [c['id'] for c in running if c['postgres']]
            if pgids:
                run(['docker', 'stop', '--timeout', '60', *pgids], stdout=sp.DEVNULL)
            # Include inactive volumes too; no volume is deleted by this job.
            sources = {'data/coolify', 'etc/ssh', 'etc/hostname', 'etc/hosts'}
            for p in Path('/var/lib/docker/volumes').glob('*/_data'):
                sources.add(str(p).lstrip('/'))
            for c in inventory:
                for m in c['Mounts']:
                    p = Path(m['Source'])
                    if m['Type'] == 'bind' and p.exists() and not p.is_socket():
                        sources.add(str(p).lstrip('/'))
            with (work / 'data.tar').open('wb') as out:
                run(['tar', '--acls', '--xattrs', '--numeric-owner',
                     '--exclude=data/coolify/backups', '-C', '/', '-cf', '-',
                     *sorted(sources)], stdout=out)
        finally:
            recover()
        (work / 'manifest.json').write_text(json.dumps({
            'host': 'remote-lab', 'created_utc': stamp,
            'maintenance_seconds': round(time.time() - started, 1),
            'original_running_containers': [c['name'] for c in running],
            'scope': 'All Docker volume data, regular bind mounts, Coolify configuration and PostgreSQL dumps',
        }, indent=2))
        checks = []
        for path in sorted(work.rglob('*')):
            if path.is_file():
                with path.open('rb') as src:
                    digest = hashlib.file_digest(src, 'sha256').hexdigest()
                checks.append(digest + '  ' + str(path.relative_to(work)))
        (work / 'SHA256SUMS').write_text('\n'.join(checks) + '\n')
        final = BASE / stamp
        work.rename(final)
        latest = BASE / 'latest.new'
        latest.unlink(missing_ok=True)
        latest.symlink_to(stamp)
        latest.replace(BASE / 'latest')
        # Retain at least the last three successful generations, even after downtime.
        generations = sorted(p for p in BASE.iterdir() if p.is_dir() and p.name.endswith('Z'))
        for old in generations[:-3]:
            shutil.rmtree(old)
        print(json.dumps({'generation': stamp, 'maintenance_seconds': round(time.time()-started, 1)}))


if __name__ == '__main__':
    os.umask(0o077)
    if os.geteuid() != 0:
        raise SystemExit('Must run as root')
    if sys.argv[1:] == ['produce']:
        produce()
    elif sys.argv[1:] == ['recover']:
        recover()
    elif not sys.argv[1:]:
        # Fixed SSH entry point. A lock prevents another export changing latest.
        BASE.mkdir(mode=0o700, parents=True, exist_ok=True)
        with (BASE / 'export.lock').open('w') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            run(['systemctl', 'start', 'lab-backup-produce.service'], stdout=sys.stderr)
            run(['tar', '-C', str(BASE / 'latest'), '-cf', '-', '.'])
    else:
        raise SystemExit('Unsupported operation')
