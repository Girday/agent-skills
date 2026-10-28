#!/usr/bin/env python3
"""Copy the editable demonstration project, refusing all overwrites."""

import argparse
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1] / "assets" / "template"
    dest = args.destination.expanduser().resolve()
    files = sorted(p for p in source.rglob("*") if p.is_file())
    conflicts = [
        str(dest / p.relative_to(source)) for p in files if (dest / p.relative_to(source)).exists()
    ]
    if conflicts:
        parser.error("Refusing to overwrite: " + ", ".join(conflicts))
    dest.mkdir(parents=True, exist_ok=True)
    for p in files:
        out = dest / p.relative_to(source)
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, out)
    print(f"Created {dest}; edit metadata.tex, title.tex and main.tex before submission.")


if __name__ == "__main__":
    main()
