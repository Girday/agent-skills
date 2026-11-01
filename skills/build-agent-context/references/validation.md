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

## Repeated CLI experiments — November 1, 2026

Synthetic text tasks were executed by DeepSeek through OpenCode CLI 1.19.4, using the gateway's configured `DeepSeek-V4-Flash` identifier. Backend weights and decoding defaults were not independently identified. Codex designed the experiments, inspected the generated artifacts and tool events, and scored them; the scorer was not independent or fully blinded.

Each repetition used a fresh process, session, workspace, configuration, data and cache. Control runs lacked this skill; treatment runs loaded immutable skill snapshots. External plugins, MCP services, shell tools and unrelated source access were disabled. The same bundled OpenCode customization skill was discoverable in all arms, but no observed worker loaded it.

The development cases covered conflicting policy versions, exceptions, an embedded instruction attempt, unverified progress and updates preserving a manual note. Separate confirmation cases covered a recipient without source access, portable evidence, reported completion and pending proposals. Criteria and source truth were saved before each confirmation set; previously inspected cases were no longer treated as held out after another revision.

Several compact-layout variants reduced some output and token counts during development but did not produce a reliable time improvement on confirmation. One portable-package run reached the 180-second timeout. Those layout changes were reverted. Artifacts from a timed-out run do not establish successful session completion.

The retained corrections distinguish unverified completion from non-completion, pending proposals from rejection, and the creator's source access from the recipient's. Local records include exact prompts, synthetic fixtures, original and candidate skill snapshots, schedules, raw events, session exports, artifact checks, timing, reported token fields and semantic review notes. Failed and rejected trials remain in the archive; the archive is not bundled with the distributed skill.

The series included 56 scored runs across eight synthetic cases, plus two setup runs. On the last two previously untested cases, all four runs of the retained version preserved critical requirements, pending status, unverified reports and the one-text recipient contract. Original-skill and no-skill controls also preserved the main requirements; some made unsupported negative completion claims. Four final treatment runs are a limited regression check, not proof of general effectiveness or a measured speedup.

Reported usage includes repeated input across agent steps. Provider billing, auxiliary requests and hidden caching were not fully verified. Time comparisons are exploratory: two repeats per case, shared-server load, unpinned backend behavior and one intermediate run with reconstructed timing limit causal claims. These trials evaluate context preparation and artifact usability; they do not establish faster or more accurate downstream task completion, universal instruction adherence, or superiority over work without the skill.

## Not yet tested

- Broader model/provider coverage and independent scoring of the CLI experiments.
- Downstream task quality, time, and tokens using prepared context versus original materials.
- Real scans, formula OCR, password-protected archives, and collections of thousands of documents.
- Automatic loading of generated context in different agent environments.

Use the [scenarios and criteria](quality-checks.md) for further checks. Revise instructions based on observed failures; do not present structural validation as a quality guarantee.
