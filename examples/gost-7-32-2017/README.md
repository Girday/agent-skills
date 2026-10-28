# GOST report layout example

[Open the PDF](example.pdf). Its eight pages demonstrate the title, abstract, contents, body section, table, figure, equation, conclusion, source list, and appendix.

The organization, names, and research data are educational examples. This is not a signed or registered research report. The source text says so explicitly; the PDF illustrates layout rather than scientific or institutional approval.

The editable project is in [source/](source/). From the repository root:

```bash
python3 skills/gost-7-32-2017-latex/scripts/build.py examples/gost-7-32-2017/source
python3 skills/gost-7-32-2017-latex/scripts/audit.py examples/gost-7-32-2017/source
```

The published PDF was compiled with XeLaTeX and Times New Roman. A different installed fallback font may change page breaks. See the skill's [validation record](../../skills/gost-7-32-2017-latex/references/validation.md) for the initial checks and their limits.
