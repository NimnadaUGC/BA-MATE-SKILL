import importlib.util
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / 'VERSION').read_text().strip()


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / filename)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


builder = module('release_builder', 'build_release.py')
checker = module('project_checker', 'check_project.py')
installer = module('skill_installer', 'install_skill.py')
rehearsal = module('synthetic_rehearsal', 'rehearse.py')


class PackageTests(unittest.TestCase):
    def test_project_links_and_metadata(self):
        self.assertEqual(checker.check(), [])

    def test_five_isolated_bundles_identical_core_and_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            release = builder.build(VERSION, Path(tmp) / 'dist')
            self.assertEqual(len(list(release.glob('*.zip'))), 6)
            for host in builder.HOSTS:
                with zipfile.ZipFile(release / f'ba-mate-{host}-{VERSION}.zip') as archive:
                    archive.extractall(Path(tmp) / 'extracted')
                package = Path(tmp) / 'extracted' / ('ba-mate-' + host)
                builder.verify_core(package)
                self.assertEqual(checker.check_links(package, package), [])
                self.assertEqual(checker.check_links(package / 'skills', package / 'skills'), [])
                helper = package / 'skills/ba-mate/scripts/bamate.py'
                workspace = Path(tmp) / ('workspace-' + host)
                for args in (['initialise'], ['apply', '--patch', str(package / 'skills/ba-mate/assets/example-patch.json'), '--expected-revision', '1'], ['validate']):
                    result = subprocess.run([sys.executable, str(helper), '--workspace', str(workspace), *args], capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0, result.stderr)
                project = Path(tmp) / ('installed-' + host)
                command = [sys.executable, str(package / 'scripts/install_skill.py'), '--host', host, '--project', str(project)]
                result = subprocess.run(command, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                installed = installer.destination_for(host, 'workspace', project)
                self.assertEqual(checker.check_links(installed, installed), [])
                self.assertEqual((installed / 'SKILL.md').read_bytes(), (ROOT / 'skills/ba-mate/SKILL.md').read_bytes())
                again = subprocess.run(command, capture_output=True, text=True)
                self.assertEqual(again.returncode, 2)
                self.assertIn('will not be overwritten', again.stderr)

    def test_release_refuses_overwrite_and_is_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = builder.build(VERSION, Path(tmp) / 'a')
            b = builder.build(VERSION, Path(tmp) / 'b')
            self.assertEqual((a / 'SHA256SUMS').read_bytes(), (b / 'SHA256SUMS').read_bytes())
            with self.assertRaises(ValueError):
                builder.build(VERSION, Path(tmp) / 'a')

    def test_manifest_shapes(self):
        portable = json.loads((ROOT / 'plugin.json').read_text())
        self.assertTrue(portable['$schema'].endswith('plugin.schema.json'))
        self.assertEqual(portable['name'], 'ba-mate')
        self.assertNotIn('mcpServers', portable)
        gemini = json.loads((ROOT / 'gemini-extension.json').read_text())
        self.assertEqual(gemini['name'], 'ba-mate')
        self.assertIn('{{args}}', (ROOT / 'commands/ba-mate.toml').read_text())

    def test_allowlist_excludes_private_state_and_git(self):
        with tempfile.TemporaryDirectory() as tmp:
            release = builder.build(VERSION, Path(tmp))
            for path in release.glob('*.zip'):
                with zipfile.ZipFile(path) as archive:
                    names = archive.namelist()
                self.assertFalse(any('/ba-mate-workspace/' in n or '/.git/' in n or '/__pycache__/' in n for n in names))

    def test_nested_private_files_do_not_enter_public_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'input'
            source.mkdir()
            (source / 'guide.md').write_text('Public guide')
            (source / 'state.json').write_text('Private synthetic state marker')
            (source / '.env.local').write_text('Private synthetic env marker')
            for name in ('.DS_Store', 'Thumbs.db', 'desktop.ini', '~$BA-Mate-Guide.docx'):
                (source / name).write_bytes(b'Fictional desktop metadata')
            (source / 'private').mkdir()
            (source / 'private' / 'notes.md').write_text('Private synthetic notes marker')
            destination = Path(tmp) / 'public'
            builder.copy_public(source, destination)
            self.assertEqual({p.name for p in destination.rglob('*') if p.is_file()}, {'guide.md'})

    def test_installer_isolated_no_overwrite_no_settings_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            settings = project / 'settings.json'
            settings.write_text('Existing unrelated setting')
            target = project / '.agents/skills/ba-mate'
            installer.install(ROOT / 'skills/ba-mate', target)
            self.assertTrue((target / 'SKILL.md').is_file())
            self.assertEqual(settings.read_text(), 'Existing unrelated setting')
            with self.assertRaises(ValueError):
                installer.install(ROOT / 'skills/ba-mate', target)

    def test_three_synthetic_journeys(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = rehearsal.rehearse(Path(tmp) / 'journeys')
            self.assertEqual(set(report['journeys'].values()), {'passed'})
            self.assertFalse(report['participant_evidence'])
            self.assertEqual(report['host_activation'], 'not tested')

    def test_cursor_paths_and_isolation(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / 'project'
            home = Path(tmp) / 'home'
            self.assertEqual(installer.destination_for('cursor', 'workspace', project), project / '.cursor/skills/ba-mate')
            self.assertEqual(installer.destination_for('cursor', 'user', user_home=home), home / '.cursor/skills/ba-mate')
            installer.install(ROOT / 'skills/ba-mate', installer.destination_for('cursor', 'workspace', project))
            self.assertFalse(home.exists())
            self.assertFalse((project / '.agents').exists())
            self.assertFalse((project / '.cursor/settings.json').exists())

    def test_installer_rejects_missing_project_and_unknown_host(self):
        with self.assertRaises(ValueError):
            installer.destination_for('cursor', 'workspace')
        with self.assertRaises(ValueError):
            installer.destination_for('unknown', 'user')

    def test_schema_one_workspace_from_previous_package_still_loads(self):
        state = rehearsal.ba.blank()
        state['package_version'] = '1.0.0'
        rehearsal.ba.check_records(state)
        self.assertEqual(state['package_version'], '1.0.0')
        self.assertEqual(rehearsal.ba.PACKAGE_VERSION, VERSION)

    def test_recorded_runtime_evidence_identifies_tested_core_and_failures(self):
        digest = hashlib.sha256()
        skill = ROOT / 'skills/ba-mate'
        for resource in builder.files(skill):
            digest.update(resource.relative_to(skill).as_posix().encode() + b'\0' + resource.read_bytes())
        records = {host: json.loads((ROOT / f'evaluation/results/{host}-v1.0.5.json').read_text(encoding='utf-8'))
                   for host in ('codex', 'cursor', 'claude', 'antigravity')}
        # Prevent a future edit from quietly inheriting final-core runtime claims.
        final_codex = [c for c in records['codex']['cases'] if c['attempt'] == 2]
        self.assertEqual({c['case_id'] for c in final_codex}, {'S01','S02','S03','S04','S05'})
        self.assertTrue(all(c['canonical_skill_sha256'] == digest.hexdigest() for c in final_codex))
        for record in records.values():
            self.assertEqual(record['package_version'], VERSION)
            for case in record['cases']:
                self.assertTrue(case['task'] and case['prompt'])
                self.assertIsInstance(case['assistance'], list)
                self.assertIn(case['result'], {'passed','failed','blocked','not-run'})
                if case['result'] in {'failed','blocked'}:
                    self.assertTrue(case['failure']['kind'] and case['failure']['detail'])
        self.assertTrue(any(c['result'] == 'failed' for c in records['cursor']['cases']))
        self.assertTrue(any(c['result'] == 'failed' for c in records['antigravity']['cases']))
        self.assertFalse(any(c['result'] == 'passed' for c in records['claude']['cases']))

    def test_installer_excludes_desktop_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'skill'
            source.mkdir()
            (source / 'SKILL.md').write_text('Fictional skill')
            for name in ('.DS_Store', 'Thumbs.db', 'desktop.ini', '~$BA-Mate-Guide.docx'):
                (source / name).write_bytes(b'Fictional desktop metadata')
            target = Path(tmp) / 'installed'
            installer.install(source, target)
            self.assertEqual({p.name for p in target.iterdir()}, {'SKILL.md'})


if __name__ == '__main__':
    unittest.main()
