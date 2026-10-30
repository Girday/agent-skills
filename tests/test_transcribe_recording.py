import dataclasses
import importlib.util
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/transcribe-recording/scripts/export_transcript.py"
spec = importlib.util.spec_from_file_location("transcript_export", SCRIPT)
exporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)


spec = importlib.util.spec_from_file_location(
    "local_transcriber", ROOT / "skills/transcribe-recording/scripts/transcribe_local.py"
)
transcriber = importlib.util.module_from_spec(spec)
spec.loader.exec_module(transcriber)


class RuntimeTests(unittest.TestCase):
    def test_cpu_default_and_explicit_cuda_do_not_require_mlx(self):
        for system in ["Windows", "Linux", "Darwin"]:
            with self.subTest(system=system):
                options = transcriber.runtime_options(
                    "faster-whisper", system=system, machine="x86_64"
                )
                self.assertEqual(options["device"], "cpu")
                self.assertEqual(options["compute_type"], "int8")
        cuda = transcriber.runtime_options("faster-whisper", device="cuda", system="Linux")
        self.assertEqual(cuda["compute_type"], "float16")

    def test_mlx_rejects_unsupported_hosts_and_ignored_flags(self):
        for system, machine in [("Windows", "AMD64"), ("Linux", "aarch64"), ("Darwin", "x86_64")]:
            with self.assertRaises(ValueError):
                transcriber.runtime_options("mlx", system=system, machine=machine)
        self.assertEqual(
            transcriber.runtime_options("mlx", system="Darwin", machine="arm64")["device"], "metal"
        )
        with self.assertRaises(ValueError):
            transcriber.runtime_options("mlx", device="cuda", system="Darwin", machine="arm64")

    def test_faster_whisper_consumes_lazy_output_and_preserves_word_fields(self):
        @dataclasses.dataclass
        class Word:
            start: float = 0.1
            end: float = 0.3
            word: str = "test"
            probability: float = 0.8

        @dataclasses.dataclass
        class Segment:
            start: float
            end: float
            text: str
            words: list

        @dataclasses.dataclass
        class Info:
            language: str = "en"

        observed = {}

        class Model:
            def __init__(self, model, **kwargs):
                observed.update(kwargs)

            def transcribe(self, audio, **kwargs):
                observed.update(kwargs)

                def lazy():
                    observed["consumed"] = True
                    yield Segment(0, 1, "test", [Word()])

                return lazy(), Info()

        module = types.ModuleType("faster_whisper")
        module.WhisperModel = Model
        with patch.dict(sys.modules, {"faster_whisper": module}):
            raw = transcriber.transcribe_audio(
                [], Path("model"), "auto", transcriber.runtime_options("faster-whisper")
            )
        self.assertTrue(observed["consumed"])
        self.assertIsNone(observed["language"])
        self.assertFalse(observed["vad_filter"])
        self.assertEqual(raw["segments"][0]["words"][0]["word"], "test")
        self.assertEqual(raw["info"]["language"], "en")


class TranscriptExportTests(unittest.TestCase):
    def job(self, root, name="job", start=0, duration=10, segments=None, **extra):
        path = root / name
        path.mkdir()
        manifest = dict(
            schema_version=1,
            source_sha256="synthetic-hash",
            source_name="synthetic.wav",
            model="test-model",
            language="ru",
            asr_status="complete_unreviewed",
            start=start,
            duration=duration,
        )
        manifest.update(extra)
        (path / "manifest.json").write_text(json.dumps(manifest))
        (path / "asr.raw.json").write_text(
            json.dumps(
                {
                    "segments": segments
                    if segments is not None
                    else [dict(start=0, end=1, text=" hello ")]
                }
            )
        )
        return path

    def test_preserves_uncertain_text_raw_bytes_and_absolute_offset(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            job = self.job(
                root,
                start=120,
                segments=[dict(start=0, end=0, text=" θ? "), dict(start=1, end=2, text=" не 5 ")],
            )
            original = (job / "asr.raw.json").read_bytes()
            dest = root / "result"
            exporter.export([job], dest)
            rows = json.loads((dest / "transcript.json").read_text())
            self.assertEqual([row["text"] for row in rows], [" θ? ", " не 5 "])
            self.assertEqual(rows[0]["start"], 120)
            self.assertIn("short_segment", rows[0]["flags"])
            self.assertTrue(all(row["speaker"] is None for row in rows))
            self.assertEqual((dest / "raw/job-001/asr.raw.json").read_bytes(), original)
            self.assertEqual(
                json.loads((dest / "manifest.json").read_text())[
                    "unprocessed_intervals_before_or_between_jobs"
                ],
                [[0.0, 120]],
            )
            marker = dest / "manual.md"
            marker.write_text("keep")
            with self.assertRaises(FileExistsError):
                exporter.export([job], dest)
            self.assertEqual(marker.read_text(), "keep")

    def test_sorts_chunks_and_reports_gap_without_claiming_end_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = self.job(root, "first")
            second = self.job(root, "second", start=12)
            output = root / "out"
            exporter.export([second, first], output)
            manifest = json.loads((output / "manifest.json").read_text())
            self.assertEqual(manifest["unprocessed_intervals_before_or_between_jobs"], [[10, 12]])
            self.assertEqual(manifest["source_end_coverage"], "not_verified")
            rows = json.loads((output / "transcript.json").read_text())
            self.assertEqual([r["start"] for r in rows], [0, 12])

    def test_segment_ids_survive_adding_an_earlier_chunk(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            later = self.job(root, "later", start=20)
            earlier = self.job(root, "earlier")
            _, alone, _ = exporter.prepare([later])
            _, combined, _ = exporter.prepare([earlier, later])
            self.assertEqual(alone[0]["id"], combined[1]["id"])

    def test_rejects_overlap_mismatch_and_invalid_times_before_writing(self):
        cases = [
            dict(start=9),
            dict(start=10, source_sha256="other"),
            dict(start=10, model="other"),
            dict(start=10, model_fingerprint={"weights": "changed"}),
            dict(start=10, versions={"mlx": "changed"}),
            dict(start=10, runtime={"backend": "faster-whisper", "device": "cuda"}),
            dict(start=10, segments=[dict(start=0, end=11, text="outside")]),
            dict(start=10, segments=[dict(start=float("nan"), end=1, text="nan")]),
            dict(
                start=10, segments=[dict(start=2, end=3, text="a"), dict(start=1, end=2, text="b")]
            ),
        ]
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                first = self.job(root, "first")
                second = self.job(root, "second", **case)
                with self.assertRaises(ValueError):
                    exporter.export([first, second], root / "result")
                self.assertFalse((root / "result").exists())

    def test_empty_text_remains_in_raw_and_word_flag_does_not_delete_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            job = self.job(
                root,
                segments=[
                    dict(start=0, end=1, text=" "),
                    dict(start=1, end=2, text="keep", words=[dict(start=1, end=1)]),
                ],
            )
            _, rows, _ = exporter.prepare([job])
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["text"], "keep")
            self.assertEqual(rows[0]["flags"], ["short_word"])


if __name__ == "__main__":
    unittest.main()
