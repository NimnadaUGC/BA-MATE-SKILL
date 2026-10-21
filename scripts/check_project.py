#!/usr/bin/env python3
"""Offline frontmatter, links, metadata and public-package hygiene checks."""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'ba-mate'


def check_links(directory, boundary):
    errors = []
    for path in directory.rglob('*.md'):
        if 'dist' in path.relative_to(directory).parts:
            continue
        text = path.read_text(encoding='utf-8')
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
            if target.startswith(('https://', 'http://', '#', 'mailto:')):
                continue
            target = target.split('#')[0]
            dest = (path.parent / target).resolve()
            if not dest.is_relative_to(boundary.resolve()) or not dest.exists():
                errors.append(str(path.relative_to(directory)) + ': broken/outside link ' + target)
    return errors


def check(root=ROOT):
    skill = root / 'skills' / 'ba-mate'
    errors = check_links(root, root) + check_links(skill, skill)
    entry = (skill / 'SKILL.md').read_text(encoding='utf-8')
    if not re.match(r'^---\nname: ba-mate\ndescription: "[^\n]+"\n---\n', entry):
        errors.append('Invalid skill frontmatter')
    if '[TODO:' in entry:
        errors.append('Unfinished skill scaffold')
    for path in root.rglob('*'):
        if {'dist', '.git', '__pycache__'} & set(path.relative_to(root).parts):
            continue
        if path.is_symlink():
            errors.append('Symlinked public resource: ' + str(path.relative_to(root)))
        if path.is_file() and path.suffix == '.json':
            try:
                json.loads(path.read_text(encoding='utf-8'))
            except ValueError:
                errors.append('Invalid JSON: ' + str(path.relative_to(root)))
        if path.is_file() and path.suffix in {'.py', '.md', '.json', '.yml', '.yaml', '.toml', '.cff'}:
            text = path.read_text(encoding='utf-8')
            if re.search(r'sk-[A-Za-z0-9]{24,}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----', text):
                errors.append('Potential secret: ' + str(path.relative_to(root)))
    version = (root / 'VERSION').read_text().strip()
    for path in ('plugin.json', '.claude-plugin/plugin.json', 'gemini-extension.json'):
        manifest = json.loads((root / path).read_text())
        if manifest.get('name') != 'ba-mate' or manifest.get('version') != version:
            errors.append('Inconsistent manifest identity/version: ' + path)
    if json.loads((root / '.claude-plugin/marketplace.json').read_text())['plugins'][0]['source'] != './':
        errors.append('Marketplace must resolve to this self-contained source root')
    metadata = (skill / 'agents/openai.yaml').read_text()
    if 'allow_implicit_invocation: false' in metadata:
        errors.append('Implicit invocation must remain enabled')
    return errors


if __name__ == '__main__':
    errors = check()
    for error in errors:
        print(error, file=sys.stderr)
    if not errors:
        print('Frontmatter, local links, versions and public-resource hygiene checks passed.')
    sys.exit(1 if errors else 0)
