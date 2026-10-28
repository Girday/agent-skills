#!/usr/bin/env python3
"""Validate portable skill metadata, local links and publishable source files."""

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".venv", "__pycache__", ".ruff_cache", "build"}
TEXT_EXTENSIONS = {".md", ".py", ".toml", ".yaml", ".yml", ".tex", ".sty", ".txt"}
PRIVATE_PATH = re.compile(r"/(?:Users|home)/[^/\s]+/|/private/(?:tmp|var)/")
CREDENTIAL = re.compile(
    r"\bgh[pousr]_[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"
)


def validate(root: Path) -> list[str]:
    errors = []
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    if not skills:
        errors.append("No skills found")
    for entry in skills:
        text = entry.read_text(encoding="utf-8")
        match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.S)
        if not match:
            errors.append(f"{entry.relative_to(root)}: missing YAML frontmatter")
            continue
        try:
            data = yaml.safe_load(match.group(1))
        except yaml.YAMLError as error:
            errors.append(f"{entry.relative_to(root)}: invalid YAML: {error}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{entry.relative_to(root)}: frontmatter must be a mapping")
            continue
        name = data.get("name", "")
        if (
            not isinstance(name, str)
            or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)
            or len(name) > 64
        ):
            errors.append(f"{entry.relative_to(root)}: invalid skill name")
        if name != entry.parent.name:
            errors.append(f"{entry.relative_to(root)}: name differs from folder")
        if not isinstance(data.get("description"), str) or not data["description"].strip():
            errors.append(f"{entry.relative_to(root)}: missing description")
        if "[TODO:" in text:
            errors.append(f"{entry.relative_to(root)}: unfinished scaffold")
        interface_file = entry.parent / "agents" / "openai.yaml"
        if interface_file.exists():
            try:
                interface = yaml.safe_load(interface_file.read_text(encoding="utf-8"))
                prompt = interface.get("interface", {}).get("default_prompt", "")
                if prompt and "$" + name not in prompt:
                    errors.append(f"{interface_file.relative_to(root)}: prompt omits skill name")
            except (yaml.YAMLError, AttributeError, TypeError) as error:
                errors.append(f"{interface_file.relative_to(root)}: invalid metadata: {error}")
    for file in root.rglob("*"):
        if any(part in SKIP_DIRS for part in file.relative_to(root).parts):
            continue
        if file.is_symlink():
            errors.append(f"{file.relative_to(root)}: symlinks are not distributed")
            continue
        if not file.is_file() or file.suffix not in TEXT_EXTENSIONS:
            continue
        text = file.read_text(encoding="utf-8")
        if PRIVATE_PATH.search(text):
            errors.append(f"{file.relative_to(root)}: personal machine path")
        if CREDENTIAL.search(text):
            errors.append(f"{file.relative_to(root)}: possible credential/private key")
        if file.suffix == ".md":
            for link in re.findall(r"\]\(([^)\s]+)\)", text):
                url = urlsplit(link)
                if url.scheme or url.netloc or not url.path:
                    continue
                target = (file.parent / unquote(url.path)).resolve()
                if not target.is_relative_to(root.resolve()) or not target.exists():
                    errors.append(f"{file.relative_to(root)}: broken/outside link: {link}")
    return errors


def main():
    errors = validate(ROOT)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Skill metadata, local links and publishable source checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
