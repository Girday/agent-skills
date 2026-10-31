# Repository guidance

This repository distributes reusable agent skills. Preserve the boundary between a skill's domain requirements, implementation choices, and user instructions.

- Maintain skill instructions, agent-facing references, and UI metadata in English. Skills must direct agents to respond in the user's language unless requested otherwise and use the artifact language required by the task. Preserve mandatory original wording and language-specific template content; transcribe recorded speech in its original language unless translation is requested. Keep README translations localized.
- Add skills under `skills/`; keep catalog entries in `README.md` and the translations under `readme/` current.
- Keep machine-specific configuration and private data out of published files.
- Do not copy bundled vendor skills or third-party materials into the repository without checking provenance and permissions.
- Run `python scripts/validate.py`, the unittest suite, `ruff check .`, and `ruff format --check .` before a requested push.
- For LaTeX changes, compile a representative document and inspect the rendered pages. State which engines and special modes were tested.
- Do not claim that automated checks certify GOST compliance. Preserve `REVIEW` and `NOT_CHECKED` distinctions.
- Publish, push, or release only when authorized by the user. Do not change unrelated installed skills as a side effect of repository edits.
- For commits made with Codex's assistance, keep the human contributor as the primary author and append `Co-authored-by: Codex <noreply@openai.com>` after a blank line in the commit message. Apply this to future commits; do not rewrite published history solely to add attribution.

## Versioning and releases

- Version the repository as a whole using `vMAJOR.MINOR.PATCH` Git tags and corresponding GitHub Releases. Individual skills do not have separate release tags.
- Continue the existing release series. Inspect current tags and GitHub Releases before choosing a version; do not assume that a version recorded in prior context is still the latest.
- During `0.x` development, increment MINOR for new skills, substantial capability or instruction changes, and breaking changes; increment PATCH for compatible fixes, small clarifications, and documentation or translation updates. Describe breaking changes explicitly. Move to `1.0.0` only when the user requests a stable release milestone.
- Group related changes into meaningful releases; do not create a release automatically for every commit or push. Authorization to commit or push alone does not authorize creating or publishing a release.
- After completing a meaningful set of changes, proactively assess whether a release is warranted. If so, suggest a specific next version and briefly explain the bump in the user's language, based on all changes since the latest release. Make the recommendation yourself rather than asking the user to classify changes as MAJOR, MINOR, or PATCH. Avoid repeating an unchanged recommendation in follow-up replies; create and publish the tag and release only after the user authorizes it.
- Before releasing, review all changes since the preceding release, run the repository checks listed above against the intended release commit, and verify that the tag points to that commit. Report any untested engines, modes, or behavior relevant to the release.
- Use English release titles in the form `vX.Y.Z — Short description` and concise English release notes describing user-visible changes across the full release range. Mention compatibility changes and material validation limits; do not present unverified behavior as tested.
- Preserve published tags and releases. Do not move or delete an existing tag, or rewrite a published release, unless the user explicitly requests that action.
