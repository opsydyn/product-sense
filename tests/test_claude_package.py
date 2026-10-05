import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import zipfile


REPO = Path(__file__).resolve().parents[1]


class ClaudePackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "source"
        self.repo.mkdir()
        shutil.copy2(REPO / "SKILL.md", self.repo)
        shutil.copytree(REPO / "references", self.repo / "references")
        shutil.copytree(REPO / "agents", self.repo / "agents")
        shutil.copytree(REPO / "assets", self.repo / "assets")
        (self.repo / "packaging/claude").mkdir(parents=True)
        (self.repo / "packaging/claude/plugin.json").write_text(
            json.dumps({"name": "product-sense", "version": "0.1.0"})
        )
        (self.repo / "private.txt").write_text("excluded")
        self.destination = self.root / "distribution"

    def build(self, package_format="claude"):
        script = REPO / "scripts/build_claude.py"
        self.assertTrue(script.is_file(), "Claude package builder is not implemented")
        spec = importlib.util.spec_from_file_location("build_claude", script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if package_format == "claude":
            return module.build(self.repo, self.destination)
        return module.build(self.repo, self.destination, package_format=package_format)

    def test_archive_contains_only_exact_canonical_payload(self):
        archive = self.build()
        expected = {
            ".claude-plugin/plugin.json": (self.repo / "packaging/claude/plugin.json").read_bytes(),
            "skills/product-sense/SKILL.md": (self.repo / "SKILL.md").read_bytes(),
        }
        for path in (self.repo / "references").glob("*.md"):
            expected[f"skills/product-sense/references/{path.name}"] = path.read_bytes()
        with zipfile.ZipFile(archive) as bundle:
            self.assertEqual(set(bundle.namelist()), set(expected))
            for name, content in expected.items():
                self.assertEqual(bundle.read(name), content)
                self.assertEqual((self.destination / "product-sense" / name).read_bytes(), content)

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
        linked = self.repo / "references/extra.md"
        linked.symlink_to(self.repo / "private.txt")
        with self.assertRaises(ValueError):
            self.build()
        self.assertEqual(next(self.destination.glob("*.zip")).read_bytes(), original)

    def test_rejects_symlinked_reference_directory(self):
        shutil.move(self.repo / "references", self.root / "outside-references")
        (self.repo / "references").symlink_to(self.root / "outside-references")
        with self.assertRaises(ValueError):
            self.build()

    def test_missing_entrypoint_fails_without_creating_a_package(self):
        (self.repo / "SKILL.md").unlink()
        with self.assertRaises(FileNotFoundError):
            self.build()
        self.assertFalse(self.destination.exists())

    def test_missing_linked_reference_fails_without_creating_a_package(self):
        (self.repo / "references/discovery.md").unlink()
        with self.assertRaises(FileNotFoundError):
            self.build()
        self.assertFalse(self.destination.exists())

    def test_rejects_symlinked_manifest_parents_before_changing_output(self):
        original = self.build().read_bytes()
        for name in ["packaging", "packaging/claude"]:
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
        self.assertEqual(list(self.repo.rglob("SKILL.md")), [self.repo / "SKILL.md"])

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
        self.assertTrue((source / "SKILL.md").is_file())

    def test_codex_archive_contains_exact_installable_skill_and_metadata(self):
        archive = self.build("codex")
        names = ["SKILL.md", "agents/openai.yaml", "assets/icon.svg"]
        names += [str(p.relative_to(self.repo)) for p in (self.repo / "references").glob("*.md")]
        with zipfile.ZipFile(archive) as bundle:
            self.assertEqual(set(bundle.namelist()), {f"product-sense/{n}" for n in names})
            for name in names:
                self.assertEqual(bundle.read(f"product-sense/{name}"), (self.repo / name).read_bytes())
        original = archive.read_bytes()
        self.assertEqual(self.build("codex").read_bytes(), original)

    def test_codex_missing_metadata_fails_without_creating_output(self):
        (self.repo / "agents/openai.yaml").unlink()
        with self.assertRaises(FileNotFoundError):
            self.build("codex")
        self.assertFalse(self.destination.exists())

    def test_includes_exact_owner_supplied_licence_in_both_formats(self):
        licence = b"Owner-selected licence text for this fixture.\n"
        (self.repo / "LICENSE").write_bytes(licence)
        for package_format in ("claude", "codex"):
            with self.subTest(package_format=package_format):
                archive = self.build(package_format)
                name = "LICENSE" if package_format == "claude" else "product-sense/LICENSE"
                with zipfile.ZipFile(archive) as bundle:
                    self.assertEqual(bundle.read(name), licence)


if __name__ == "__main__":
    unittest.main()
