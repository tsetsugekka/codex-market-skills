"""Build the marketplace variant with explicit shared research references."""
import argparse
import json
import posixpath
import re
import zipfile
from pathlib import Path
from pathlib import PurePosixPath

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
PRIVATE_NAMES = {'.local', 'private', 'private-rag', 'private-references',
                 'private_rag', 'private_references', 'rag_index'}


def reject_unsafe_path(path, root):
    if root.is_symlink():
        raise ValueError(f'Symlink in package source: {root}')
    current = root
    for part in path.relative_to(root).parts:
        current = current / part
        if part.casefold() in PRIVATE_NAMES:
            raise ValueError(f'Private package source: {current}')
        if current.is_symlink():
            raise ValueError(f'Symlink in package source: {current}')


def source_files(folder):
    reject_unsafe_path(folder, ROOT)
    for source in sorted(folder.iterdir()):
        reject_unsafe_path(source, ROOT)
        if source.is_dir():
            yield from source_files(source)
        elif source.is_file():
            yield source


def package_files():
    files = {}
    for entry in ROOT.iterdir():
        if entry.name.casefold() in PRIVATE_NAMES:
            raise ValueError(f'Private package source: {entry}')
    for folder in ('.codex-plugin', 'skills', 'assets'):
        for source in source_files(ROOT / folder):
            files[source.relative_to(ROOT).as_posix()] = source.read_text()
    for name in ('shared-references.json', 'shared-scripts.json'):
        reject_unsafe_path(ROOT / name, ROOT)
    resources = json.loads((ROOT / 'shared-references.json').read_text())
    resources += json.loads((ROOT / 'shared-scripts.json').read_text())
    for relative in resources:
        if (not isinstance(relative, str) or not relative or
                relative != str(PurePosixPath(relative)) or
                PurePosixPath(relative).is_absolute() or
                '..' in PurePosixPath(relative).parts or '\\' in relative):
            raise ValueError(f'Invalid shared resource: {relative}')
        source_root = REPO / 'skills'
        source = source_root / relative
        reject_unsafe_path(source, source_root)
        if not source.resolve().is_relative_to(source_root.resolve()):
            raise ValueError(f'Shared resource outside source: {relative}')
        if not source.is_file():
            raise ValueError(f'Missing shared resource: {relative}')
        destination = 'skills/' + relative
        if destination in files:
            raise ValueError(f'Duplicate authority: {destination}')
        files[destination] = source.read_text()
    for path, content in list(files.items()):
        def resolve(match):
            target = match.group(1)
            if re.match(r'^(?:\.\./){3,}skills/', target):
                target = posixpath.relpath(re.sub(r'^(?:\.\./)+', '', target), posixpath.dirname(path))
            return '](' + target + ')'
        files[path] = re.sub(r'\]\(([^)]+)\)', resolve, content)
    return files


def validate(files):
    manifest = json.loads(files['.codex-plugin/plugin.json'])
    skills = [p for p in files if p.endswith('/SKILL.md')]
    if len(skills) != 10:
        raise ValueError('Expected ten skills')
    for path, content in files.items():
        if Path(path).suffix not in {'.md', '.json', '.svg', '.py'}:
            raise ValueError(f'Unsupported package file: {path}')
        if re.search(r'/Users/|/private/tmp/|api_secrets\.env|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY|sk-proj-[A-Za-z0-9_-]+', content):
            raise ValueError(f'Private content: {path}')
        if path in skills:
            name = Path(path).parent.name
            if not re.search(r'^---\nname: ' + re.escape(name) + r'\n', content):
                raise ValueError(f'Invalid skill name: {path}')
            if not re.search(r'^description: .+', content, re.M):
                raise ValueError(f'Missing skill description: {path}')
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
    args = parser.parse_args()
    target = args.output.resolve()
    assert not target.is_relative_to(REPO), 'Write packages outside the source repository'
    files = package_files()
    manifest = validate(files)
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path, content in sorted(files.items()):
            item = zipfile.ZipInfo(manifest['name'] + '/' + path, (2026, 9, 21, 0, 0, 0))
            item.compress_type = zipfile.ZIP_DEFLATED
            item.external_attr = 0o100644 << 16
            archive.writestr(item, content)
    print(f"{manifest['version']}: 10 skills, {len(files)} files -> {target}")


if __name__ == '__main__':
    main()
