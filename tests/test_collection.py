import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pdfplumber
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "gost-7-32-2017-latex"


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


installer = load("local_installer", ROOT / "scripts" / "install.py")
validator = load("collection_validator", ROOT / "scripts" / "validate.py")
builder = load("report_builder", SKILL / "scripts" / "build.py")


class InstallationTests(unittest.TestCase):
    def test_installs_complete_skill_and_preserves_existing_copy(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory)
            installed = installer.install(SKILL.name, dest)
            self.assertEqual(
                (installed / "SKILL.md").read_bytes(), (SKILL / "SKILL.md").read_bytes()
            )
            self.assertTrue((installed / "LICENSE.txt").is_file())
            marker = installed / "user-file.txt"
            marker.write_text("keep me", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                installer.install(SKILL.name, dest)
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep me")

    def test_rejects_path_traversal(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                installer.install("../outside", Path(directory))

    def test_project_initializer_refuses_overwrite_without_partial_copy(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / "report"
            dest.mkdir()
            (dest / "main.tex").write_text("user source", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SKILL / "scripts" / "init_project.py"), str(dest)],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual((dest / "main.tex").read_text(encoding="utf-8"), "user source")
            self.assertEqual(sorted(p.name for p in dest.iterdir()), ["main.tex"])


class ValidationTests(unittest.TestCase):
    def make_skill(self, root):
        skill = root / "skills" / "example"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "---\nname: example\ndescription: A test skill\n---\n\n# Example\n",
            encoding="utf-8",
        )
        return skill

    def test_collection_passes(self):
        self.assertEqual(validator.validate(ROOT), [])

    def test_invalid_metadata_and_broken_links_are_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = self.make_skill(root)
            text = (skill / "SKILL.md").read_text(encoding="utf-8")
            (skill / "SKILL.md").write_text(
                text.replace("name: example", "name: wrong") + "[missing](missing.md)\n",
                encoding="utf-8",
            )
            errors = validator.validate(root)
            self.assertTrue(any("name differs" in e for e in errors))
            self.assertTrue(any("broken/outside link" in e for e in errors))

    def test_personal_paths_are_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = self.make_skill(root)
            (skill / "notes.md").write_text(
                "/" + "Users" + "/someone/private-file", encoding="utf-8"
            )
            self.assertTrue(any("personal machine path" in e for e in validator.validate(root)))


class AuditTests(unittest.TestCase):
    def audit(self, root):
        result = subprocess.run(
            [sys.executable, str(SKILL / "scripts" / "audit.py"), str(root)],
            capture_output=True,
            text=True,
        )
        return result.returncode, json.loads(result.stdout)

    def make_pdf(self, root, width=595.276, height=841.89):
        build = root / "build"
        build.mkdir()
        writer = PdfWriter()
        writer.add_blank_page(width=width, height=height)
        with (build / "main.pdf").open("wb") as stream:
            writer.write(stream)
        (build / "main.log").write_text("Output written on build/main.pdf\n", encoding="utf-8")
        return build

    def test_missing_build_is_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            code, report = self.audit(Path(directory))
            self.assertEqual(code, 2)
            self.assertFalse(report["certified"])

    def test_bad_page_size_is_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_pdf(root, 500, 500)
            code, report = self.audit(root)
            self.assertEqual(code, 1)
            self.assertIn(
                "6.1.1.pdf_page_boxes",
                [c["rule"] for c in report["checks"] if c["status"] == "FAIL"],
            )

    def test_old_pdf_does_not_mask_failed_compilation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build = self.make_pdf(root)
            (build / "main.log").write_text("No pages of output.\n", encoding="utf-8")
            code, report = self.audit(root)
            self.assertEqual(code, 1)
            self.assertEqual(report["checks"][0]["status"], "FAIL")

    def test_unfilled_data_is_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_pdf(root)
            (root / "metadata.tex").write_text("[УКАЗАТЬ ИМЯ]\n", encoding="utf-8")
            code, report = self.audit(root)
            self.assertEqual(code, 1)
            self.assertTrue(
                any(
                    c["rule"] == "data.completeness" and c["status"] == "FAIL"
                    for c in report["checks"]
                )
            )

    def test_partial_checks_never_claim_certification(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_pdf(root)
            code, report = self.audit(root)
            self.assertEqual(code, 0)
            self.assertFalse(report["certified"])
            self.assertTrue(any(c["status"] == "NOT_CHECKED" for c in report["checks"]))


@unittest.skipUnless(builder.engine_path("xelatex"), "XeLaTeX not installed")
class LatexIntegrationTests(unittest.TestCase):
    def test_long_appendix_contents_keep_spacing_and_page_leaders(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copy2(SKILL / "assets/template/gost732.sty", root / "gost732.sty")
            shutil.copy2(ROOT / "tests/fixtures/gost-contents.tex", root / "main.tex")
            result = subprocess.run(
                [sys.executable, str(SKILL / "scripts/build.py"), str(root)],
                capture_output=True,
                text=True,
                timeout=180,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            log = (root / "build/main.log").read_text()
            self.assertNotIn("Overfull", log)
            with pdfplumber.open(root / "build/main.pdf") as doc:
                self.assertEqual(len(doc.pages), 6)
                toc = doc.pages[1]
                lines = [line for line in toc.extract_text_lines() if line["top"] < 750]
                for previous, following in zip(lines, lines[1:]):
                    self.assertGreaterEqual(following["top"] - previous["top"], 20.5)
                for page in (4, 5, 6):
                    entry = next(line for line in lines if line["text"].endswith(f" {page}"))
                    self.assertGreaterEqual(entry["text"].count("."), 2)
                    self.assertAlmostEqual(entry["x1"], toc.width - 15 * 72 / 25.4, delta=1)
            source = (root / "main.tex").read_text()
            (root / "main.tex").write_text(
                source.replace(r"\begin{document}", r"\setcounter{tocdepth}{-1}\begin{document}")
            )
            result = subprocess.run(
                [sys.executable, str(SKILL / "scripts/build.py"), str(root)],
                capture_output=True,
                text=True,
                timeout=180,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            with pdfplumber.open(root / "build/main.pdf") as doc:
                self.assertNotIn("ПРИЛОЖЕНИЕ", doc.pages[1].extract_text())

    def test_page_numbers_use_sheet_center_after_margin_changes(self):
        fixture = (ROOT / "tests" / "fixtures" / "gost-pagination.tex").read_text()
        old_footer = (
            r"\makeatletter"
            r"\renewcommand\ps@plain{"
            r"\let\@oddhead\@empty\let\@evenhead\@empty"
            r"\def\@oddfoot{\normalfont\normalsize\hfil\thepage\hfil}"
            r"\let\@evenfoot\@oddfoot}"
            r"\pagestyle{plain}"
            r"\makeatother"
        )
        engine = "xelatex"
        for centered_on_sheet in (False, True):
            with self.subTest(engine=engine, centered_on_sheet=centered_on_sheet):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    shutil.copy2(SKILL / "assets/template/gost732.sty", root / "gost732.sty")
                    source = fixture
                    if not centered_on_sheet:
                        source = source.replace(
                            r"\begin{document}", old_footer + "\n" + r"\begin{document}"
                        )
                        source = source.replace(
                            r"\begin{GostTitlePage}",
                            r"\begin{GostTitlePage}\thispagestyle{plain}",
                        )
                    (root / "main.tex").write_text(source)
                    result = subprocess.run(
                        [
                            sys.executable,
                            str(SKILL / "scripts/build.py"),
                            str(root),
                            "--engine",
                            engine,
                        ],
                        capture_output=True,
                        text=True,
                        timeout=180,
                    )
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    with pdfplumber.open(root / "build/main.pdf") as doc:
                        self.assertEqual(len(doc.pages), 3)
                        for number, page in enumerate(doc.pages[1:], 2):
                            words = [
                                w
                                for w in page.extract_words()
                                if w["text"] == str(number) and w["top"] > page.height - 60
                            ]
                            self.assertEqual(len(words), 1)
                            center = (words[0]["x0"] + words[0]["x1"]) / 2
                            offset_mm = abs(center - page.width / 2) * 25.4 / 72
                            if centered_on_sheet:
                                self.assertLess(offset_mm, 0.5)
                            else:
                                self.assertGreater(offset_mm, 7)
                    audit = subprocess.run(
                        [sys.executable, str(SKILL / "scripts/audit.py"), str(root)],
                        capture_output=True,
                        text=True,
                    )
                    checks = json.loads(audit.stdout)["checks"]
                    title = next(c for c in checks if c["rule"] == "6.3.2.title_number")
                    self.assertEqual(title["status"], "PASS" if centered_on_sheet else "FAIL")
                    pagination = next(c for c in checks if c["rule"] == "6.3.1.pdf_pagination")
                    self.assertEqual(
                        pagination["status"], "PASS" if centered_on_sheet else "REVIEW"
                    )
                    if not centered_on_sheet:
                        self.assertEqual(pagination["evidence"], [2, 3])

    def test_numbering_longtable_and_appendix_alphabet(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copy2(SKILL / "assets" / "template" / "gost732.sty", root / "gost732.sty")
            shutil.copy2(ROOT / "tests" / "fixtures" / "gost-numbering.tex", root / "main.tex")
            result = subprocess.run(
                [sys.executable, str(SKILL / "scripts" / "build.py"), str(root)],
                capture_output=True,
                text=True,
                timeout=180,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            aux = (root / "build" / "main.aux").read_text(encoding="utf-8")
            for key, number in (
                ("fig:first", "1.1"),
                ("eq:first", "1.1"),
                ("tab:long", "1.1"),
                ("fig:second", "2.1"),
                ("eq:second", "2.1"),
                ("fig:app", "А.1"),
                ("eq:app", "А.1"),
                ("tab:app", "Б.1"),
            ):
                self.assertIn(f"newlabel{{{key}}}{{{{{number}}}", aux)
            pages = PdfReader(root / "build" / "main.pdf").pages
            texts = [p.extract_text() for p in pages]
            self.assertTrue(any("Продолжение таблицы 1.1" in text for text in texts))
            text = " ".join(" ".join(texts).split())
            self.assertIn("А Б В Г Д Е Ж И К Л М Н П Р С Т У Ф Х Ц Ш Щ Э Ю Я 1", text)
            self.assertNotIn("1.1. Заголовок подраздела", text)


if __name__ == "__main__":
    unittest.main()
