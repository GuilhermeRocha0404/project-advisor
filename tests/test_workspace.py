"""Filesystem guarantees; these checks do not certify model behavior."""
from pathlib import Path
import subprocess
import shutil
import json
import hashlib
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/project-advisor/scripts/workspace.py'


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / 'target'
        self.project.mkdir()
        self.workspace = self.root / 'advisor'

    def run_setup(self, *extra, project=None, workspace=None, harness='codex'):
        return subprocess.run([sys.executable, str(SCRIPT), '--workspace', str(workspace or self.workspace),
                               '--project', str(project or self.project), '--harness', harness, *extra],
                              capture_output=True, text=True, encoding='utf-8')

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


if __name__ == '__main__':
    unittest.main()
