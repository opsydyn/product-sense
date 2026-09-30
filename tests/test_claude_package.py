import importlib.util
import json
from pathlib import Path
import shutil
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
        (self.repo / "packaging/claude").mkdir(parents=True)
        (self.repo / "packaging/claude/plugin.json").write_text(
            json.dumps({"name": "product-sense", "version": "0.1.0"})
        )
        (self.repo / "private.txt").write_text("excluded")
        self.destination = self.root / "distribution"

    def build(self):
        script = REPO / "scripts/build_claude.py"
        self.assertTrue(script.is_file(), "Claude package builder is not implemented")
        spec = importlib.util.spec_from_file_location("build_claude", script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.build(self.repo, self.destination)

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


if __name__ == "__main__":
    unittest.main()
