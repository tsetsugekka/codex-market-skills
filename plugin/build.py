"""Build the marketplace variant with explicit shared research references."""
import argparse
import json
import posixpath
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def package_files():
    files = {}
    for folder in ('.codex-plugin', 'skills', 'assets'):
        for source in sorted((ROOT / folder).rglob('*')):
            if source.is_file():
                files[source.relative_to(ROOT).as_posix()] = source.read_text()
    resources = json.loads((ROOT / 'shared-references.json').read_text())
    resources += json.loads((ROOT / 'shared-scripts.json').read_text())
    for relative in resources:
        source = REPO / 'skills' / relative
        assert source.resolve().is_relative_to(REPO / 'skills'), relative
        destination = 'skills/' + relative
        assert destination not in files, f'Duplicate authority: {destination}'
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
    assert len(skills) == 10, 'Expected ten skills'
    for path, content in files.items():
        assert Path(path).suffix in {'.md', '.json', '.svg', '.py'}, path
        assert not re.search(r'/Users/|/private/tmp/|api_secrets\.env|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY|sk-proj-[A-Za-z0-9_-]+', content), f'Private content: {path}'
        if path in skills:
            name = Path(path).parent.name
            assert re.search(r'^---\nname: ' + re.escape(name) + r'\n', content), path
            assert re.search(r'^description: .+', content, re.M), path
        for target in re.findall(r'\]\(([^)]+)\)', content) if path.endswith('.md') else []:
            if '://' in target or target.startswith('#'):
                continue
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(path), target.split('#')[0]))
            assert resolved in files, f'Unbundled reference: {path} -> {target}'
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
