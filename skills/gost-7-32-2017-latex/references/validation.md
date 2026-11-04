# Skill Distribution Validation

Date: October 28, 2026. This records validation of a specific template and scripts, not permission to consider every future document GOST-compliant.

- Standard `quick_validate.py`: skill valid; YAML/name/structure checked.
- Requirements map: compared 128 actual numbered clauses/heading groups in sections 3, 5, 6 against the scan; no missing identifiers. Sections 1, 2, 4 and appendices А–Е reviewed separately. Identifier presence alone does not prove paraphrase completeness; content was read and compared against rules, mandatory-element bold emphasis and the rotated correction were inspected in images.
- XeLaTeX, TeX Live 2025, macOS, Times New Roman; math font `latinmodern-math.otf`. Demonstration report: 8 pages, stable references, no overfull, missing glyphs, or LaTeX warnings. Small underfull warnings on some lines accepted after visual review.
- Test document: 9 pages; 70-row table continuing on pp. 4, 5, 6; repeated headers/borders; multiline appendix contents entry; footnote; lists/notes; headings without a final period after the number added by the Russian language package.
- Verified figure/equation labels 1.1, 2.1, А.1; tables 1.1, Б.1; sequence of 25 Cyrillic letters with exclusions and transition to numbers after exhaustion.
- Actual demonstration PDF size A4; declared margins 30/15/20/20 mm, indent 12.5 mm, body font 14 bp; text-boundary and page-number analysis found no violations. All 8 demonstration pages and 9 test pages visually reviewed; the affected page rechecked after list-indent fixes.
- `init_project.py` refused to overwrite an existing project; the source's control hash was unchanged.
- Negative checks: `audit.py` detected a PDF with corrupted MediaBox; detected a stale PDF left behind when the final log did not indicate successful output.
- LuaLaTeX sources and commands are available, but this distribution was actually tested with XeLaTeX. A3, multiple volumes, biber, title-page continuation, and external normative standards did not receive separate executable trials; instructions describe necessary actions/checks without claiming automatic execution.

The starter intentionally has unfilled administrative fields and should receive `FAIL` for data completeness until replaced. The demonstration PDF uses fictional organization/names and educational observations; it is not an approved research report. Scientific results and organizational compliance review are not certified.

## Follow-up: November 4, 2026

The earlier pagination check had a false negative: it used the text-area center rather than the physical sheet center. With 30/15 mm side margins, the old template placed page numbers 7.5 mm to the right of the sheet center. The template now configures the `plain` page style itself, including chapter-opening pages; the audit uses half the actual PDF page width. A regression fixture exercises chapter starts and a change to 35/15 mm margins, and verifies that the old text-centered footer receives `REVIEW`.

XeLaTeX regression checks and the eight-page demonstration build pass; measured page-number offsets are below 0.01 mm. LuaLaTeX also builds the three-page pagination fixture and eight-page demonstration after supplying `lualatex-math` in an isolated TeX tree and a writable font cache. These are engine and pagination checks, not certification of the reports or of special modes. The initial limits for A3, multiple volumes, biber, and title-page continuation remain.

Long appendix contents entries exposed a separate layout defect: an entry could overfill its line and lose visible dot leaders. The appendix formatter now preserves ordinary word spacing, paragraph line height, a right-aligned page column, and a minimum leader span. A dedicated six-page XeLaTeX fixture checks long entries, baseline separation, and actual PDF page-number positions. A model's bottom-aligned `parbox` workaround was rejected because it compressed spacing between entries; it is not part of the template.
