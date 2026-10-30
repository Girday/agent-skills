# LaTeX Implementation and Extensions

## Starter project

`assets/template/` contains `main.tex`, `metadata.tex`, `title.tex`, and `gost732.sty`. This is a single-volume XeLaTeX/LuaLaTeX example, not a completed report. `metadata.tex` has visible unfilled fields; do not use demonstration research results as real data. Required packages: `extreport`, `fontspec`, `polyglossia`, `unicode-math`, `geometry`, `amsmath`, `graphicx`, `array`, `longtable`, `caption`, `indentfirst`, `etoolbox`, `hyperref`. Install missing packages only when necessary and in an authorized environment.

Body text: 14 bp, baselines 21 bp apart. This is a fixed implementation of the selected one-and-a-half spacing, not a numerical GOST definition. Compare actual output for agreement with Word/local compliance review; do not multiply spacing again through `setspace`. Single-spaced blocks: 14/16.8 bp; footnotes/small text: 12/14.4 bp. `bp` = 1/72 inch; TeX `pt` = 1/72.27 inch. Distinguish them when measuring PDFs.

`gost732.sty` selects TNR, then explicitly warns about substitution with Liberation Serif/CMU Serif; Latin Modern Math is an allowed implementation choice. Do not embed unlicensed font files in the delivered project.

## Command semantics

| Report content | Command | Note |
|---|---|---|
| Section 1 | `\chapter{Название}` | New page, number and heading at paragraph indent |
| Subsection 1.1 | `\section{Название}` | Bold, paragraph indent |
| Clause 1.1.1 | `\subsection{Название}` | Do not create a sole clause; an untitled clause needs a separate number/paragraph, not an empty heading |
| Subclause 1.1.1.1 | `\subsubsection{Название}` | Same; four levels counted from chapter |
| Structural element | `\GostStructural{ВВЕДЕНИЕ}` | Uppercase, centered, new page, toc entry |
| Contents | `\GostTOC` | Does not include itself; starts with structural heading |
| Title page | `GostTitlePage` | Number hidden, counter not reset |
| Keywords | `\GostKeywords{первое, второе, …}` | Manually check 5–15 items |
| Figure/table | `figure`/`table` and `\caption` | Figure caption after graphic/explanations; table caption before data |
| Object reference | `рисунок~\ref{fig:key}` | Corresponding full word for tables/appendices |
| Equation | `equation` + `\label`, `\eqref` | Centered, number right, parentheses |
| Symbol explanations | `\GostWhere{...}` | Starts with “где” without colon; each symbol on a new line |
| Note | `\GostNote{Текст}` | Paragraph indent; sole note unnumbered |
| Multiple notes | `GostNotes` + `\item` | Numbers without periods |
| Dashes/numbers | `GostDashes` / `GostNumbers` | Nested numbered lists need a separate counter; do not blindly share `enumi` |
| Appendix | `\GostAppendix{Заголовок}{статус}{app:key}` | New page, Cyrillic letter, object counters reset, status/title in toc |
| Sources | `GostSources`, `\GostSource{src:key}{описание}` | Manually ordered by first citation; numbers with periods |
| Source citation | `\GostCite{src:key}` | Square brackets; verify actual metadata |

For clause-only division or sections without subsections, deliberately adapt counters/commands under 6.4.2–6.4.4. Do not create a fictitious level merely for number appearance. Headings do not end with periods; multiple sentences may have internal periods. The template suppresses word hyphenation in headings/captions, but an excessively long word can still exceed margins.

By default, figures/tables/equations use continuous numbering, independent of `chapter` resets. For section-based numbering, call `\GostNumberWithinSections` in the preamble. Within appendices, numbers are А.1, etc.; do not call `\chapter` in an appendix; start its sections with `\section` (А.1). Do not mix Cyrillic А with Latin A in displayed numbers. `label` identifiers may use Latin letters.

## Title-page variants

The template shows matching research/report titles and one approval block. For differing titles, add the research title with an initial capital, then “по теме:” and the uppercase report title. For interim reports, add the stage in parentheses after the type. For multiple volumes, add “Книга N” below the type. For two endorsement/approval blocks, use two `minipage` blocks of 0.47 width: endorsement left, approval right. Check blocks against 6.10; do not arbitrarily enlarge block spacing.

For one contributor, put their position/degree/academic title/initials/surname on the title page. Do not equate contributor and research-supervisor roles without evidence. There is no separate contributor list for one person. For a team, add a structural contributor-list element with three columns and no visible grid: positions; space for signatures/dates; names and work sections; organization for external participants.

If signatures do not fit, add continuation under 6.10.1 with the required phrases; city/year only on the first sheet. Include the extra sheet in pagination. Record hiding its page number as a selected interpretation and check with the organization, since 6.3.2 does not address it separately. Printed black lines reserve space for real blue signatures and seals.

## Terms and abbreviations

Terms introduction: “В настоящем отчете о НИР применяют следующие термины с соответствующими определениями”.

Abbreviations introduction: “В настоящем отчете о НИР применяют следующие сокращения и обозначения”.

Follow with an alphabetical list without paragraph indent: term/abbreviation, dash, explanation, no final punctuation. For exactly three symbols, record the choice under local rules. A Russian lettered list uses the same letters as appendices, in lowercase: `а, б, в, г, д, е, ж, и, к, л, м, н, п, р, с, т, у, ф, х, ц, ш, щ, э, ю, я`; marker with closing parenthesis.

## Table continuation

Do not put a multipage table in a floating `table`. `longtable` manages pages itself. Title only over the first part, then “Продолжение таблицы N”; do not use `\caption` on every part, as it creates false numbers/entries.

```latex
В таблице~\ref{tab:long} приведены результаты наблюдений.
\begin{longtable}{|p{75mm}|>{\centering\arraybackslash}p{75mm}|}
\caption{Результат наблюдения}\label{tab:long}\\
\hline Наблюдение & Значение\\\hline
\endfirsthead
\multicolumn{2}{@{}l}{\GostSingle Продолжение таблицы \thetable}\\
\hline Наблюдение & Значение\\\hline
\endhead
\hline\endfoot
\hline\endlastfoot
Первое & 1\\
% More rows with actual data
Последнее & 2\\
\end{longtable}
```

Two 75 mm columns plus intercolumn space and rules fit within 165 mm of text width. Account for `tabcolsep`/rules. If a smaller font is needed, use local `\small`, not `resizebox` on the entire table; check readability. `longtable` may require another pass for column widths. Single spacing is mandatory for multiline captions, not automatically the whole table body.

## Equations

Explain symbols in occurrence order, not alphabetically. For a long equation:

```latex
\begin{equation}
\begin{aligned}
S &= a_1+a_2+a_3+{}\\
  &\quad +a_4+a_5.
\end{aligned}
\end{equation}
```

The sign at the end of the first line repeats at the start of the next. Use `\times` at multiplication breaks, not a dot/asterisk. Mathematical punctuation follows the sentence. Do not hide an entire line in `\small` to make it fit; change line breaks.

## Bibliography

For short verified lists, manual template commands avoid an extra dependency. They **do not sort automatically**: entries must follow first-citation order. List numbers have periods; text references have brackets; do not substitute one format for the other. Large lists may use `biblatex`/`biber` with a checked style, `sorting=none`, numeric citations, and a period after each list number. `build.py` does not run biber: run it separately, then rerun LaTeX until stable. Check every entry against current applicable standards, not just the style name.

## A3 and multiple volumes

The default template is A4 only. A3 requires actual PDF page size 297×420 mm (or rotated), suitable margins, and pagination; `landscape`, `resizebox`, or `newgeometry` alone does not change MediaBox. XeLaTeX changes driver `papersize`; LuaLaTeX changes engine page dimensions; restore A4 afterward and check both sides of the transition. A prepared A3 PDF can be included through a suitable mechanism preserving physical size and correct page number. Implement and verify the specific method on the actual engine for such tasks; this example is not ready-made mixed-format automation.

For multiple volumes, use a separate project for each, with its own title/contents/objects; the first contains the overall structure with volume numbers (later volumes' titles alone are permitted). Reconcile shared titles and abstract statistics. Do not silently replace report-wide continuity under 6.3.1 with per-file resets; record the cross-volume pagination decision with the organization. For overall numbering, explicitly set `\setcounter{page}{N}` and check joins; individual-volume audits then require adapted expected physical page numbers. Do not claim multi-volume validation from a single-volume example.
