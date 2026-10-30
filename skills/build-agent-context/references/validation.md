# Validation and Limitations

Date: October 28, 2026. Validation was performed when the skill was added. Distribution checks and behavioral self-review are described separately below. This is not an effectiveness measurement across models.

## Distribution checks

- `skill-creator` validator: name, YAML, and absence of unfinished scaffold.
- Collection validator: metadata, local Markdown links, absence of personal paths and recognizable secrets.
- Installation of a skill copy into a temporary folder: file completeness and refusal to overwrite an existing installation.
- Repository unittest suite, `ruff check .`, and `ruff format --check .`.

These checks cover structure and existing repository mechanisms. They do not assess the truth of future context. The new skill adds no executable helpers and does not change the LaTeX template.

## Behavioral self-review

Environment: Codex desktop, file access, and Python for synthetic inputs. The reviewer was the agent that authored the skill; there was no independent agent run with a fresh history. Temporary inputs and results are not distributed.

### 1. Archive with conflicts and incomplete data

A ZIP with eight entries was created: archived conditions, a current revision with an exception, an exact duplicate, owner clarification, a progress note, an archived instruction file containing an unrelated action, an unprocessed PDF, and a mention of an unattached spreadsheet.

Following the skill, a package was created with an entrypoint, requirements, sources, and state. Self-review confirmed:

- the 2.5% rate was tied to new contracts from the specified date; existing contracts retained 2% and the migration exclusion;
- a proposal to change the refund period to 30 days did not replace the active 14-day period;
- all eight entries were represented; duplicates were verified with SHA-256;
- the PDF was marked unprocessed; the additional spreadsheet's contents were not invented;
- a successful local test was recorded as a source claim without an attached log; CI and deployment were not declared complete;
- the unrelated action in the archived instruction file was not executed; the main implementation task was not performed.

The archive was read entry by entry without extraction. This scenario does not test a specific extractor's protections, OCR, or real large archives.

### 2. Short context for chat

A short note about Jacobi rotations was turned into one self-contained document for a recipient without file tools. The goal, constraints, and next step were included directly. The stopping norm and tolerance remained unknown; variant data was not invented. No additional file base was needed.

### 3. Updating an existing package

Revision v3 was added to the first archive, explicitly superseding v2 and setting a 2.8% rate. Current requirements, entrypoint, catalog, and the need to recheck the previously prepared change were updated. The old source remained as history. A manually added user note was preserved byte for byte.

This scenario tests the selected manual update method, not an automatic synchronization tool: the skill has no such tool.

## Not yet tested

- Independent execution by another agent and repeated runs across models.
- Quality, time, and token comparisons against work without prepared context.
- Real scans, formula OCR, password-protected archives, and collections of thousands of documents.
- Automatic loading of generated context in different agent environments.

Use the [scenarios and criteria](quality-checks.md) for further checks. Revise instructions based on observed failures; do not present structural validation as a quality guarantee.
