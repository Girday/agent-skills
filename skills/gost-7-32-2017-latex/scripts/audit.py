#!/usr/bin/env python3
"""Evidence-limited audit. Exit 1 means detected failure, 2 missing build, 0 no detected failure.
Exit 0 never certifies full GOST compliance; inspect REVIEW and NOT_CHECKED.
Optional pdfplumber checks actual page boxes, text bounds and page-number placement.
"""

import argparse
import json
import re
import sys
from pathlib import Path

TEX_PT_MM = 25.4 / 72.27
PDF_BP_MM = 25.4 / 72


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("project", type=Path)
    p.add_argument("--main", default="main")
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    root = args.project.expanduser().resolve()
    stem = args.main.removesuffix(".tex")
    build = root / "build"
    entries = []

    def add(rule, status, evidence):
        entries.append(dict(rule=rule, status=status, evidence=evidence))

    pdf = build / (stem + ".pdf")
    logpath = build / (stem + ".log")
    if not pdf.exists() or not logpath.exists():
        add("build", "FAIL", "PDF/log missing; compile before audit")
        finish(entries, args.output)
        return 2
    log = logpath.read_text(errors="replace")
    bad = [
        x
        for x in (
            "undefined references",
            "undefined citations",
            "Missing character:",
            "Rerun to get",
            "There were multiply-defined labels",
            "Fatal error",
            "Emergency stop",
            "No pages of output",
        )
        if x in log
    ]
    if "Output written on" not in log:
        bad.append("Final log does not confirm PDF output; an existing PDF may be stale")
    add(
        "build.references",
        "FAIL" if bad else "PASS",
        bad or "No detected unresolved references/glyph errors in final log",
    )
    overfull = re.findall(r"Overfull \\[hv]box[^\n]*", log)
    add(
        "6.1.2.overflow",
        "REVIEW" if overfull else "PASS",
        overfull or "No overfull-box messages in final log",
    )
    underfull = re.findall(r"Underfull \\[hv]box[^\n]*", log)
    if underfull:
        add("6.1.2.spacing", "REVIEW", underfull)
    metricfile = build / (stem + ".gostmetrics")
    if metricfile.exists():
        m = dict(line.split("=", 1) for line in metricfile.read_text().splitlines() if "=" in line)

        def mm(k):
            return float(m[k]) * TEX_PT_MM

        left, top = mm("left_pt"), mm("top_pt")
        right = mm("paperwidth_pt") - left - mm("textwidth_pt")
        bottom = mm("paperheight_pt") - top - mm("textheight_pt")
        actual = dict(left=left, right=right, top=top, bottom=bottom, indent=mm("parindent_pt"))
        expected = dict(left=30, right=15, top=20, bottom=20, indent=12.5)
        good = all(abs(actual[k] - expected[k]) < 0.2 for k in expected)
        add("6.1.1.declared_geometry", "PASS" if good else "FAIL", actual)
        size_bp = float(m["font_pt"]) * 72 / 72.27
        add(
            "6.1.1.declared_body_font",
            "PASS" if size_bp >= 11.99 else "FAIL",
            dict(
                font=m.get("font"),
                size_bp=size_bp,
                baseline_bp=float(m["baseline_pt"]) * 72 / 72.27,
            ),
        )
        add(
            "6.1.1.actual_spacing",
            "REVIEW",
            "Declared baseline is a template choice; inspect actual body lines and local interpretation of 1.5 spacing",
        )
        if m.get("font") != "Times New Roman":
            add(
                "6.1.1.recommended_font",
                "REVIEW",
                "Explicit substitute: "
                + m.get("font", "?")
                + "; TNR is recommended, not mandatory",
            )
    else:
        add(
            "6.1.1.declared_geometry",
            "NOT_CHECKED",
            "No metrics from template; inspect preamble and actual PDF",
        )
    placeholders = []
    for tex in root.rglob("*.tex"):
        if "build" in tex.relative_to(root).parts:
            continue
        for i, line in enumerate(tex.read_text(errors="replace").splitlines(), 1):
            if not line.lstrip().startswith("%") and re.search(r"\[УКАЗАТЬ|\[ЗАПОЛНИТЬ|TODO", line):
                placeholders.append(f"{tex.relative_to(root)}:{i}")
    add(
        "data.completeness",
        "FAIL" if placeholders else "REVIEW",
        placeholders or "No known placeholder patterns; factual verification still required",
    )
    try:
        import pdfplumber
    except ImportError:
        add(
            "pdf.actual_geometry",
            "NOT_CHECKED",
            "pdfplumber unavailable; render/inspect with another installed PDF tool",
        )
    else:
        with pdfplumber.open(pdf) as doc:
            boxes, overflow, footers = [], [], []
            first_has_number = False
            for n, page in enumerate(doc.pages, 1):
                width, height = page.width * PDF_BP_MM, page.height * PDF_BP_MM
                valid = any(
                    abs(width - w) < 0.7 and abs(height - h) < 0.7
                    for w, h in ((210, 297), (297, 210), (297, 420), (420, 297))
                )
                if not valid:
                    boxes.append(dict(page=n, width_mm=width, height_mm=height))
                chars = [c for c in page.chars if c.get("text", "").strip()]
                body = [c for c in chars if c["bottom"] * PDF_BP_MM < height - 15]
                outside = [
                    c
                    for c in body
                    if c["x0"] * PDF_BP_MM < 29.2
                    or c["x1"] * PDF_BP_MM > width - 14.2
                    or c["top"] * PDF_BP_MM < 19.2
                    or c["bottom"] * PDF_BP_MM > height - 19.2
                ]
                if outside:
                    overflow.append(dict(page=n, characters=len(outside)))
                words = page.extract_words()
                footer_words = [w for w in words if w["top"] * PDF_BP_MM > height - 18]
                nums = [w for w in footer_words if w["text"] == str(n)]
                center = (30 + width - 15) / 2
                centered = [
                    w for w in nums if abs((w["x0"] + w["x1"]) / 2 * PDF_BP_MM - center) < 3
                ]
                if n == 1:
                    first_has_number = bool(centered)
                elif not centered:
                    footers.append(n)
            add(
                "6.1.1.pdf_page_boxes",
                "FAIL" if boxes else "PASS",
                boxes
                or f"{len(doc.pages)} A4/A3 page boxes; appropriateness of exceptions needs review",
            )
            add(
                "6.1.1.pdf_text_bounds",
                "REVIEW" if overflow else "PASS",
                overflow
                or "Detected text within nominal margins, excluding footer; graphics/rules require visual review",
            )
            add(
                "6.3.2.title_number",
                "FAIL" if first_has_number else "PASS",
                "Detected centered page 1 footer"
                if first_has_number
                else "No centered page 1 footer detected; title identity needs review",
            )
            add(
                "6.3.1.pdf_pagination",
                "REVIEW" if footers else "PASS",
                footers
                or "Centered physical page numbers 2..N detected; title continuations/inserts require manual review",
            )
            add(
                "5.4.3.contents_exception",
                "REVIEW",
                f"Physical volume {len(doc.pages)} pages; omission of contents allowed only at <=10",
            )
    for rule, evidence in (
        ("5.content", "Verify introduction, methods, results, conclusion and factual source data"),
        (
            "5.3.abstract",
            "Verify 5–15 keywords, case/grammar, one-page text and actual aggregate counts",
        ),
        ("6.2.headings", "Verify case, breaks, hyphenation, indent, numbered hierarchy and toc"),
        (
            "6.5-6.9.objects",
            "Verify every first mention, placement, caption, continuation, formula explanation and source link",
        ),
        (
            "6.10-6.17.special",
            "Verify title, signatures, participants, glossaries, bibliography and appendix status/letter order",
        ),
        (
            "6.1.2.visual",
            "Render and inspect every page including graphics, clipping, tables and glyphs",
        ),
        (
            "3.organizational",
            "Confirm norm control, signatures, registration and submission with organization",
        ),
    ):
        add(rule, "NOT_CHECKED", evidence)
    finish(entries, args.output)
    return 1 if any(x["status"] == "FAIL" for x in entries) else 0


def finish(entries, output):
    report = dict(
        certified=False,
        note="PASS applies only to the named limited check. REVIEW/NOT_CHECKED are unresolved.",
        checks=entries,
    )
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    sys.exit(main())
