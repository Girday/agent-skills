#!/usr/bin/env python3
"""Compile a trusted LaTeX project until references stabilize; no shell escape."""

import argparse
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path


def engine_path(name):
    found = shutil.which(name)
    fallback = Path("/Library/TeX/texbin") / name
    return found or (str(fallback) if fallback.is_file() else None)


def snapshot(folder, stem):
    h = hashlib.sha256()
    for suffix in (".aux", ".toc", ".out", ".lof", ".lot"):
        p = folder / (stem + suffix)
        h.update(p.read_bytes() if p.exists() else b"")
    return h.digest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--main", default="main.tex")
    parser.add_argument("--engine", choices=("xelatex", "lualatex"), default="xelatex")
    parser.add_argument("--max-passes", type=int, default=5)
    args = parser.parse_args()
    root = args.project.expanduser().resolve()
    mainfile = (root / args.main).resolve()
    if mainfile.parent != root or not mainfile.is_file():
        parser.error("--main must name an existing TeX file directly in the project folder")
    if not 2 <= args.max_passes <= 8:
        parser.error("--max-passes must be between 2 and 8")
    engine = engine_path(args.engine)
    if not engine:
        parser.error(f"{args.engine} unavailable; sources preserved")
    out = root / "build"
    out.mkdir(exist_ok=True)
    old = None
    for run in range(1, args.max_passes + 1):
        cmd = [
            engine,
            "-no-shell-escape",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            "-output-directory=build",
            mainfile.name,
        ]
        result = subprocess.run(
            cmd, cwd=root, capture_output=True, text=True, errors="replace", timeout=180
        )
        (out / f"pass-{run}.txt").write_text(result.stdout + result.stderr)
        if result.returncode:
            print("\n".join((result.stdout + result.stderr).splitlines()[-35:]), file=sys.stderr)
            return result.returncode
        state = snapshot(out, mainfile.stem)
        log = (out / (mainfile.stem + ".log")).read_text(errors="replace")
        if (
            run >= 2
            and state == old
            and "Rerun to get" not in log
            and "Rerun to get cross-references" not in log
        ):
            if (
                "undefined references" in log
                or "undefined citations" in log
                or "Missing character:" in log
            ):
                print(
                    "Unresolved references/citations or missing glyphs; inspect build log.",
                    file=sys.stderr,
                )
                return 2
            print(f"Built {out / (mainfile.stem + '.pdf')} in {run} passes.")
            return 0
        old = state
    print("Auxiliary files did not stabilize; inspect build log.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except subprocess.TimeoutExpired:
        print("Compiler timeout; sources preserved.", file=sys.stderr)
        sys.exit(2)
