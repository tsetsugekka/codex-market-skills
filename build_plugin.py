"""Package the tracked, canonical skills without rewriting their contents."""
import argparse
import json
import posixpath
import re
import subprocess
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent
PRIVATE_NAMES = {'.local', 'private', 'private-rag', 'private-references',
                 'private_rag', 'private_references', 'rag_index'}


def package_files():
    paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=REPO).decode().split('\0')
    files = {}
    for relative in sorted(paths):
        path = Path(relative)
        if not (relative.startswith('skills/') or relative in {'.codex-plugin/plugin.json', 'assets/logo.svg'}):
            continue
        if any(part.casefold() in PRIVATE_NAMES or part == 'private-references.md' for part in path.parts):
            raise ValueError(f'Private package source: {relative}')
        source = REPO
        for part in path.parts:
            source = source / part
            if source.is_symlink():
                raise ValueError(f'Symlink in package source: {relative}')
        if path.name.startswith('test_') or 'tests' in path.parts:
            continue
        files[relative] = source.read_text()
    return files


def validate(files):
    manifest = json.loads(files['.codex-plugin/plugin.json'])
    skills = [p for p in files if p.endswith('/SKILL.md')]
    if len(skills) != 10:
        raise ValueError('Expected ten skills')
    for path, content in files.items():
        if Path(path).suffix not in {'.md', '.json', '.svg', '.py', '.yaml', '.html'}:
            raise ValueError(f'Unsupported package file: {path}')
        if re.search(r'/Users/|/private/tmp/|api_secrets\.env|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY|sk-proj-[A-Za-z0-9_-]+', content):
            raise ValueError(f'Private content: {path}')
        if path in skills:
            if not re.search(r'^---\nname: ' + re.escape(Path(path).parent.name) + r'\n', content):
                raise ValueError(f'Invalid skill name: {path}')
            if not re.search(r'^description: .+', content, re.M):
                raise ValueError(f'Missing description: {path}')
        for target in re.findall(r'\]\(([^)]+)\)', content) if path.endswith('.md') else []:
            if '://' in target or target.startswith('#'):
                continue
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(path), target.split('#')[0]))
            if resolved not in files:
                raise ValueError(f'Unbundled reference: {path} -> {target}')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    target = parser.parse_args().output.resolve()
    if target.is_relative_to(REPO):
        raise ValueError('Write packages outside the source repository')
    files = package_files()
    manifest = validate(files)
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path, content in sorted(files.items()):
            item = zipfile.ZipInfo(manifest['name'] + '/' + path, (2026, 10, 6, 0, 0, 0))
            item.compress_type = zipfile.ZIP_DEFLATED
            item.external_attr = 0o100644 << 16
            archive.writestr(item, content)
    print(f"{manifest['version']}: {len(files)} files -> {target}")


if __name__ == '__main__':
    main()
