#!/usr/bin/env python3
"""Run a bounded local Whisper job on CPU/CUDA or Apple Silicon; retain raw relative timestamps."""

import argparse
import hashlib
import importlib.metadata
import json
import math
import platform
import subprocess
import sys
import warnings
from dataclasses import asdict
from pathlib import Path


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def finite_nonnegative(value):
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError("expected finite nonnegative seconds")
    return number


def runtime_options(backend, device=None, compute_type=None, system=None, machine=None):
    if backend == "mlx":
        if (system or platform.system()) != "Darwin" or (
            machine or platform.machine()
        ).lower() not in {"arm64", "aarch64"}:
            raise ValueError("MLX requires macOS on Apple Silicon; use faster-whisper here")
        if device is not None or compute_type is not None:
            raise ValueError("--device and --compute-type apply only to faster-whisper")
        return {"backend": "mlx", "device": "metal", "compute_type": "float16"}
    if backend != "faster-whisper":
        raise ValueError("unknown backend")
    device = device or "cpu"
    if device not in {"cpu", "cuda"}:
        raise ValueError("faster-whisper device must be cpu or cuda")
    return {
        "backend": backend,
        "device": device,
        "compute_type": compute_type or ("int8" if device == "cpu" else "float16"),
    }


def transcribe_audio(audio, model_path, language, runtime):
    language = None if language == "auto" else language
    if runtime["backend"] == "mlx":
        import mlx_whisper

        return mlx_whisper.transcribe(
            audio,
            path_or_hf_repo=str(model_path),
            language=language,
            word_timestamps=True,
            verbose=False,
        )
    from faster_whisper import WhisperModel

    model = WhisperModel(
        str(model_path), device=runtime["device"], compute_type=runtime["compute_type"]
    )
    segments, info = model.transcribe(
        audio, language=language, word_timestamps=True, vad_filter=False
    )
    # Consuming the generator runs inference. Save all native segment fields.
    return {"segments": [asdict(segment) for segment in segments], "info": asdict(info)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--model", required=True, help="Local model path or HF model ID")
    parser.add_argument("--backend", choices=["faster-whisper", "mlx"], default="faster-whisper")
    parser.add_argument("--device", choices=["cpu", "cuda"])
    parser.add_argument(
        "--compute-type", help="CTranslate2 type; default int8 on CPU, float16 on CUDA"
    )
    parser.add_argument("--language", default="auto", help="Language code or auto")
    parser.add_argument("--start", type=finite_nonnegative, default=0.0)
    parser.add_argument("--duration", type=finite_nonnegative, default=90.0)
    args = parser.parse_args()
    if not args.source.is_file():
        parser.error("source is not a file")
    try:
        runtime = runtime_options(args.backend, args.device, args.compute_type)
    except ValueError as error:
        parser.error(str(error))
    # Import only on execution; help and argument checks need no ASR runtime.
    import imageio_ffmpeg
    import numpy as np
    from huggingface_hub import snapshot_download

    args.output.mkdir(parents=True, exist_ok=False)
    source_hash = sha256(args.source)
    model_path = Path(args.model)
    if not model_path.is_dir():
        model_path = Path(snapshot_download(repo_id=args.model))
    if args.backend == "mlx":
        weights = model_path / "weights.safetensors"
        if not weights.is_file():
            weights = model_path / "weights.npz"
        files = [model_path / "config.json", weights]
    else:
        if not (model_path / "model.bin").is_file():
            raise ValueError("faster-whisper requires a converted CTranslate2 model with model.bin")
        files = sorted(
            file for file in model_path.iterdir() if file.suffix in {".bin", ".json", ".txt"}
        )
    fingerprint = {file.name: sha256(file) for file in files}
    command = [imageio_ffmpeg.get_ffmpeg_exe(), "-nostdin", "-v", "warning"]
    command += ["-ss", str(args.start), "-i", str(args.source.resolve())]
    if args.duration:
        command += ["-t", str(args.duration)]
    command += ["-ac", "1", "-ar", "16000", "-f", "f32le", "pipe:1"]
    decoded = subprocess.run(command, capture_output=True, check=False)
    (args.output / "decode.log").write_bytes(decoded.stderr)
    decoded.check_returncode()
    audio = np.frombuffer(decoded.stdout, dtype="<f4").copy()
    del decoded
    if not len(audio):
        raise ValueError("decoded interval contains no samples")
    duration = len(audio) / 16000
    with warnings.catch_warnings(record=True) as notices:
        warnings.simplefilter("always")
        try:
            raw = transcribe_audio(audio, model_path, args.language, runtime)
        finally:
            inference_log = "\n".join(
                f"{item.category.__name__}: {item.message}" for item in notices
            )
            (args.output / "inference.log").write_text(inference_log, encoding="utf-8")
            if inference_log:
                print(inference_log, file=sys.stderr)
    (args.output / "asr.raw.json").write_text(
        json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    if sha256(args.source) != source_hash:
        raise RuntimeError("source changed during processing; job not finalized")
    packages = ["imageio-ffmpeg", "numpy", "huggingface-hub"]
    packages += (
        ["mlx-whisper", "mlx"] if args.backend == "mlx" else ["faster-whisper", "ctranslate2"]
    )
    versions = {name: importlib.metadata.version(name) for name in packages}
    manifest = {
        "schema_version": 1,
        "source_name": args.source.name,
        "source_sha256": source_hash,
        "model": args.model,
        "model_fingerprint": fingerprint,
        "runtime": runtime,
        "platform": platform.platform(),
        "language": args.language,
        "start": args.start,
        "duration": duration,
        "requested_duration": args.duration,
        "sample_rate": 16000,
        "channels": 1,
        "versions": versions,
        "asr_status": "complete_unreviewed",
        "diarization_status": "not_performed",
        "audio_review_status": "not_performed",
        "decode_has_warnings": bool((args.output / "decode.log").stat().st_size),
        "inference_has_warnings": bool(inference_log),
    }
    # Completion marker is written last; raw output alone is not a finished job.
    (args.output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Saved {duration:.3f} seconds from offset {args.start:.3f} to {args.output}")


if __name__ == "__main__":
    main()
