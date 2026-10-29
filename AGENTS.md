# Repository guidance

This repository distributes reusable agent skills. Preserve the boundary between a skill's domain requirements, implementation choices, and user instructions.

- Add skills under `skills/`; keep catalog entries in both READMEs current.
- Keep machine-specific configuration and private data out of published files.
- Do not copy bundled vendor skills or third-party materials into the repository without checking provenance and permissions.
- Run `python scripts/validate.py`, the unittest suite, `ruff check .`, and `ruff format --check .` before a requested push.
- For LaTeX changes, compile a representative document and inspect the rendered pages. State which engines and special modes were tested.
- Do not claim that automated checks certify GOST compliance. Preserve `REVIEW` and `NOT_CHECKED` distinctions.
- Publish, push, or release only when authorized by the user. Do not change unrelated installed skills as a side effect of repository edits.
- For commits made with Codex's assistance, keep the human contributor as the primary author and append `Co-authored-by: Codex <noreply@openai.com>` after a blank line in the commit message. Apply this to future commits; do not rewrite published history solely to add attribution.
