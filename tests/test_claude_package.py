import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import zipfile


REPO = Path(__file__).resolve().parents[1]
PLUGIN = Path("plugins/product-sense")
SKILL = PLUGIN / "skills/product-sense"


class ClaudePackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "source"
        shutil.copytree(REPO / PLUGIN, self.repo / PLUGIN, ignore=shutil.ignore_patterns(".DS_Store"))
        (self.repo / "private.txt").write_text("excluded")
        (self.repo / "qualification").mkdir()
        (self.repo / "qualification/report.md").write_text("excluded")
        self.plugin = self.repo / PLUGIN
        self.skill = self.repo / SKILL
        self.destination = self.root / "distribution"

    def build(self, package_format="claude"):
        script = REPO / "scripts/build_claude.py"
        spec = importlib.util.spec_from_file_location("build_claude", script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.build(self.repo, self.destination, package_format=package_format)

    def plugin_files(self):
        return {p.relative_to(self.plugin).as_posix(): p.read_bytes()
                for p in self.plugin.rglob("*") if p.is_file()}

    def test_archive_is_exactly_the_plugin_folder(self):
        archive = self.build()
        expected = self.plugin_files()
        self.assertIn(".claude-plugin/plugin.json", expected)
        self.assertIn("skills/product-sense/SKILL.md", expected)
        self.assertIn("README.md", expected)
        self.assertIn("LICENSE", expected)
        with zipfile.ZipFile(archive) as bundle:
            self.assertEqual(set(bundle.namelist()), set(expected))
            for name, content in expected.items():
                self.assertEqual(bundle.read(name), content)
                self.assertEqual((self.destination / "product-sense" / name).read_bytes(), content)

    def test_excludes_system_files(self):
        (self.skill / ".DS_Store").write_bytes(b"junk")
        with zipfile.ZipFile(self.build()) as bundle:
            self.assertFalse(any(n.endswith(".DS_Store") for n in bundle.namelist()))

    def test_rebuild_removes_stale_files_and_has_identical_archive_bytes(self):
        original = self.build().read_bytes()
        stale = self.destination / "product-sense/skills/product-sense/stale.txt"
        stale.write_text("must not survive")
        for path in self.repo.rglob("*.md"):
            path.touch()
        self.assertEqual(self.build().read_bytes(), original)
        self.assertFalse(stale.exists())

    def test_rejects_symlinked_reference_before_changing_existing_output(self):
        original = self.build().read_bytes()
        (self.skill / "references/extra.md").symlink_to(self.repo / "private.txt")
        with self.assertRaises(ValueError):
            self.build()
        self.assertEqual(next(self.destination.glob("*.zip")).read_bytes(), original)

    def test_rejects_symlinked_reference_directory(self):
        shutil.move(self.skill / "references", self.root / "outside-references")
        (self.skill / "references").symlink_to(self.root / "outside-references")
        with self.assertRaises(ValueError):
            self.build()

    def test_missing_entrypoint_fails_without_creating_a_package(self):
        (self.skill / "SKILL.md").unlink()
        with self.assertRaises(FileNotFoundError):
            self.build()
        self.assertFalse(self.destination.exists())

    def test_missing_linked_reference_fails_without_creating_a_package(self):
        (self.skill / "references/discovery.md").unlink()
        with self.assertRaises(FileNotFoundError):
            self.build()
        self.assertFalse(self.destination.exists())

    def test_missing_licence_fails_without_creating_a_package(self):
        (self.plugin / "LICENSE").unlink()
        for package_format in ("claude", "codex"):
            with self.subTest(package_format=package_format):
                with self.assertRaises(FileNotFoundError):
                    self.build(package_format)
                self.assertFalse(self.destination.exists())

    def test_rejects_symlinked_parents_before_changing_output(self):
        original = self.build().read_bytes()
        for name in ["plugins", "plugins/product-sense", "plugins/product-sense/.claude-plugin"]:
            with self.subTest(parent=name):
                parent = self.repo / name
                outside = self.root / f"outside-{parent.name}"
                shutil.move(parent, outside)
                parent.symlink_to(outside)
                try:
                    with self.assertRaises(ValueError):
                        self.build()
                    self.assertEqual(next(self.destination.glob("*.zip")).read_bytes(), original)
                finally:
                    parent.unlink()
                    shutil.move(outside, parent)

    def test_default_cli_build_keeps_generated_skills_outside_source(self):
        scripts = self.repo / "scripts"
        scripts.mkdir()
        shutil.copy2(REPO / "scripts/build_claude.py", scripts)
        temporary_outputs = self.root / "temporary-outputs"
        temporary_outputs.mkdir()
        result = subprocess.run(
            ["python3", str(scripts / "build_claude.py")],
            env={**os.environ, "TMPDIR": str(temporary_outputs)},
            capture_output=True, text=True, check=True,
        )
        archive = Path(result.stdout.strip()).resolve()
        self.assertFalse(archive.is_relative_to(self.repo.resolve()))
        self.assertTrue(archive.is_file())
        self.assertEqual(list(self.repo.rglob("SKILL.md")), [self.skill / "SKILL.md"])

    def test_rejects_output_inside_source_before_creating_files(self):
        self.destination = self.repo / "dist/claude"
        with self.assertRaises(ValueError):
            self.build()
        self.assertFalse(self.destination.exists())

    def test_rejects_output_that_would_replace_source(self):
        source = self.root / "product-sense"
        self.repo.rename(source)
        self.repo = source
        self.destination = self.root
        with self.assertRaises(ValueError):
            self.build()
        self.assertTrue((source / SKILL / "SKILL.md").is_file())

    def test_codex_archive_is_the_skill_folder_plus_licence(self):
        archive = self.build("codex")
        expected = {p.relative_to(self.skill).as_posix(): p.read_bytes()
                    for p in self.skill.rglob("*") if p.is_file()}
        expected["LICENSE"] = (self.plugin / "LICENSE").read_bytes()
        self.assertIn("agents/openai.yaml", expected)
        self.assertIn("assets/icon.svg", expected)
        with zipfile.ZipFile(archive) as bundle:
            self.assertEqual(set(bundle.namelist()), {f"product-sense/{n}" for n in expected})
            for name, content in expected.items():
                self.assertEqual(bundle.read(f"product-sense/{name}"), content)
        original = archive.read_bytes()
        self.assertEqual(self.build("codex").read_bytes(), original)

    def test_codex_missing_metadata_fails_without_creating_output(self):
        (self.skill / "agents/openai.yaml").unlink()
        with self.assertRaises(FileNotFoundError):
            self.build("codex")
        self.assertFalse(self.destination.exists())

    def test_packages_exclude_files_outside_the_plugin_folder(self):
        for package_format in ("claude", "codex"):
            with self.subTest(package_format=package_format):
                with zipfile.ZipFile(self.build(package_format)) as bundle:
                    names = bundle.namelist()
                self.assertFalse(any("private.txt" in n or "qualification" in n for n in names))


if __name__ == "__main__":
    unittest.main()
