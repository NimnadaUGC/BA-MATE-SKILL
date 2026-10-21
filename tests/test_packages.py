import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


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

    def test_four_isolated_bundles_identical_core_and_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            release = builder.build('1.0.0', Path(tmp) / 'dist')
            self.assertEqual(len(list(release.glob('*.zip'))), 5)
            for host in builder.HOSTS:
                with zipfile.ZipFile(release / f'ba-mate-{host}-1.0.0.zip') as archive:
                    archive.extractall(Path(tmp) / 'extracted')
                package = Path(tmp) / 'extracted' / ('ba-mate-' + host)
                builder.verify_core(package)
                self.assertEqual(checker.check_links(package / 'skills', package / 'skills'), [])
                helper = package / 'skills/ba-mate/scripts/bamate.py'
                workspace = Path(tmp) / ('workspace-' + host)
                for args in (['initialise'], ['apply', '--patch', str(package / 'skills/ba-mate/assets/example-patch.json'), '--expected-revision', '1'], ['validate']):
                    result = subprocess.run([sys.executable, str(helper), '--workspace', str(workspace), *args], capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0, result.stderr)

    def test_release_refuses_overwrite_and_is_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = builder.build('1.0.0-rc.1', Path(tmp) / 'a')
            b = builder.build('1.0.0-rc.1', Path(tmp) / 'b')
            self.assertEqual((a / 'SHA256SUMS').read_bytes(), (b / 'SHA256SUMS').read_bytes())
            with self.assertRaises(ValueError):
                builder.build('1.0.0-rc.1', Path(tmp) / 'a')

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
            release = builder.build('1.0.0', Path(tmp))
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


if __name__ == '__main__':
    unittest.main()
