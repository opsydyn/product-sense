"""Build a skills-only Claude plugin from the canonical repository source."""

from pathlib import Path
import re
import shutil
import tempfile
import zipfile


def read_regular(path: Path, root: Path) -> bytes:
    component = root
    for part in ("", *path.relative_to(root).parts):
        component = component / part
        if component.is_symlink():
            raise ValueError(f"Package source must not contain a symlink: {component}")
    if not path.is_file():
        raise FileNotFoundError(path)
    return path.read_bytes()


def build(repo: Path, destination: Path) -> Path:
    """Replace generated product-sense/ and product-sense.zip in destination."""
    references = repo / "references"
    if references.is_symlink():
        raise ValueError(f"Reference directory must not be a symlink: {references}")
    if not references.is_dir():
        raise FileNotFoundError(references)
    entrypoint = read_regular(repo / "SKILL.md", repo)
    payload = {
        ".claude-plugin/plugin.json": read_regular(repo / "packaging/claude/plugin.json", repo),
        "skills/product-sense/SKILL.md": entrypoint,
    }
    for path in sorted(references.glob("*.md")):
        payload[f"skills/product-sense/references/{path.name}"] = read_regular(path, repo)
    # Refuse an archive whose entrypoint directs Claude to an omitted reference.
    for reference in re.findall(r"\]\((references/[^)]+)\)", entrypoint.decode("utf-8")):
        if f"skills/product-sense/{reference}" not in payload:
            raise FileNotFoundError(repo / reference)

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
                member = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
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
    print(build(root, root / "dist/claude"))
