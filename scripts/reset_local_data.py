from __future__ import annotations

import argparse
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "backend" / "data"
RUNTIME_SUFFIXES = (".json", ".json.tmp")


def reset_local_data(*, repo_root: Path = REPO_ROOT, yes: bool = False) -> dict[str, list[str] | bool]:
    """Delete project-local runtime JSON data and preserve source files."""

    data_dir = (repo_root / "backend" / "data").resolve()
    data_dir.mkdir(parents=True, exist_ok=True)

    candidates = sorted(
        path
        for path in data_dir.iterdir()
        if path.is_file() and _is_runtime_json_file(path, data_dir)
    )
    result = {
        "dry_run": not yes,
        "deleted": [],
        "would_delete": [str(path) for path in candidates],
        "preserved": [str(data_dir / ".gitkeep")],
    }

    if not yes:
        return result

    for path in candidates:
        path.unlink()
        result["deleted"].append(str(path))

    gitkeep = data_dir / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.write_text("\n", encoding="utf-8")

    return result


def _is_runtime_json_file(path: Path, data_dir: Path) -> bool:
    resolved = path.resolve()
    if resolved.parent != data_dir:
        return False
    return any(resolved.name.endswith(suffix) for suffix in RUNTIME_SUFFIXES)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Safely reset Sentigraph local runtime JSON data under backend/data."
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Actually delete runtime JSON files. Without this flag the script prints a dry run.",
    )
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    result = reset_local_data(yes=args.yes)
    mode = "deleted" if args.yes else "would delete"
    files = result["deleted"] if args.yes else result["would_delete"]
    print(f"Sentigraph local data reset ({'apply' if args.yes else 'dry-run'}).")
    if files:
        for path in files:
            print(f"- {mode}: {path}")
    else:
        print("- no runtime JSON files found")
    print(f"- preserved: {DATA_DIR / '.gitkeep'}")
    if not args.yes:
        print("Run again with --yes to delete these files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
