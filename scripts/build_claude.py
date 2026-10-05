"""Build Claude and Codex distributions from the canonical skill source."""

from pathlib import Path
import argparse
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


def build(repo: Path, destination: Path, package_format: str = "claude") -> Path:
    """Replace generated product-sense/ and product-sense.zip in destination."""
    if package_format not in {"claude", "codex"}:
        raise ValueError("Unknown package format")
    source = repo.resolve()
    output = destination.resolve()
    if output.is_relative_to(source) or source.is_relative_to(output / "product-sense"):
        raise ValueError("Build outside the skill source tree; output must not replace source")
    references = repo / "references"
    if references.is_symlink():
        raise ValueError(f"Reference directory must not be a symlink: {references}")
    if not references.is_dir():
        raise FileNotFoundError(references)
    entrypoint = read_regular(repo / "SKILL.md", repo)
    skill_prefix = "skills/product-sense/" if package_format == "claude" else ""
    payload = {f"{skill_prefix}SKILL.md": entrypoint}
    if package_format == "claude":
        payload[".claude-plugin/plugin.json"] = read_regular(repo / "packaging/claude/plugin.json", repo)
    else:
        payload["agents/openai.yaml"] = read_regular(repo / "agents/openai.yaml", repo)
        payload["assets/icon.svg"] = read_regular(repo / "assets/icon.svg", repo)
    if (repo / "LICENSE").exists() or (repo / "LICENSE").is_symlink():
        payload["LICENSE"] = read_regular(repo / "LICENSE", repo)
    for path in sorted(references.glob("*.md")):
        payload[f"{skill_prefix}references/{path.name}"] = read_regular(path, repo)
    # Refuse an archive whose entrypoint directs Claude to an omitted reference.
    for reference in re.findall(r"\]\((references/[^)]+)\)", entrypoint.decode("utf-8")):
        if f"{skill_prefix}{reference}" not in payload:
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
        help="Generated files go outside the installed skill tree (default: system temporary directory)",
    )
    arguments = parser.parse_args()
    output = arguments.output_dir or Path(tempfile.gettempdir()) / "product-sense-release" / arguments.format
    print(build(root, output, arguments.format))
