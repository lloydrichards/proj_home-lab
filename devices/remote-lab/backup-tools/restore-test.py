#!/usr/bin/python3
"""Restore saved PostgreSQL dumps on remote-lab without a network or published ports."""
import json
import os
from pathlib import Path
import subprocess as sp
import shutil
import sqlite3
import sys
import tarfile
import tempfile
import time

BASE = Path('/var/lib/lab-backup-export')


def sqlite_tests(source):
    checked = []
    with tempfile.TemporaryDirectory(dir=BASE) as temp, tarfile.open(source / 'data.tar') as archive:
        names = {m.name: m for m in archive.getmembers() if m.isfile()}
        for name, member in names.items():
            with archive.extractfile(member) as src:
                header = src.read(16)
                if header != b'SQLite format 3\x00':
                    continue
                target = Path(temp) / str(len(checked))
                with target.open('wb') as dst:
                    dst.write(header)
                    shutil.copyfileobj(src, dst)
            # Restore the accompanying WAL, if present. SQLite rebuilds SHM.
            wal = names.get(name + '-wal')
            if wal:
                with archive.extractfile(wal) as src, Path(str(target) + '-wal').open('wb') as dst:
                    shutil.copyfileobj(src, dst)
            with sqlite3.connect(target) as db:
                if db.execute('PRAGMA integrity_check').fetchall() != [('ok',)]:
                    raise RuntimeError('Restored SQLite database plus WAL failed integrity check')
                db.execute('SELECT count(*) FROM sqlite_master').fetchone()
            checked.append({'path': name, 'wal_included': wal is not None, 'integrity': 'passed'})
    if len(checked) < 5:
        raise RuntimeError('Expected at least five restored application databases')
    return checked


def main():
    os.umask(0o077)
    source = (BASE / 'latest').resolve()
    sqlite_results = sqlite_tests(source)
    if sys.argv[1:] == ['--sqlite-only']:
        report_path = BASE / 'restore-test.json'
        report = json.loads(report_path.read_text())
        if report['generation'] != source.name:
            raise RuntimeError('PostgreSQL test belongs to a different generation')
        report['sqlite'] = sqlite_results
        report_path.write_text(json.dumps(report, indent=2))
        print(json.dumps({'sqlite_databases_restored': len(sqlite_results), 'integrity': 'passed'}))
        return
    if sys.argv[1:]:
        raise RuntimeError('Unsupported operation')
    inventory = json.loads((source / 'containers.json').read_text())
    results = []
    with (BASE / 'restore-test.log').open('wb') as log:
        def run(args, **kw):
            return sp.run(args, check=True, stdout=log, stderr=log, **kw)

        for index, dump in enumerate(sorted((source / 'postgres').glob('*.sql'))):
            original = next(c for c in inventory if c['Name'].lstrip('/') == dump.stem)
            name = f'lab-backup-restore-{os.getpid()}-{index}'
            try:
                run(['docker', 'run', '-d', '--name', name, '--network', 'none',
                     '--label', 'home-lab.backup-restore-test=true', '--restart=no',
                     '--tmpfs', '/restore-data:rw,size=1073741824',
                     '-e', 'PGDATA=/restore-data', '-e', 'POSTGRES_USER=lab_restore_admin',
                     '-e', 'POSTGRES_DB=lab_restore_admin',
                     '-e', 'POSTGRES_HOST_AUTH_METHOD=trust', original['Image']])
                for _ in range(90):
                    ready = sp.run(['docker', 'exec', name, 'pg_isready', '-U', 'lab_restore_admin'],
                                   stdout=sp.DEVNULL, stderr=sp.DEVNULL)
                    if ready.returncode == 0:
                        break
                    time.sleep(1)
                else:
                    raise RuntimeError('Isolated restore database did not start')
                with dump.open('rb') as inp:
                    run(['docker', 'exec', '-i', name, 'psql', '-U', 'lab_restore_admin',
                         '-d', 'lab_restore_admin', '-v', 'ON_ERROR_STOP=1'], stdin=inp)
                names = sp.check_output(['docker', 'exec', name, 'psql', '-U', 'lab_restore_admin',
                                         '-d', 'lab_restore_admin', '-Atc',
                                         "SELECT datname FROM pg_database WHERE NOT datistemplate AND datname != 'lab_restore_admin'"],
                                        text=True).splitlines()
                for database in names:
                    run(['docker', 'exec', name, 'psql', '-U', 'lab_restore_admin', '-d', database,
                         '-v', 'ON_ERROR_STOP=1', '-Atc',
                         "SELECT count(*) FROM information_schema.tables WHERE table_schema='public'"])
                result = {'source_container': dump.stem, 'cluster_restore': 'passed',
                          'databases_readable': names}
                if dump.stem == 'coolify-db':
                    run(['docker', 'exec', name, 'createdb', '-U', 'lab_restore_admin', 'coolify_custom_test'])
                    with (source / 'postgres/coolify.dmp').open('rb') as inp:
                        run(['docker', 'exec', '-i', name, 'pg_restore', '-U', 'lab_restore_admin',
                             '-d', 'coolify_custom_test', '--no-owner', '--no-acl', '--exit-on-error'], stdin=inp)
                    # Verify a saved encrypted SSH key with the APP_KEY from the archive.
                    cipher = sp.check_output(['docker', 'exec', name, 'psql', '-U', 'lab_restore_admin',
                                              '-d', 'coolify_custom_test', '-Atc',
                                              'SELECT private_key FROM private_keys WHERE private_key IS NOT NULL LIMIT 1'])
                    with tarfile.open(source / 'data.tar') as archive:
                        env = archive.extractfile('data/coolify/source/.env').read().decode()
                    key = next(line.split('=', 1)[1].strip().strip('"\'') for line in env.splitlines()
                               if line.startswith('APP_KEY='))
                    if not cipher.strip():
                        raise RuntimeError('No encrypted credential available for restore verification')
                    php = r'''
                    require '/var/www/html/vendor/autoload.php';
                    $v=json_decode(stream_get_contents(STDIN),true,512,JSON_THROW_ON_ERROR);
                    $key=$v['key'];
                    if(str_starts_with($key,'base64:')) $key=base64_decode(substr($key,7));
                    $e=new Illuminate\Encryption\Encrypter($key,'AES-256-CBC');
                    $plain=$e->decryptString($v['cipher']);
                    if(!str_contains($plain,'PRIVATE KEY')) exit(2);
                    echo "Saved credential decryption passed\n";
                    '''
                    payload = json.dumps({'key': key, 'cipher': cipher.decode().strip()}).encode()
                    run(['docker', 'exec', '-i', 'coolify', 'php', '-r', php], input=payload)
                    result['custom_dump_restore'] = 'passed'
                    result['saved_credential_decryption'] = 'passed'
                results.append(result)
            finally:
                sp.run(['docker', 'rm', '-f', '-v', name], stdout=log, stderr=log)
    report = {'generation': source.name, 'postgresql': results, 'sqlite': sqlite_results,
              'isolation': 'network none; no published ports; temporary database data',
              'limit': 'Database and saved credential recovery; full Coolify dashboard and end-to-end app UI recovery not exercised'}
    (BASE / 'restore-test.json').write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
