"""Preflight scope regressions; no credentials, snapshots or repositories accessed."""
import importlib.util
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('agent_backup', Path(__file__).with_name('agents.py'))
agent_backup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agent_backup)


class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        (self.home / '.codex/sessions').mkdir(parents=True)
        (self.home / '.local/share/opencode').mkdir(parents=True)
        (self.home / '.t3').mkdir()
        self.env_file = self.home / '.t3/service.env'
        self.env_file.write_text('EXAMPLE=value\n')
        for target, value in (('HOME', self.home), ('BASE', self.home)):
            self.enterContext(patch.object(agent_backup, target, value))
        self.enterContext(patch.object(agent_backup.sp, 'check_output', return_value='btrfs\n'))
        self.enterContext(patch.object(agent_backup.shutil, 'disk_usage',
                                      return_value=SimpleNamespace(free=50 * 1024**3)))

    def test_regular_configuration_file_is_accepted_without_changes(self):
        agent_backup.preflight()
        self.assertEqual(self.env_file.read_text(), 'EXAMPLE=value\n')

    def test_unreadable_directory_is_reported_instead_of_skipped(self):
        with patch.object(agent_backup.os, 'scandir', side_effect=PermissionError('test denial')):
            with self.assertRaises(PermissionError):
                agent_backup.preflight()

    def test_configuration_symlink_requires_scope_review(self):
        self.env_file.unlink()
        self.env_file.symlink_to(self.home / '.codex')
        with self.assertRaisesRegex(RuntimeError, 'symlink'):
            agent_backup.preflight()


if __name__ == '__main__':
    unittest.main()
