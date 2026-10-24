"""Filesystem guarantees; these checks do not certify model behavior."""
from pathlib import Path
from argparse import Namespace
from contextlib import redirect_stdout
import importlib.util
import io
import re
import stat
import subprocess
import shutil
import json
import hashlib
import sys
import tempfile
import os
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/project-advisor/scripts/workspace.py'
SPEC = importlib.util.spec_from_file_location('advisor_installer', SCRIPT)
INSTALLER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INSTALLER)


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=os.environ.get('ADVISOR_TEST_TMPDIR'))
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / 'target'
        self.project.mkdir()
        self.workspace = self.root / 'advisor'

    def run_setup(self, *extra, project=None, workspace=None, harness='codex'):
        return subprocess.run([sys.executable, str(SCRIPT), '--workspace', str(workspace or self.workspace),
                               '--project', str(project or self.project), '--harness', harness, *extra],
                              capture_output=True, text=True, encoding='utf-8')

    def snapshot(self, workspace=None):
        return {p.name: ('link', os.readlink(p)) if p.is_symlink() else ('file', p.read_bytes())
                for p in (workspace or self.workspace).iterdir()}

    def make_symlink(self, path, target):
        try:
            path.symlink_to(target)
        except OSError as error:
            if os.name == 'nt' and getattr(error, 'winerror', None) == 1314:
                self.skipTest('Windows requires symlink creation privilege (WinError 1314)')
            raise

    def test_method_version_matches_template_and_cli(self):
        template = (SCRIPT.parents[1] / 'templates/AGENTS.md').read_text(encoding='utf-8')
        version = re.search(r'project-advisor method ([^; ]+);', template).group(1)
        self.assertEqual(INSTALLER.VERSION, version)
        result = subprocess.run([sys.executable, str(SCRIPT), '--version'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), f'Project Advisor method {version}')
        self.assertFalse(self.workspace.exists())

    def test_preview_and_idempotent_install(self):
        self.assertEqual(self.run_setup().returncode, 0)
        self.assertFalse(self.workspace.exists())
        self.assertEqual(self.run_setup('--apply').returncode, 0)
        before = {p.name: p.read_bytes() for p in self.workspace.iterdir()}
        self.assertEqual(self.run_setup('--apply').returncode, 0)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.workspace.iterdir()})
        self.assertEqual(list(self.project.iterdir()), [])

    def test_preserves_legacy_state_and_personal_rules(self):
        self.workspace.mkdir()
        state = self.workspace / 'CONSULTOR_STATE.md'
        state.write_bytes(b'# Private state\r\nExisting decisions: keep exact bytes.\r\n')
        local = self.workspace / 'ADVISOR_LOCAL.md'
        local.write_bytes(b'Use Portuguese.\n')
        before = state.read_bytes()
        self.assertNotEqual(self.run_setup('--state-file', state.name, '--apply').returncode, 0)
        self.assertEqual(self.run_setup('--state-file', state.name, '--adopt-existing-state', '--apply').returncode, 0)
        self.assertEqual(state.read_bytes(), before)
        self.assertEqual(local.read_bytes(), b'Use Portuguese.\n')
        self.assertFalse((self.workspace / 'ADVISOR_STATE.md').exists())
        self.assertEqual(self.run_setup('--apply').returncode, 0)
        self.assertEqual(state.read_bytes(), before)

    def test_manifest_errors_preserve_files(self):
        self.assertEqual(self.run_setup('--apply').returncode, 0)
        manifest = self.workspace / '.advisor-workspace.json'
        for invalid in ('{', '[]', '{}', '{"schema": 2}', '{"schema": 1, "project": 3}'):
            manifest.write_text(invalid, encoding='utf-8')
            before = {p.name: p.read_bytes() for p in self.workspace.iterdir()}
            result = self.run_setup('--apply')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('recover the binding', result.stderr)
            self.assertEqual(before, {p.name: p.read_bytes() for p in self.workspace.iterdir()})

    def test_lock_recovery_does_not_remove_existing_lock(self):
        self.assertEqual(self.run_setup('--apply').returncode, 0)
        lock = self.workspace / '.advisor-setup.lock'
        lock.write_text('unknown process', encoding='utf-8')
        before = {p.name: p.read_bytes() for p in self.workspace.iterdir()}
        result = self.run_setup('--apply')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('confirmed stale', result.stderr)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.workspace.iterdir()})

    def test_skill_ancestor_is_rejected_without_writes(self):
        source = self.root / 'advisor-parent' / 'skill'
        shutil.copytree(SCRIPT.parents[1], source)
        parent = source.parent
        result = subprocess.run([sys.executable, str(source / 'scripts/workspace.py'),
                                 '--workspace', str(parent), '--project', str(self.project),
                                 '--harness', 'codex', '--apply'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(parent.iterdir()), [source])

    def test_single_schema_and_lf_output(self):
        source = self.root / 'crlf-skill'
        shutil.copytree(SCRIPT.parents[1], source)
        for relative in ('templates/AGENTS.md', 'references/STATE_SCHEMA.md'):
            path = source / relative
            path.write_bytes(path.read_text(encoding='utf-8').replace('\n', '\r\n').encode('utf-8'))
        result = subprocess.run([sys.executable, str(source / 'scripts/workspace.py'),
                                 '--workspace', str(self.workspace), '--project', str(self.project),
                                 '--harness', 'codex', '--apply'], capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        state = (self.workspace / 'ADVISOR_STATE.md').read_bytes()
        expected = (source / 'references/STATE_SCHEMA.md').read_text(encoding='utf-8')
        self.assertEqual(state, expected.replace('{{PROJECT_NAME}}', self.project.name).encode('utf-8'))
        self.assertNotIn(b'\r', (self.workspace / 'AGENTS.md').read_bytes())
        self.assertNotIn(str(self.project).encode(), state)

    def test_missing_manifest_does_not_overwrite_workspace(self):
        self.assertEqual(self.run_setup('--apply').returncode, 0)
        (self.workspace / '.advisor-workspace.json').unlink()
        before = {p.name: p.read_bytes() for p in self.workspace.iterdir()}
        self.assertNotEqual(self.run_setup('--adopt-existing-state', '--apply').returncode, 0)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.workspace.iterdir()})

    def test_legacy_template_is_preserved(self):
        self.workspace.mkdir()
        template = self.workspace / 'CONSULTOR_STATE_TEMPLATE.md'
        template.write_bytes(b'legacy template')
        self.assertNotEqual(self.run_setup('--apply').returncode, 0)
        self.assertEqual(list(self.workspace.iterdir()), [template])
        self.assertEqual(template.read_bytes(), b'legacy template')

    def test_refuses_project_switch_and_modified_instructions(self):
        self.assertEqual(self.run_setup('--apply').returncode, 0)
        other = self.root / 'other'
        other.mkdir()
        self.assertNotEqual(self.run_setup('--apply', project=other).returncode, 0)
        agents = self.workspace / 'AGENTS.md'
        agents.write_text('My custom instructions', encoding='utf-8')
        self.assertNotEqual(self.run_setup('--apply').returncode, 0)
        self.assertEqual(agents.read_text(), 'My custom instructions')

    def test_separate_projects_have_separate_states(self):
        self.assertEqual(self.run_setup('--apply').returncode, 0)
        second = self.root / 'second-target'
        second.mkdir()
        workspace = self.root / 'second-advisor'
        self.assertEqual(self.run_setup('--apply', project=second, workspace=workspace).returncode, 0)
        self.assertNotEqual((workspace / 'ADVISOR_STATE.md').read_bytes(),
                            (self.workspace / 'ADVISOR_STATE.md').read_bytes())

    def test_harness_adapters(self):
        for harness in ('codex', 'claude', 'opencode'):
            with self.subTest(harness=harness):
                ws = self.root / harness
                self.assertEqual(self.run_setup('--apply', workspace=ws, harness=harness).returncode, 0)
                self.assertTrue((ws / 'AGENTS.md').exists())
                if harness == 'claude':
                    self.assertEqual((ws / 'CLAUDE.md').read_text(), '# Project Advisor workspace\n\n@AGENTS.md\n')
                else:
                    self.assertFalse((ws / 'CLAUDE.md').exists())

    def test_refuses_harness_change_without_writes(self):
        self.assertEqual(self.run_setup('--apply').returncode, 0)
        before = self.snapshot()
        for harness in ('claude', 'opencode'):
            with self.subTest(harness=harness):
                result = self.run_setup('--apply', harness=harness)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Harness change', result.stderr)
                self.assertEqual(self.snapshot(), before)

    def test_refuses_competing_states_without_writes(self):
        self.workspace.mkdir()
        for name in INSTALLER.STATE_NAMES:
            (self.workspace / name).write_bytes(b'Private decisions for this project.\n')
        before = self.snapshot()
        for name in INSTALLER.STATE_NAMES:
            with self.subTest(state=name):
                result = self.run_setup('--state-file', name, '--adopt-existing-state', '--apply')
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Another state exists', result.stderr)
                self.assertEqual(self.snapshot(), before)

    def test_refuses_state_filename_conflict_without_writes(self):
        self.assertEqual(self.run_setup('--apply').returncode, 0)
        before = self.snapshot()
        result = self.run_setup('--state-file', 'CONSULTOR_STATE.md', '--apply')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Preserve the existing state filename', result.stderr)
        self.assertEqual(self.snapshot(), before)

    def test_refuses_local_overrides_without_writes(self):
        for name in ('AGENTS.override.md', 'CLAUDE.local.md'):
            with self.subTest(override=name):
                ws = self.root / name
                ws.mkdir()
                (ws / name).write_bytes(b'Custom local instructions.\n')
                before = self.snapshot(ws)
                result = self.run_setup('--apply', workspace=ws)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(name, result.stderr)
                self.assertEqual(self.snapshot(ws), before)

    def test_refuses_unmanaged_claude_in_other_harnesses(self):
        for harness in ('codex', 'opencode'):
            with self.subTest(harness=harness):
                ws = self.root / harness
                ws.mkdir()
                (ws / 'CLAUDE.md').write_bytes(b'Custom Claude instructions.\n')
                before = self.snapshot(ws)
                result = self.run_setup('--apply', harness=harness, workspace=ws)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Existing CLAUDE.md', result.stderr)
                self.assertEqual(self.snapshot(ws), before)

    def test_refuses_symlinks_without_touching_destinations(self):
        names = ('AGENTS.md', 'CLAUDE.md', '.advisor-workspace.json', 'ADVISOR_STATE.md',
                 'CONSULTOR_STATE.md', 'AGENTS.override.md', 'CLAUDE.local.md')
        for name in names:
            for dangling in (False, True):
                with self.subTest(name=name, dangling=dangling):
                    ws = self.root / f'{name}-{dangling}'
                    ws.mkdir()
                    target = self.root / f'target-{name}-{dangling}'
                    if not dangling:
                        target.write_bytes(b'External content must remain unchanged.\n')
                    self.make_symlink(ws / name, target)
                    before = self.snapshot(ws)
                    harness = 'claude' if name == 'CLAUDE.md' else 'codex'
                    result = self.run_setup('--apply', workspace=ws, harness=harness)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(self.snapshot(ws), before)
                    if dangling:
                        self.assertFalse(target.exists())
                    else:
                        self.assertEqual(target.read_bytes(), b'External content must remain unchanged.\n')

    def test_refuses_dangling_claude_in_other_harness(self):
        self.workspace.mkdir()
        target = self.root / 'absent-claude'
        self.make_symlink(self.workspace / 'CLAUDE.md', target)
        before = self.snapshot()
        result = self.run_setup('--apply')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Existing CLAUDE.md', result.stderr)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(target.exists())

    def test_interrupted_install_can_recover_without_rewriting_state(self):
        for harness in ('codex', 'claude'):
            with self.subTest(harness=harness):
                ws = self.root / harness
                args = Namespace(workspace=str(ws), project=str(self.project), harness=harness,
                                 state_file=None, adopt_existing_state=False, apply=True)
                write = INSTALLER.atomic_write

                def fail_before_manifest(path, data):
                    if path.name == INSTALLER.MANIFEST:
                        raise OSError('Injected interruption before manifest')
                    return write(path, data)

                with mock.patch.object(INSTALLER, 'atomic_write', side_effect=fail_before_manifest):
                    with redirect_stdout(io.StringIO()), self.assertRaises(OSError):
                        INSTALLER.prepare(args)
                self.assertFalse((ws / INSTALLER.MANIFEST).exists())
                self.assertFalse((ws / '.advisor-setup.lock').exists())
                state = ws / 'ADVISOR_STATE.md'
                before = self.snapshot(ws)
                state_before = state.read_bytes()
                for extra in ((), ('--adopt-existing-state',)):
                    result = self.run_setup(*extra, '--apply', workspace=ws, harness=harness)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn('backup outside the workspace', result.stderr)
                    self.assertIn('--state-file', result.stderr)
                    self.assertEqual(self.snapshot(ws), before)
                backup = self.root / f'{harness}-backup'
                backup.mkdir()
                orphan_names = ('AGENTS.md', 'CLAUDE.md') if harness == 'claude' else ('AGENTS.md',)
                for name in orphan_names:
                    (ws / name).rename(backup / name)
                    self.assertEqual((backup / name).read_bytes(), before[name][1])
                reviewed = self.snapshot(ws)
                self.assertEqual(self.run_setup('--adopt-existing-state', workspace=ws,
                                                harness=harness).returncode, 0)
                self.assertEqual(self.snapshot(ws), reviewed)
                result = self.run_setup('--adopt-existing-state', '--apply', workspace=ws,
                                        harness=harness)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(state.read_bytes(), state_before)

    @unittest.skipUnless(os.name == 'posix', 'POSIX mode guarantees; Windows uses ACLs')
    def test_new_state_is_private_and_existing_modes_are_preserved(self):
        previous_umask = os.umask(0)
        try:
            self.assertEqual(self.run_setup('--apply').returncode, 0)
        finally:
            os.umask(previous_umask)
        state = self.workspace / 'ADVISOR_STATE.md'
        self.assertEqual(stat.S_IMODE(state.stat().st_mode), 0o600)
        state.chmod(0o640)
        before = state.read_bytes()
        self.assertEqual(self.run_setup('--apply').returncode, 0)
        self.assertEqual(stat.S_IMODE(state.stat().st_mode), 0o640)
        self.assertEqual(state.read_bytes(), before)
        legacy_ws = self.root / 'legacy-advisor'
        legacy_ws.mkdir()
        legacy_state = legacy_ws / 'CONSULTOR_STATE.md'
        legacy_state.write_bytes(b'Private legacy decisions.\r\n')
        legacy_state.chmod(0o640)
        result = self.run_setup('--state-file', legacy_state.name, '--adopt-existing-state',
                                '--apply', workspace=legacy_ws)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(stat.S_IMODE(legacy_state.stat().st_mode), 0o640)
        self.assertEqual(legacy_state.read_bytes(), b'Private legacy decisions.\r\n')

    def test_no_writes_on_conflict_or_external_template(self):
        self.workspace.mkdir()
        template = self.workspace / 'ADVISOR_STATE_TEMPLATE.md'
        template.write_bytes(b'custom state schema')
        self.assertNotEqual(self.run_setup('--apply').returncode, 0)
        self.assertEqual(list(self.workspace.iterdir()), [template])
        template.unlink()
        (self.workspace / 'AGENTS.md').write_bytes(b'existing instructions')
        self.assertNotEqual(self.run_setup('--apply').returncode, 0)
        self.assertFalse((self.workspace / 'ADVISOR_STATE.md').exists())

    def test_refuses_nested_workspace(self):
        nested = self.project / 'advisor'
        self.assertNotEqual(self.run_setup('--apply', workspace=nested).returncode, 0)
        self.assertFalse(nested.exists())

    def test_missing_state_is_not_silently_recreated(self):
        self.assertEqual(self.run_setup('--apply').returncode, 0)
        state = self.workspace / 'ADVISOR_STATE.md'
        state.unlink()
        self.assertNotEqual(self.run_setup('--apply').returncode, 0)
        self.assertFalse(state.exists())

    def test_update_preserves_state_and_refreshes_manifest(self):
        self.assertEqual(self.run_setup('--apply').returncode, 0)
        state = self.workspace / 'ADVISOR_STATE.md'
        before = state.read_bytes()
        source = self.root / 'updated-skill'
        shutil.copytree(SCRIPT.parents[1], source)
        template = source / 'templates/AGENTS.md'
        template.write_text(template.read_text(encoding='utf-8') + '\nUpdated guidance.\n', encoding='utf-8')
        command = [sys.executable, str(source / 'scripts/workspace.py'), '--workspace', str(self.workspace),
                   '--project', str(self.project), '--harness', 'codex']
        old_method = (self.workspace / 'AGENTS.md').read_bytes()
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
        self.assertEqual((self.workspace / 'AGENTS.md').read_bytes(), old_method)
        self.assertEqual(subprocess.run(command + ['--apply'], capture_output=True).returncode, 0)
        method = (self.workspace / 'AGENTS.md').read_bytes()
        self.assertNotEqual(method, old_method)
        self.assertEqual(state.read_bytes(), before)
        manifest = json.loads((self.workspace / '.advisor-workspace.json').read_text())
        self.assertEqual(manifest['files']['AGENTS.md'], hashlib.sha256(method).hexdigest())

    def test_claude_update_preserves_state_and_adapter(self):
        self.assertEqual(self.run_setup('--apply', harness='claude').returncode, 0)
        before = self.snapshot()
        source = self.root / 'updated-claude-skill'
        shutil.copytree(SCRIPT.parents[1], source)
        template = source / 'templates/AGENTS.md'
        template.write_text(template.read_text(encoding='utf-8') + '\nUpdated guidance.\n', encoding='utf-8')
        command = [sys.executable, str(source / 'scripts/workspace.py'), '--workspace', str(self.workspace),
                   '--project', str(self.project), '--harness', 'claude']
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
        self.assertEqual(self.snapshot(), before)
        result = subprocess.run(command + ['--apply'], capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.workspace / 'ADVISOR_STATE.md').read_bytes(), before['ADVISOR_STATE.md'][1])
        self.assertEqual((self.workspace / 'CLAUDE.md').read_bytes(), before['CLAUDE.md'][1])
        manifest = json.loads((self.workspace / INSTALLER.MANIFEST).read_text())
        for name in ('AGENTS.md', 'CLAUDE.md'):
            self.assertEqual(manifest['files'][name], hashlib.sha256((self.workspace / name).read_bytes()).hexdigest())


if __name__ == '__main__':
    unittest.main()
