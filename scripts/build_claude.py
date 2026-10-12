"""Build Claude and Codex distributions from the canonical plugin folder."""

from pathlib import Path
import argparse
import re
import shutil
import tempfile
import zipfile

PLUGIN = Path("plugins/product-sense")
SKILL = PLUGIN / "skills/product-sense"
SYSTEM_FILES = {".DS_Store", "Thumbs.db", "desktop.ini"}


def reject_symlinks(path: Path, root: Path) -> None:
    component = root
    for part in ("", *path.relative_to(root).parts):
        component = component / part
        if component.is_symlink():
            raise ValueError(f"Package source must not contain a symlink: {component}")


def read_regular(path: Path, root: Path) -> bytes:
    reject_symlinks(path, root)
    if not path.is_file():
        raise FileNotFoundError(path)
    return path.read_bytes()


def collect(folder: Path, repo: Path) -> dict:
    """Every regular file under folder, keyed by its path relative to folder."""
    reject_symlinks(folder, repo)
    if not folder.is_dir():
        raise FileNotFoundError(folder)
    files = {}
    for path in sorted(folder.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Package source must not contain a symlink: {path}")
        if path.is_file() and path.name not in SYSTEM_FILES and "__MACOSX" not in path.parts:
            files[path.relative_to(folder).as_posix()] = read_regular(path, repo)
    return files


def build(repo: Path, destination: Path, package_format: str = "claude") -> Path:
    """Replace generated product-sense/ and product-sense.zip in destination."""
    if package_format not in {"claude", "codex"}:
        raise ValueError("Unknown package format")
    source = repo.resolve()
    output = destination.resolve()
    if output.is_relative_to(source) or source.is_relative_to(output / "product-sense"):
        raise ValueError("Build outside the skill source tree; output must not replace source")
    plugin, skill = repo / PLUGIN, repo / SKILL
    entrypoint = read_regular(skill / "SKILL.md", repo)
    read_regular(plugin / ".claude-plugin/plugin.json", repo)
    read_regular(plugin / "LICENSE", repo)
    if package_format == "claude":
        payload = collect(plugin, repo)
        skill_prefix = f"{SKILL.relative_to(PLUGIN).as_posix()}/"
    else:
        payload = collect(skill, repo)
        payload["LICENSE"] = read_regular(plugin / "LICENSE", repo)
        read_regular(skill / "agents/openai.yaml", repo)
        skill_prefix = ""
    # Refuse an archive whose entrypoint directs Claude to an omitted reference.
    for reference in re.findall(r"\]\((references/[^)]+)\)", entrypoint.decode("utf-8")):
        if f"{skill_prefix}{reference}" not in payload:
            raise FileNotFoundError(skill / reference)

    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".build-", dir=destination) as temporary:
        staging = Path(temporary)
        folder = staging / "product-sense"
        archive = staging / "product-sense.zip"
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_STORED) as bundle:
            for name, content in sorted(payload.items()):
                target = folder / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
                archive_name = f"product-sense/{name}" if package_format == "codex" else name
                member = zipfile.ZipInfo(archive_name, date_time=(1980, 1, 1, 0, 0, 0))
                member.create_system = 3
                member.external_attr = 0o100644 << 16
                bundle.writestr(member, content)
        generated = destination / "product-sense"
        if generated.is_symlink():
            raise ValueError(f"Generated folder must not be a symlink: {generated}")
        if generated.exists():
            shutil.rmtree(generated)
        folder.replace(generated)
        archive.replace(destination / "product-sense.zip")
    return destination / "product-sense.zip"


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("claude", "codex"), default="claude")
    parser.add_argument(
        "--output-dir", type=Path,
        default=None,
        help="Generated files go outside the source tree (default: system temporary directory)",
    )
    arguments = parser.parse_args()
    output = arguments.output_dir or Path(tempfile.gettempdir()) / "product-sense-release" / arguments.format
    print(build(root, output, arguments.format))
