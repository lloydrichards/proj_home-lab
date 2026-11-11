#!/usr/bin/python3
"""Prepare a disposable Codex profile from the verified R2 agent backup."""
import json
import os
from pathlib import Path
import pwd
import runpy
import shlex
import shutil
import socket
import sqlite3
import stat
import tempfile
import uuid

TESTS = Path('/var/lib/lab-codex-resume-test')


def choose_session(profile):
    for path in sorted((profile / 'sessions').rglob('*.jsonl')):
        if path.is_symlink():
            continue
        session_id = None
        roles = set()
        with path.open() as source:
            for line in source:
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    break
                payload = record.get('payload', {})
                if record.get('type') == 'session_meta':
                    session_id = payload.get('id')
                if record.get('type') == 'response_item' and payload.get('type') == 'message':
                    roles.add(payload.get('role'))
                if record.get('type') == 'event_msg':
                    if payload.get('type') == 'user_message':
                        roles.add('user')
                    if payload.get('type') == 'agent_message':
                        roles.add('assistant')
                if session_id and {'user', 'assistant'} <= roles:
                    return str(uuid.UUID(session_id))
    raise RuntimeError('No restored conversation with user and assistant messages found')


def build_profile(source, destination):
    destination.mkdir(mode=0o700)
    for name in ('sessions', 'archived_sessions'):
        if (source / name).is_dir() and not (source / name).is_symlink():
            shutil.copytree(source / name, destination / name, symlinks=True)
    files = {'auth.json', 'session_index.jsonl', 'history.jsonl'}
    files.update(p.name for p in source.glob('state_*.sqlite*'))
    files.update(p.name for p in source.glob('thread_history_*.sqlite*'))
    for name in files:
        path = source / name
        if path.is_file() and not path.is_symlink():
            shutil.copy2(path, destination / name)
    # The minimal profile omits saved hooks, MCP connections and deployment settings.
    (destination / 'config.toml').write_text(
        'sandbox_mode = "read-only"\napproval_policy = "on-request"\n'
        'cli_auth_credentials_store = "file"\n')
    for path in destination.glob('state_*.sqlite'):
        with sqlite3.connect(path) as database:
            columns = {row[1] for row in database.execute('PRAGMA table_info(threads)')}
            if 'rollout_path' not in columns:
                continue
            for thread_id, rollout in database.execute('SELECT id, rollout_path FROM threads').fetchall():
                original = Path(rollout)
                if original.is_relative_to('/home/coder/.codex'):
                    restored = destination / original.relative_to('/home/coder/.codex')
                    database.execute('UPDATE threads SET rollout_path=? WHERE id=?',
                                     (str(restored), thread_id))
            if database.execute('PRAGMA integrity_check').fetchall() != [('ok',)]:
                raise RuntimeError('Restored Codex index failed integrity check')
    return choose_session(destination)


def main():
    if os.geteuid() != 0 or socket.gethostname().split('.')[0] != 'home-lab':
        raise RuntimeError('Run as root on home-lab')
    os.umask(0o077)
    backup = runpy.run_path('/usr/local/sbin/lab-agent-backup', run_name='recovery_helper')
    status = json.loads(backup['STATUS'].read_text())
    cloud = backup['envs']()[1]
    if not TESTS.exists():
        TESTS.mkdir(mode=0o755)
    info = TESTS.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022:
        raise RuntimeError('Recovery-test parent must be a root-owned protected directory')
    # umask 077 narrows mkdir's requested 0755; coder must traverse this parent.
    TESTS.chmod(0o755)
    with tempfile.TemporaryDirectory(prefix='resume-source-', dir=backup['BASE']) as temporary:
        codex_path = backup['VIEW'] / 'coder/.codex'
        backup['restic'](cloud, 'restore', status['cloud_snapshot'], '--target', temporary,
                         '--include', str(codex_path), '--verify')
        restored = Path(temporary) / codex_path.relative_to('/')
        target = Path(tempfile.mkdtemp(prefix='test-', dir=TESTS))
        try:
            profile = target / 'codex'
            session_id = build_profile(restored, profile)
            workspace = target / 'workspace'
            workspace.mkdir(mode=0o700)
            launcher = target / 'open.sh'
            launcher.write_text(
                '#!/usr/bin/bash\nset -eu\n'
                'unset CODEX_SQLITE_HOME\n'
                f'export CODEX_HOME={shlex.quote(str(profile))}\n'
                'exec /home/coder/.local/share/mise/command-wrappers/bin/codex resume '
                f'{shlex.quote(session_id)} --no-daemon --sandbox read-only '
                f'--cd {shlex.quote(str(workspace))}\n')
            launcher.chmod(0o700)
            account = pwd.getpwnam('coder')
            for directory, dirs, files in os.walk(target, followlinks=False):
                for name in dirs + files:
                    os.lchown(Path(directory) / name, account.pw_uid, account.pw_gid)
            os.chown(target, account.pw_uid, account.pw_gid)
        except Exception:
            shutil.rmtree(target)
            raise
    print(f'Restored R2 snapshot: {status["cloud_snapshot"]}')
    print(f'Test conversation: {session_id}')
    print('Open the restored copy with:')
    print(f'sudo -u coder -H {shlex.quote(str(launcher))}')


if __name__ == '__main__':
    main()
