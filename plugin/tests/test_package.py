import importlib.util
import json
import tempfile
import unittest
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('plugin_build', ROOT / 'build.py')
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class PackageTests(unittest.TestCase):
    def test_release_archive_is_self_contained_and_reproducible(self):
        with tempfile.TemporaryDirectory() as directory:
            archives = [Path(directory) / name for name in ('first.zip', 'second.zip')]
            for archive in archives:
                subprocess.run(['python3', str(ROOT / 'build.py'), str(archive)], check=True, capture_output=True)
            self.assertEqual(archives[0].read_bytes(), archives[1].read_bytes())
            with zipfile.ZipFile(archives[0]) as archive:
                files = {name.removeprefix('codex-market-skills/'): archive.read(name).decode() for name in archive.namelist()}
            self.assertEqual(build.validate(files)['version'], '0.1.9')
            for relative in json.loads((ROOT / 'shared-references.json').read_text()):
                self.assertEqual(files['skills/' + relative], (ROOT.parent / 'skills' / relative).read_text())
            self.assertFalse(any(p.startswith(('docs/', 'tests/')) or p.endswith('.py') for p in files))

    def test_missing_research_reference_fails(self):
        files = build.package_files()
        del files['skills/market-daily-strategist/references/strategy-archetypes.md']
        with self.assertRaisesRegex(AssertionError, 'Unbundled reference'):
            build.validate(files)

    def test_private_path_fails_before_packaging(self):
        files = build.package_files()
        files['skills/market-daily-strategist/references/private.md'] = '/Users/example/private-account'
        with self.assertRaisesRegex(AssertionError, 'Private content'):
            build.validate(files)


if __name__ == '__main__':
    unittest.main()
