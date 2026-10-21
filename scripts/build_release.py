#!/usr/bin/env python3
"""Build allowlisted, self-contained distributions without changing source files."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'ba-mate'
HOSTS = ('codex', 'claude', 'gemini', 'antigravity')
SOURCE_DIRS = {'skills', 'scripts', 'tests', 'docs', 'examples', 'evaluation', '.github', '.claude-plugin', 'commands'}
SOURCE_FILES = {'README.md', 'LICENSE', 'NOTICE', 'CITATION.cff', 'CHANGELOG.md', 'CONTRIBUTING.md',
                'VERSION', '.gitignore', 'plugin.json', 'gemini-extension.json'}
SAFE_ROOT = SOURCE_DIRS | SOURCE_FILES


def files(root):
    for p in sorted(root.rglob('*')):
        if {'ba-mate-workspace', '.git', '__pycache__', 'private', '.venv'} & set(p.relative_to(root).parts):
            continue
        if p.name == 'state.json' or p.name.startswith('.env') or p.suffix in {'.key', '.pem', '.pyc', '.pyo'}:
            continue
        if p.is_symlink():
            raise ValueError('Symlinked resources cannot enter release archives')
        if p.is_file():
            yield p


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def copy_public(source, destination):
    if source.is_symlink():
        raise ValueError('Symlinked resources cannot enter release archives')
    destination.mkdir(parents=True, exist_ok=True)
    for path in files(source):
        target = destination / path.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def bundle(host, version, stage):
    target = stage / ('ba-mate-' + host)
    target.mkdir()
    copy_public(SKILL, target / 'skills' / 'ba-mate')
    for name in ('LICENSE', 'NOTICE', 'CITATION.cff'):
        shutil.copy2(ROOT / name, target / name)
    # Include complete installation guidance and local installer for every host.
    (target / 'docs').mkdir()
    for name in ('INSTALLATION.md', 'COMPATIBILITY.md'):
        shutil.copy2(ROOT / 'docs' / name, target / 'docs' / name)
    (target / 'scripts').mkdir()
    shutil.copy2(ROOT / 'scripts' / 'install_skill.py', target / 'scripts' / 'install_skill.py')
    (target / 'README.md').write_text(f'# BA Mate {host} distribution\n\nDistribution {version}; canonical skill { (ROOT / "VERSION").read_text().strip() }; framework F4-draft.1; schema 1.\n\nSee docs/INSTALLATION.md for this host. All runtime resources are inside skills/ba-mate. No MCP or provider connection is required. Host runtime qualification is recorded separately in docs/COMPATIBILITY.md.\n', encoding='utf-8')
    if host == 'codex':
        manifest = json.loads((ROOT / 'plugin.json').read_text())
        manifest['version'] = version
        write_json(target / 'plugin.json', manifest)
    elif host == 'claude':
        manifest = json.loads((ROOT / '.claude-plugin' / 'plugin.json').read_text())
        manifest['version'] = version
        write_json(target / '.claude-plugin' / 'plugin.json', manifest)
        shutil.copy2(ROOT / '.claude-plugin' / 'marketplace.json', target / '.claude-plugin' / 'marketplace.json')
    elif host == 'gemini':
        manifest = json.loads((ROOT / 'gemini-extension.json').read_text())
        manifest['version'] = version
        write_json(target / 'gemini-extension.json', manifest)
        shutil.copytree(ROOT / 'commands', target / 'commands')
    write_json(target / 'release.json', {'distribution_version': version, 'canonical_skill_version': (ROOT / 'VERSION').read_text().strip(),
               'framework_version': 'F4-draft.1', 'record_schema': 1, 'host': host, 'qualification': 'structurally checked; live-host runtime pending'})
    verify_core(target)
    return target


def verify_core(target):
    canonical = {p.relative_to(SKILL).as_posix(): p.read_bytes() for p in files(SKILL)}
    installed = target / 'skills' / 'ba-mate'
    packaged = {p.relative_to(installed).as_posix(): p.read_bytes() for p in files(installed)}
    if canonical != packaged:
        raise ValueError('Distribution skill differs from canonical resources')


def archive(directory, path):
    # Fixed entry metadata makes repeated builds deterministic.
    with zipfile.ZipFile(path, 'x', compression=zipfile.ZIP_DEFLATED) as z:
        for p in files(directory):
            info = zipfile.ZipInfo(directory.name + '/' + p.relative_to(directory).as_posix(), date_time=(2026, 10, 13, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, p.read_bytes())


def build(version, output):
    if not re.fullmatch(r'\d+\.\d+\.\d+(?:-rc\.\d+)?', version):
        raise ValueError('Version must be semantic x.y.z or x.y.z-rc.n')
    output.mkdir(parents=True, exist_ok=True)
    destination = output / version
    if destination.exists() or destination.is_symlink():
        raise ValueError('Release directory already exists; use a new output directory for a rebuild')
    # Stage the entire release on the destination volume, then publish together.
    with tempfile.TemporaryDirectory(prefix='.ba-mate-build-', dir=output) as tmp:
        staging = Path(tmp)
        release = staging / 'release'
        release.mkdir()
        for host in HOSTS:
            package = bundle(host, version, staging)
            archive(package, release / f'ba-mate-{host}-{version}.zip')
        source = staging / 'BA-MATE-SKILL'
        source.mkdir()
        for entry in sorted(SAFE_ROOT):
            path = ROOT / entry
            if not path.exists():
                raise ValueError('Missing allowlisted release resource: ' + entry)
            if path.is_symlink():
                raise ValueError('Symlinked resources cannot enter release archives')
            if path.is_dir():
                copy_public(path, source / entry)
            else:
                shutil.copy2(path, source / entry)
        write_json(source / 'release.json', {'distribution_version': version, 'canonical_skill_version': (ROOT / 'VERSION').read_text().strip(),
                   'framework_version': 'F4-draft.1', 'record_schema': 1, 'pilot_status': 'not conducted'})
        archive(source, release / f'ba-mate-source-{version}.zip')
        sums = [hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.name for p in sorted(release.glob('*.zip'))]
        (release / 'SHA256SUMS').write_text('\n'.join(sums) + '\n', encoding='utf-8')
        release.rename(destination)
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', default=(ROOT / 'VERSION').read_text().strip())
    parser.add_argument('--output', type=Path, default=ROOT / 'dist')
    args = parser.parse_args()
    try:
        print('Prepared release archives at ' + str(build(args.version, args.output)))
        return 0
    except (ValueError, OSError) as exc:
        print('BA Mate packaging: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
