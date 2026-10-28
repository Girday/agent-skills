#!/usr/bin/env python3
"""Install a skill from this checkout without overwriting existing data."""

import argparse
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def install(name: str, destination: Path) -> Path:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError("Expected a lowercase hyphenated skill name")
    source = ROOT / "skills" / name
    if not (source / "SKILL.md").is_file():
        raise ValueError(f"Skill not found: {name}")
    if source.is_symlink() or not source.resolve().is_relative_to(ROOT / "skills"):
        raise ValueError("Skill must be inside this checkout")
    destination = destination.expanduser().resolve()
    target = destination / name
    # copytree also refuses a target created concurrently after this check.
    if target.exists() or target.is_symlink():
        raise FileExistsError(f"Refusing to overwrite: {target}")
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill")
    default_home = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
    parser.add_argument("--dest", type=Path, default=default_home / "skills")
    args = parser.parse_args()
    try:
        target = install(args.skill, args.dest)
    except (ValueError, OSError) as error:
        parser.exit(1, f"{error}\n")
    print(f"Installed {target}")
    print("If the skill does not appear, restart Codex.")


if __name__ == "__main__":
    main()
