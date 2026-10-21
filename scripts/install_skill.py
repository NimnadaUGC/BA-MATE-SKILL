#!/usr/bin/env python3
"""Copy only the BA Mate skill, refusing to overwrite existing installations."""
import argparse
from pathlib import Path
import os
import shutil
import sys
import tempfile


def install(source, destination):
    if destination.exists() or destination.is_symlink():
        raise ValueError('Existing installation will not be overwritten; preserve/remove it explicitly first')
    if not (source / 'SKILL.md').is_file():
        raise ValueError('Source does not contain SKILL.md')
    if source.is_symlink() or any(p.is_symlink() for p in source.rglob('*')):
        raise ValueError('Symlinked package resources are unsupported')
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix='.ba-mate-install-', dir=destination.parent))
    lock = destination.parent / '.ba-mate-install.lock'
    try:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError as exc:
            raise ValueError('Another BA Mate installation is active or its lock requires examination') from exc
        try:
            os.close(fd)
            shutil.copytree(source, temporary / 'ba-mate', ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            if destination.exists() or destination.is_symlink():
                raise ValueError('Installation appeared during copy; nothing overwritten')
            # Rename on the same volume; no settings files are touched.
            (temporary / 'ba-mate').rename(destination)
        finally:
            lock.unlink()
    finally:
        shutil.rmtree(temporary)
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', choices=['codex', 'claude', 'gemini', 'antigravity'], required=True)
    parser.add_argument('--scope', choices=['workspace', 'user'], default='workspace')
    parser.add_argument('--project', type=Path)
    parser.add_argument('--source', type=Path, default=Path(__file__).resolve().parents[1] / 'skills' / 'ba-mate')
    args = parser.parse_args()
    if args.scope == 'workspace' and args.project is None:
        parser.error('--project is required for a workspace installation')
    base = args.project.absolute() if args.scope == 'workspace' else Path.home()
    folders = {'codex': '.agents/skills', 'claude': '.claude/skills', 'gemini': '.gemini/skills',
               'antigravity': '.agents/skills' if args.scope == 'workspace' else '.gemini/config/skills'}
    try:
        target = install(args.source, base / folders[args.host] / 'ba-mate')
        print('Installed only the BA Mate skill at ' + str(target))
        return 0
    except (OSError, ValueError) as exc:
        print('BA Mate installation: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
