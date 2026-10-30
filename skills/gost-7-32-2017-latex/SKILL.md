---
name: gost-7-32-2017-latex
description: Prepare, edit, and review research reports in LaTeX using GOST 7.32-2017; adapt its formatting to coursework and other documents with institutional requirements. Use when this standard, a LaTeX template, or report compliance review is requested, including title pages, structure, equations, tables, references, and appendices.
---

# GOST 7.32-2017 in LaTeX

Create an editable project and a reviewed PDF. Respond in the user's language unless they request otherwise. Use the language required by the task for generated artifacts. Preserve exact wording where required by standards, templates, or source material. The bundled template is Russian; adapt its language only as the task requires, preserving applicable mandatory wording. The standard covers research reports; label use for coursework as an adaptation. Do not interpret every request for “GOST” formatting as a request for this particular standard.

## Before starting

Read [sources.md](references/sources.md) and [requirements.md](references/requirements.md). This is an analytical map of all sections and appendices, not an official edition. Distinguish requirements, permitted alternatives, recommendations, template choices, and organizational actions.

Use available materials to identify the document type, interim/final report status, institutional requirements, contributors, administrative details, number of volumes, language, content, and sources. Ask only about missing information that affects the next step; continue other work. Do not invent UDC codes, registration numbers, job titles, signatures, seals, results, or bibliography. Visible `[УКАЗАТЬ …]` placeholders are acceptable in drafts; list unfilled fields before delivery. Do not imitate a signature or seal.

Choose a profile:

1. **Research report under the standard** — all applicable rules and explicitly selected permitted alternatives.
2. **Coursework adaptation** — formatting follows the user's/institution's assignment; record differences from GOST in a separate note.

If the user requires a deviation, follow the request and name the specific difference. Do not attribute a university rule to GOST. Defaults: A4, single-sided printing, 14 bp, Times New Roman when available, one-and-a-half line spacing, continuous figure/table/equation numbering. **14 bp is a template choice; GOST requires at least 12 pt. Times New Roman is recommended.** Math fonts, heading spacing, and footer position are also template choices.

## Implementation

Read [latex-workflow.md](references/latex-workflow.md): commands, LaTeX mapping to requirements, A3, multiple volumes, long tables, and bibliography. Do not treat an existing `G7-32` class as proof of compliance without checking its behavior.

Place a new document in a separate folder with `main.tex`. In Codex desktop, when `create_latex_project` is available, first create a project with that tool using `assets/template/main.tex`, then add neighboring template resources and open the folder through `open_in_codex`. In other environments:

```bash
python3 /absolute/path/to/skill/scripts/init_project.py /absolute/path/to/new-report
```

The initializer does not overwrite files. Inspect existing documents first: class, preamble, structure, and local requirements. Edit in place, preserving data and working commands. The template contains demonstration data; adapt all administrative fields, abstract statistics, structure, and objects to the actual content.

Use XeLaTeX or LuaLaTeX. If Times New Roman is unavailable, choose an explicit Cyrillic-capable substitute and report it during review; do not silently substitute fonts. Do not download proprietary fonts. Do not shrink all text or margins to fit material; see map clauses 6.1.1 and 6.6.7 for exceptions.

## Verification and delivery

```bash
python3 /absolute/path/to/skill/scripts/build.py /absolute/path/to/report
python3 /absolute/path/to/skill/scripts/audit.py /absolute/path/to/report --output /absolute/path/to/report/build/audit.json
```

Achieve a successful build, stable contents/references, and no missing characters. Follow [qa.md](references/qa.md). Automated audit is limited: class parameters do not prove actual margins on every page; a heading's presence does not prove substantive completeness. `REVIEW` and `NOT_CHECKED` do not mean compliance.

Render the PDF and inspect every page, in batches for long reports. Specifically check the title page/continuation, abstract, multiline contents, section starts, equations, captions, table continuations, appendices, and final page; check the physical MediaBox for A3. Do not present one screenshot as review of the entire document. If tools are unavailable, preserve sources and list unchecked items.

Create a separate `compliance-report.md`: profile/source edition; selected permitted alternatives; applicable clauses and evidence in source/PDF; deviations; unfilled fields; unchecked items. Statuses: `PASS`, `FAIL`, `REVIEW`, `NOT_APPLICABLE`, `NOT_CHECKED`. Organizational clauses, signing, report submission, and official compliance review cannot be marked `PASS` merely because a PDF exists; this skill does not perform them automatically.

Deliver `.tex`, local styles/images/bibliography, the PDF, and a brief review result. Do not add agent instructions or information about the creation process to the submitted report. Keep the compliance note separate. Do not promise certified or unconditional compliance from one successful build.
