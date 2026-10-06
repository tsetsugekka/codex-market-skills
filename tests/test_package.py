import importlib.util
import posixpath
import re
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('builder', ROOT / 'build_plugin.py')
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class PackageTests(unittest.TestCase):
    def test_archive_matches_canonical_source_and_is_reproducible(self):
        with tempfile.TemporaryDirectory() as directory:
            paths = [Path(directory) / f'{n}.zip' for n in (1, 2)]
            for path in paths:
                subprocess.run(['python3', str(ROOT / 'build_plugin.py'), str(path)], check=True, capture_output=True)
            self.assertEqual(paths[0].read_bytes(), paths[1].read_bytes())
            with zipfile.ZipFile(paths[0]) as z:
                files = {n.split('/', 1)[1]: z.read(n).decode() for n in z.namelist()}
            build.validate(files)
            for name, content in files.items():
                self.assertEqual(content.encode(), (ROOT / name).read_bytes(), name)
                if name.endswith('.py'):
                    compile(content, name, 'exec')
            self.assertEqual(len([n for n in files if n.endswith('/SKILL.md')]), 10)
            self.assertIn('skills/us-stock-gamma-moomoo/scripts/gamma_report.py', files)
            self.assertIn('skills/us-stock-gamma-moomoo/scripts/render_spx_gamma_heatmap.py', files)
            self.assertFalse(any(n.startswith(('plugin/', 'tests/', 'docs/')) for n in files))

    def test_untracked_private_file_is_not_read(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'skills').mkdir()
            (root / 'skills/private.txt').write_text('SECRET')
            with mock.patch.object(build, 'REPO', root), mock.patch.object(build.subprocess, 'check_output', return_value=b''):
                self.assertEqual(build.package_files(), {})

    def test_tracked_private_paths_and_symlinks_rejected_before_read(self):
        for name in ['skills/private/secret.md', 'skills/private-references.md', 'skills/linked.md']:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as d:
                root = Path(d);p = root / name;p.parent.mkdir(parents=True)
                if 'linked' in name:
                    p.symlink_to(root / 'external-secret')
                else:
                    p.write_text('SECRET')
                with mock.patch.object(build, 'REPO', root), mock.patch.object(build.subprocess, 'check_output', return_value=(name+'\0').encode()), mock.patch.object(Path, 'read_text') as read:
                    with self.assertRaises(ValueError):build.package_files()
                    read.assert_not_called()

    def test_missing_reference_rejected(self):
        files = build.package_files()
        del files['skills/market-daily-strategist/references/reference-layers.md']
        with self.assertRaisesRegex(ValueError, 'Unbundled reference'):build.validate(files)

    def test_each_skill_can_be_installed_without_sibling_files(self):
        subprocess.run(['python3', str(ROOT / 'sync_skill_references.py'), '--check'], check=True)
        files = build.package_files()
        for skill in (ROOT / 'skills').glob('*/SKILL.md'):
            prefix = skill.parent.relative_to(ROOT).as_posix() + '/'
            for path, content in files.items():
                if not path.startswith(prefix) or not path.endswith('.md'):
                    continue
                for target in re.findall(r'\]\(([^)]+)\)', content):
                    if '://' in target or target.startswith('#'):
                        continue
                    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(path), target.split('#')[0]))
                    self.assertTrue(resolved.startswith(prefix), f'{path} requires a sibling: {target}')
                    self.assertIn(resolved, files)


if __name__ == '__main__':
    unittest.main()
