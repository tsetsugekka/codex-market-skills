import importlib.util
import json
import tempfile
import unittest
import subprocess
import sys
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
            self.assertEqual(build.validate(files)['version'], '0.1.11')
            for relative in json.loads((ROOT / 'shared-references.json').read_text()):
                self.assertEqual(files['skills/' + relative], (ROOT.parent / 'skills' / relative).read_text())
            scripts = json.loads((ROOT / 'shared-scripts.json').read_text())
            self.assertEqual({p for p in files if p.endswith('.py')}, {'skills/' + p for p in scripts} | {'skills/jp-stock-move-reason/scripts/filter_forum.py'})
            for relative in scripts:
                self.assertEqual(files['skills/' + relative], (ROOT.parent / 'skills' / relative).read_text())
                compile(files['skills/' + relative], relative, 'exec')
            self.assertFalse(any(p.startswith(('docs/', 'tests/')) for p in files))

    def test_missing_research_reference_fails(self):
        files = build.package_files()
        del files['skills/market-daily-strategist/references/strategy-archetypes.md']
        with self.assertRaisesRegex(AssertionError, 'Unbundled reference'):
            build.validate(files)

    def test_packaged_script_entrypoints_and_expiry_values(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, content in build.package_files().items():
                dest = root / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(content)
            for script in root.rglob('*.py'):
                subprocess.run([sys.executable, str(script), '--help'], check=True, capture_output=True)
            script = root / 'skills/us-stock-gamma-moomoo/scripts/option_scenario_table.py'
            for kind, expected in [('C', [0, 0, 10]), ('P', [10, 0, 0])]:
                result = subprocess.run([
                    sys.executable, str(script), '--kind', kind, '--strike', '100', '--iv', '20',
                    '--asof', '2026-09-21T16:00:00-04:00', '--expiry', '2026-09-21T16:00:00-04:00',
                    '--spots', '90,100,110', '--timezone', 'America/New_York',
                ], check=True, text=True, capture_output=True)
                rows = [line.split('|') for line in result.stdout.splitlines()[2:5]]
                self.assertEqual([float(row[2]) for row in rows], expected)

    def test_private_path_fails_before_packaging(self):
        files = build.package_files()
        files['skills/market-daily-strategist/references/private.md'] = '/Users/example/private-account'
        with self.assertRaisesRegex(AssertionError, 'Private content'):
            build.validate(files)


if __name__ == '__main__':
    unittest.main()
