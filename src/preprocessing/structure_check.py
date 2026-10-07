"""structure_check.py — minimal starter for the Receipt Dataset project.

This base-level script checks the dataset: it reports how many files live
in each dataset/ folder and validates JSON annotation files against the
required fields of the draft label schema.

Usage (run from the repository root):

    python src/preprocessing/structure_check.py            # summary + validation
    python src/preprocessing/structure_check.py --list     # also list every file

Python built-ins only — nothing to install.
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATASET_DIR = REPO_ROOT / "dataset"

FOLDERS = (
    "images/raw",
    "images/processed",
    "annotations/raw",
    "annotations/validated",
    "annotations/schemas",
    "metadata",
)

# Required fields from the draft label schema (docs/label-schema.md).
REQUIRED_ANNOTATION_FIELDS = ("receipt_id", "merchant", "date", "total")


def scan(folder: Path = DATASET_DIR) -> dict[str, list[Path]]:
    """Return the files found in each dataset/ subfolder (top level only)."""
    out: dict[str, list[Path]] = {}
    for rel in FOLDERS:
        base = folder.joinpath(*rel.split("/"))
        out[rel] = sorted(p for p in base.glob("*") if p.is_file()) if base.is_dir() else []
    return out


def annotation_issues(path: Path) -> list[str]:
    """Return a list of problems with a JSON annotation file (empty = OK)."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"not valid JSON: {exc}"]
    if not isinstance(data, dict):
        return ["file is not a JSON object"]
    return [f"missing field: {name}" for name in REQUIRED_ANNOTATION_FIELDS if name not in data]


def report(found: dict[str, list[Path]], show_list: bool = False) -> str:
    lines = ["Receipt dataset - structure check", "=" * 42]
    total = 0
    for rel in FOLDERS:
        count = len(found[rel])
        total += count
        lines.append(f"  dataset/{rel:22s} : {count} file(s)")
    lines.append("-" * 42)
    lines.append(f"  TOTAL                       : {total} file(s)")

    checked = 0
    problems: list[str] = []
    for rel in ("annotations/raw", "annotations/validated"):
        for path in found[rel]:
            if path.suffix.lower() == ".json":
                checked += 1
                problems.extend(f"{rel}/{path.name}: {issue}" for issue in annotation_issues(path))

    lines.append(f"\nAnnotations checked : {checked}")
    if problems:
        lines.append("Problems found:")
        lines.extend(f"  - {p}" for p in problems)
    else:
        lines.append("No problems found. [OK]")

    if show_list:
        lines.append("\nFiles:")
        for rel in FOLDERS:
            lines.extend(f"  dataset/{rel}/{p.name}" for p in found[rel])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check the structure and draft annotations of the receipt dataset."
    )
    parser.add_argument("--list", action="store_true", help="also list every file found")
    args = parser.parse_args(argv)

    found = scan()
    print(report(found, show_list=args.list))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())