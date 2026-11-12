"""Exercise private address migration without accessing installed services."""
import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location('collector', HERE / 'collect.py')
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)


class CollectorConfigurationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)

    def refresh(self, supplied=None, existing=None):
        # Relocate all installation paths and bypass only the root/hostname guards.
        # Stop at collector replacement, before any systemd files can be written.
        home = self.base / 'home/lab-backup'
        credentials = home / 'credentials'
        credentials.mkdir(parents=True)
        if existing is not None:
            (credentials / 'remote-ip').write_text(existing + '\n')
        destination = self.base / 'usr/local/sbin/lab-backup-collect'
        destination.parent.mkdir(parents=True)
        destination.write_text('working collector')
        script = (HERE / 'install-home.sh').read_text()
        script = script.replace('[[ $EUID == 0 ]]', 'true')
        script = script.replace('/home/lab-backup', str(home))
        script = script.replace('/usr/local/sbin/lab-backup-collect', str(destination))
        script = script.replace('install -m 755 -o root -g root "$source_dir/collect.py"',
                                'exit 77\ninstall -m 755 -o root -g root "$source_dir/collect.py"')
        installer = self.base / 'install-home.sh'
        installer.write_text(script)
        mocks = self.base / 'bin'
        mocks.mkdir()
        commands = {
            'hostname': 'echo home-lab',
            'restic': 'exit 0',
            'id': 'exit 0',
            'chown': 'exit 0',
            'install': 'mkdir -p "' + str(credentials) + '"',
        }
        for name, body in commands.items():
            path = mocks / name
            path.write_text('#!/bin/bash\n' + body + '\n')
            path.chmod(0o755)
        env = dict(os.environ, PATH=str(mocks) + ':' + os.environ['PATH'])
        env.pop('BACKUP_EXPORTER_IP', None)
        if supplied is not None:
            env['BACKUP_EXPORTER_IP'] = supplied
        result = subprocess.run(['bash', str(installer), '--refresh-services'],
                                env=env, capture_output=True, text=True)
        self.assertEqual(destination.read_text(), 'working collector')
        return result, credentials / 'remote-ip'

    def test_old_installation_stops_before_replacing_working_collector(self):
        result, path = self.refresh()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Set BACKUP_EXPORTER_IP', result.stderr)
        self.assertFalse(path.exists())

    def test_invalid_input_stops_before_replacing_working_collector(self):
        result, path = self.refresh(supplied='not-an-address')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('valid IPv4', result.stderr)
        self.assertFalse(path.exists())

    def test_explicit_address_is_installed_before_collector_replacement(self):
        result, path = self.refresh(supplied='192.0.2.20')
        self.assertEqual(result.returncode, 77, result.stderr)
        self.assertEqual(path.read_text(), '192.0.2.20\n')
        self.assertEqual(path.stat().st_mode & 0o777, 0o600)

    def test_refresh_reuses_existing_private_address(self):
        result, path = self.refresh(existing='192.0.2.30')
        self.assertEqual(result.returncode, 77, result.stderr)
        self.assertEqual(path.read_text(), '192.0.2.30\n')

    def test_collection_uses_configured_exporter_for_ssh(self):
        credentials = self.base / 'credentials'
        credentials.mkdir()
        (credentials / 'remote-ip').write_text('192.0.2.40\n')
        staging = self.base / 'staging'
        staging.mkdir()
        with patch.object(collector, 'BASE', self.base), \
                patch.object(collector, 'STAGING', staging), \
                patch.object(collector.shutil, 'disk_usage',
                             return_value=SimpleNamespace(free=50 * 1024**3)), \
                patch.object(collector, 'run', side_effect=RuntimeError('stop at SSH')) as run:
            with self.assertRaisesRegex(RuntimeError, 'stop at SSH'):
                collector.collect()
        self.assertEqual(run.call_args.args[0][-2:], ['lab-backup@192.0.2.40', 'export'])


if __name__ == '__main__':
    unittest.main()
