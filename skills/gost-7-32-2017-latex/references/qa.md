# Compliance Review and Automation Limits

For distribution checks and untested modes, see [validation.md](validation.md). They do not replace review of a new document.

## Stages

1. **Data:** type/profile/edition, local requirements, applicability of each map clause; real administrative details, results, sources; no unfilled fields.
2. **Build:** successful exit code, stable `.aux/.toc/.out`, no undefined references/citations, missing characters, or duplicate labels. Review every overfull/underfull warning: fix causes rather than suppress warnings.
3. **Objective measurements:** every page's MediaBox; configured/actual text boundaries; body font/size/color/baselines; paragraphs; page numbers. TeX pt differs from PDF bp. Metrics are recorded only at document start and do not detect later local reconfiguration.
4. **Visual review of every page:** headings/new pages/whitespace, Cyrillic/math, headers/footers, tables/captions/continuations, appendices. The number of reviewed pages must match PDF length; track ranges for large reports. Inspect at a readable scale, enlarging problem areas as needed.
5. **Content relationships:** all toc titles/pages; each first object mention and placement; captions, numbers, explanations, transitions; abstract statistics; source/appendix order.
6. **Organizational conditions:** genuine signatures/dates/seal, registration, approval, compliance review, paper/printing/submission require separate evidence; do not infer them from a file.

## Rendering

Use installed `pdftoppm`/`mutool`/another available renderer. Example:

```bash
pdftoppm -r 110 -png /absolute/report/build/main.pdf /absolute/report/build/page
```

If Poppler cannot find fontconfig, provide a **temporary** configuration with system font directories and a writable cache through `FONTCONFIG_FILE`; do not change user configuration just for review. Do not leave a stuck process repeating messages. Extracted-text checks do not replace rendering.

## What audit.py checks

| Check | Basis | Limitation |
|---|---|---|
| Build/references/glyphs | Final log | Does not prove scientific correctness |
| Overflows | Overfull/underfull | Visual assessment required; floats can cause cosmetic warnings |
| Declared margins/indent/font | `.gostmetrics` | Initial configuration; local changes remain possible |
| Unfilled data | Template markers in `.tex` | Does not recognize all placeholders; skips comments |
| Actual formats | MediaBox through pdfplumber | A3 allowed only when applicable; rotation accounted for |
| Text boundaries | PDF character coordinates | Not all graphics/lines; 0.8 mm tolerance; footer analyzed separately; REVIEW requires inspection |
| Pagination | Physical pages 2..N and footer center | Title continuation, inserts with own numbering, multiple volumes/initial N need manual analysis |

`audit.py` requires only the standard library; additional geometry checks use `pdfplumber` when available. Without it, those checks report `NOT_CHECKED`. Exit 0 means “no detected errors in performed checks”; `certified` is always false. Exit 1 indicates a detected error; 2 means no build. The demonstration template should fail for unfilled data until fields are replaced.

## Compliance note

Create `compliance-report.md` separately from the report:

```markdown
Profile: research report / coursework adaptation
Edition: GOST 7.32-2017, corrections ИУС 2–2019, 3–2020, 1–2022
Source and verification date: …
Local requirements: …
Implementation choices: 14 bp, font …, numbering …

| Clause | Applicability | Status | Evidence / remaining work |
|---|---|---|---|
| 6.1.1 margins | yes | PASS | parameters + page measurements … |
| 5.2.2 | one contributor | PASS | details on title page, no separate list |
| 6.6.3 | multipage table | REVIEW | continuation on p. … not yet inspected |
| 3.5 | yes | NOT_CHECKED | no organizational compliance-review confirmation |

Deviations and grounds: …
Unfilled fields: …
Visually inspected: pages … of …
Outcome: what is ready and what prevents submission.
```

For full compliance review, check every applicable requirements.md row, not just the four example rows. `NOT_APPLICABLE` needs a reason (e.g. no patent studies or tables). Do not apply a machine PASS to an entire clause with several independent requirements. Do not present the service report as an official organizational certificate.
