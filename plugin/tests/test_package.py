import importlib.util
import json
import tempfile
import unittest
import subprocess
import sys
import zipfile
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('plugin_build', ROOT / 'build.py')
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class PackageTests(unittest.TestCase):
    def fake_sources(self, directory):
        repo = Path(directory)
        plugin = repo / 'plugin'
        for name in ('.codex-plugin', 'skills', 'assets'):
            (plugin / name).mkdir(parents=True)
        (repo / 'skills').mkdir()
        for name in ('shared-references.json', 'shared-scripts.json'):
            (plugin / name).write_text('[]')
        return repo, plugin

    def assert_rejected_without_reading(self, repo, plugin, forbidden):
        reads = []
        read_text = Path.read_text

        def record_read(path, *args, **kwargs):
            reads.append(path)
            return read_text(path, *args, **kwargs)

        with mock.patch.object(build, 'ROOT', plugin), mock.patch.object(build, 'REPO', repo), \
                mock.patch.object(Path, 'read_text', record_read):
            with self.assertRaises(ValueError):
                build.package_files()
        self.assertNotIn(forbidden, reads)

    def test_release_archive_is_self_contained_and_reproducible(self):
        with tempfile.TemporaryDirectory() as directory:
            archives = [Path(directory) / name for name in ('first.zip', 'second.zip')]
            for archive in archives:
                subprocess.run(['python3', str(ROOT / 'build.py'), str(archive)], check=True, capture_output=True)
            self.assertEqual(archives[0].read_bytes(), archives[1].read_bytes())
            with zipfile.ZipFile(archives[0]) as archive:
                files = {name.removeprefix('codex-market-skills/'): archive.read(name).decode() for name in archive.namelist()}
            expected_version = json.loads((ROOT / '.codex-plugin/plugin.json').read_text())['version']
            self.assertEqual(build.validate(files)['version'], expected_version)
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
        with self.assertRaisesRegex(ValueError, 'Unbundled reference'):
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
        with self.assertRaisesRegex(ValueError, 'Private content'):
            build.validate(files)

    def test_private_directories_are_rejected_before_reading(self):
        for relative in ('.local', 'private-references', 'skills/example/private-rag'):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as directory:
                repo, plugin = self.fake_sources(directory)
                private = plugin / relative
                private.mkdir(parents=True)
                secret = private / 'secret.md'
                secret.write_text('private marker')
                self.assert_rejected_without_reading(repo, plugin, secret)

    def test_plugin_symlinks_are_rejected_before_reading(self):
        for is_directory in (False, True):
            with self.subTest(is_directory=is_directory), tempfile.TemporaryDirectory() as directory:
                repo, plugin = self.fake_sources(directory)
                secret = repo / 'secret.md'
                secret.write_text('private marker')
                if is_directory:
                    target = repo / 'secret-directory'
                    target.mkdir()
                    (target / 'secret.md').write_text('private marker')
                    link = plugin / 'skills' / 'linked-directory'
                else:
                    target = secret
                    link = plugin / 'skills' / 'linked.md'
                link.symlink_to(target, target_is_directory=is_directory)
                self.assert_rejected_without_reading(repo, plugin, link)

    def test_shared_resources_reject_symlinks_and_private_paths_before_reading(self):
        for relative in ('linked.md', 'linked-directory/secret.md', 'private-references/secret.md'):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as directory:
                repo, plugin = self.fake_sources(directory)
                source_root = repo / 'skills'
                private = source_root / 'private-references'
                private.mkdir()
                secret = private / 'secret.md'
                secret.write_text('private marker')
                if relative == 'linked.md':
                    (source_root / relative).symlink_to(secret)
                elif relative.startswith('linked-directory/'):
                    (source_root / 'linked-directory').symlink_to(private, target_is_directory=True)
                (plugin / 'shared-references.json').write_text(json.dumps([relative]))
                self.assert_rejected_without_reading(repo, plugin, source_root / relative)

    def test_shared_manifest_symlink_is_rejected_before_reading(self):
        with tempfile.TemporaryDirectory() as directory:
            repo, plugin = self.fake_sources(directory)
            manifest = plugin / 'shared-references.json'
            manifest.unlink()
            target = repo / 'private-list.json'
            target.write_text('[]')
            manifest.symlink_to(target)
            self.assert_rejected_without_reading(repo, plugin, manifest)

    def test_shared_manifest_cannot_escape_source_root(self):
        with tempfile.TemporaryDirectory() as directory:
            repo, plugin = self.fake_sources(directory)
            secret = repo / 'secret.md'
            secret.write_text('private marker')
            (plugin / 'shared-references.json').write_text('["../secret.md"]')
            self.assert_rejected_without_reading(repo, plugin, secret)

    def test_shared_resource_cannot_replace_plugin_authority(self):
        with tempfile.TemporaryDirectory() as directory:
            repo, plugin = self.fake_sources(directory)
            relative = 'example/references/shared.md'
            for root in (plugin / 'skills', repo / 'skills'):
                source = root / relative
                source.parent.mkdir(parents=True)
                source.write_text('public reference')
            (plugin / 'shared-references.json').write_text(json.dumps([relative]))
            with mock.patch.object(build, 'ROOT', plugin), mock.patch.object(build, 'REPO', repo):
                with self.assertRaisesRegex(ValueError, 'Duplicate authority'):
                    build.package_files()


if __name__ == '__main__':
    unittest.main()
