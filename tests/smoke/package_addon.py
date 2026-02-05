import argparse
import zipfile
from pathlib import Path

ADDON_DIR_NAME = "sorcar"

EXCLUDED_DIRS = {
    ".git",
    ".github",
    "__pycache__",
    ".idea",
    ".vscode",
    "venv",
    "avaliacao",
    "tests",
}
EXCLUDED_SUFFIXES = {".pyc", ".zip"}
EXCLUDED_FILES = {
    "avaliacao_total_addon.md",
    "avaliacao_total_addon_relatorio.md",
}

def should_include(rel_path: Path) -> bool:
    if any(part in EXCLUDED_DIRS for part in rel_path.parts):
        return False
    if rel_path.name in EXCLUDED_FILES:
        return False
    if rel_path.suffix in EXCLUDED_SUFFIXES:
        return False
    return True

def main() -> None:
    parser = argparse.ArgumentParser(description="Package addon as a Blender-installable zip.")
    parser.add_argument("--output", default="sorcar-smoke.zip", help="Output zip filepath.")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[2]
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    files = []
    for path in sorted(root.rglob("*")):
        if path.is_dir():
            continue
        if path.resolve() == output:
            continue
        rel_path = path.relative_to(root)
        if not should_include(rel_path):
            continue
        files.append((path, rel_path))

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path, rel_path in files:
            archive.write(path, (Path(ADDON_DIR_NAME) / rel_path).as_posix())

    print(output.as_posix())

if __name__ == "__main__":
    main()
