"""Preflight scope regressions; no credentials, snapshots or repositories accessed."""
import importlib.util
from pathlib import Path
import shutil
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
        self.enterContext(patch.object(agent_backup, 'mounted_paths', return_value=set()))
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

    def test_intermediate_symlink_to_live_data_is_rejected(self):
        live = self.home / 'live-local'
        (self.home / '.local').rename(live)
        (self.home / '.local').symlink_to(live, target_is_directory=True)
        with self.assertRaisesRegex(RuntimeError, 'symlink'):
            agent_backup.preflight()

    def test_mounted_ancestor_is_rejected_even_when_root_is_not_a_mount(self):
        for boundary in (self.home, self.home / '.local'):
            with self.subTest(boundary=boundary):
                with patch.object(agent_backup, 'mounted_paths', return_value={boundary}):
                    with self.assertRaisesRegex(RuntimeError, 'nested storage'):
                        agent_backup.preflight()

    def test_nested_subvolume_ancestor_is_rejected(self):
        original = Path.lstat
        for boundary in (self.home, self.home / '.local'):
            def subvolume(path):
                result = original(path)
                return SimpleNamespace(st_mode=result.st_mode, st_ino=256) if path == boundary else result
            with self.subTest(boundary=boundary), patch.object(Path, 'lstat', subvolume):
                with self.assertRaisesRegex(RuntimeError, 'nested storage'):
                    agent_backup.preflight()

    def test_mounted_file_inside_included_directory_is_rejected(self):
        mounted = self.home / '.codex/auth.json'
        mounted.write_text('private test fixture')
        with patch.object(agent_backup, 'mounted_paths', return_value={mounted}):
            with self.assertRaisesRegex(RuntimeError, 'mounted storage'):
                agent_backup.preflight()

    def test_mounted_excluded_project_checkpoints_do_not_expand_scope(self):
        mounted = self.home / '.local/share/opencode/repos/project'
        mounted.mkdir(parents=True)
        with patch.object(agent_backup, 'mounted_paths', return_value={mounted}):
            roots = agent_backup.preflight()
        self.assertNotIn('.local/share/opencode/repos', roots)

    def freeze(self):
        expected = agent_backup.preflight()
        view = self.home / 'view'
        view.mkdir()
        frozen = view / self.home.name
        for name in expected:
            source = self.home / name
            target = frozen / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, target, symlinks=True)
            else:
                shutil.copy2(source, target)
        self.enterContext(patch.object(agent_backup, 'VIEW', view))
        return expected, frozen

    def test_missing_optional_frozen_root_fails_instead_of_being_skipped(self):
        expected, frozen = self.freeze()
        (frozen / '.t3/service.env').unlink()
        with self.assertRaisesRegex(RuntimeError, 'Frozen agent root missing'):
            agent_backup.frozen_roots(expected)

    def test_frozen_intermediate_symlink_cannot_redirect_backup_to_live_data(self):
        expected, frozen = self.freeze()
        shutil.rmtree(frozen / '.local')
        (frozen / '.local').symlink_to(self.home / '.local', target_is_directory=True)
        with self.assertRaisesRegex(RuntimeError, 'symlink'):
            agent_backup.frozen_roots(expected)

    def test_shared_skill_metadata_and_payload_use_the_same_frozen_view(self):
        metadata = self.home / '.local/state/lab-skills'
        metadata.mkdir(parents=True)
        payload = self.home / '.agents/skills/example'
        payload.mkdir(parents=True)
        for name in ('state.json', 'journal.json', 'apply.lock'):
            (metadata / name).write_text('before')
        (payload / 'SKILL.md').write_text('before')
        expected, frozen = self.freeze()
        (metadata / 'state.json').write_text('after')
        (payload / 'SKILL.md').write_text('after')
        roots = agent_backup.frozen_roots(expected)
        self.assertIn(str(frozen / '.local/state/lab-skills'), roots)
        self.assertIn(str(frozen / '.agents'), roots)
        for name in ('state.json', 'journal.json', 'apply.lock'):
            self.assertEqual((frozen / '.local/state/lab-skills' / name).read_text(), 'before')
        self.assertEqual((frozen / '.agents/skills/example/SKILL.md').read_text(), 'before')


if __name__ == '__main__':
    unittest.main()
