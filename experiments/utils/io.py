"""File I/O helpers: load prompts and JSON under project root."""
import json
from pathlib import Path


def load_prompt(root: Path, *path_parts: str) -> str:
    """Load a text file under root (e.g. prompts/foo.txt)."""
    path = root.joinpath(*path_parts)
    with open(path, encoding="utf-8") as f:
        return f.read()


def load_json(root: Path, *path_parts: str):
    """Load JSON under root (e.g. tests/problems.json)."""
    path = root.joinpath(*path_parts)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(root: Path, data, *path_parts: str) -> None:
    """Write JSON under root."""
    path = root.joinpath(*path_parts)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
