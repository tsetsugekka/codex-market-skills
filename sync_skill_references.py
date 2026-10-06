"""Synchronize public common references into each independently installable Skill."""
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMON = ('reference-layers.md', 'runtime-capabilities.md', 'release-and-privacy.md')


def synchronize(check=False):
    stale = []
    for skill in sorted((ROOT / 'skills').glob('*/SKILL.md')):
        for name in COMMON:
            source = ROOT / 'shared/references' / name
            target = skill.parent / 'references' / name
            content = source.read_bytes()
            if target.exists() and target.read_bytes() == content:
                continue
            if check:
                stale.append(str(target.relative_to(ROOT)))
            else:
                target.parent.mkdir(exist_ok=True)
                target.write_bytes(content)
    if stale:
        raise ValueError('Stale or missing common references: ' + ', '.join(stale))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    synchronize(parser.parse_args().check)
