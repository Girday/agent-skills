# Local Routes: Windows, Linux, macOS

## Choose an engine

| Environment | Engine | Computation |
|---|---|---|
| Windows, Linux, macOS with compatible wheels | `faster-whisper` (default) | CPU, int8 by default |
| Windows / Linux with compatible NVIDIA hardware and CUDA libraries | `faster-whisper --device cuda` | float16 by default; type can be set explicitly |
| macOS on Apple Silicon | `mlx` | Metal; separate MLX weight format |

Check architecture, Python, RAM, and package availability. NVIDIA hardware does not guarantee a working CUDA route: driver, CTranslate2, cuBLAS, and cuDNN versions must be compatible. Check [current faster-whisper requirements](https://github.com/SYSTRAN/faster-whisper#requirements); do not automatically install drivers for a sample. For unsupported GPUs, choose CPU or report the blocker. Do not use MLX on Windows/Linux; Intel Macs use the CPU route. An installed package does not prove GPU access from the agent environment.

## Environment

Isolate dependencies; do not modify system Python. Running the environment's Python by full path does not require activation.

Windows, PowerShell (inside the skill folder):

```powershell
py -m venv .venv-asr
.\.venv-asr\Scripts\python.exe -m pip install faster-whisper imageio-ffmpeg
.\.venv-asr\Scripts\python.exe scripts/transcribe_local.py recording.m4a probe --backend faster-whisper --model MODEL_PATH --start 120 --duration 90
.\.venv-asr\Scripts\python.exe scripts/export_transcript.py probe --output probe-export
```

Linux / macOS, shell:

```sh
python3 -m venv .venv-asr
.venv-asr/bin/python -m pip install faster-whisper imageio-ffmpeg
.venv-asr/bin/python scripts/transcribe_local.py recording.m4a probe --backend faster-whisper --model MODEL_PATH --start 120 --duration 90
.venv-asr/bin/python scripts/export_transcript.py probe --output probe-export
```

For NVIDIA, add `--device cuda` to recognition; specify a supported `--compute-type` if needed. CUDA failure does not switch the recording to cloud processing.

Additional Apple Silicon route:

```sh
.venv-asr/bin/python -m pip install mlx-whisper imageio-ffmpeg
.venv-asr/bin/python scripts/transcribe_local.py recording.m4a probe-mlx --backend mlx --model MLX_MODEL_PATH --duration 90
```

Engine models are **not interchangeable**. `MODEL_PATH` is a converted CTranslate2 model folder (containing `model.bin`) or its explicit Hugging Face repo ID; `MLX_MODEL_PATH` is a folder/ID in MLX Whisper format. For IDs, the script downloads a snapshot. The helper does not expand short names such as `small` into repo IDs: use the exact identifier from the selected model's documentation. Do not download a large model before checking dependencies and resources.

Models are downloaded separately from software. Store them locally for offline work. Set the cache with `HF_HOME`; prohibit network requests with `HF_HUB_OFFLINE=1`. In PowerShell: `$env:HF_HUB_OFFLINE = '1'`; in shell: `export HF_HUB_OFFLINE=1`. Local paths need no snapshot download. Do not search for or print secrets to enable execution.

## Sample and coverage

The `scripts/transcribe_local.py` helper neither installs dependencies nor sends recordings to a service. It decodes the selected interval with FFmpeg from imageio-ffmpeg into mono float32 / 16 kHz and calls the chosen engine. External FFmpeg provides consistent chunking and logging across both engines; faster-whisper itself can decode through PyAV.

The default duration of 90 seconds is a **sample**, not full coverage. `--duration 0` processes to the end; `--start` is the offset in seconds. Use the same environment Python for the full recording:

```sh
python scripts/transcribe_local.py recording.m4a full-run --backend faster-whisper --model MODEL_PATH --duration 0
python scripts/export_transcript.py full-run --output transcript-package
```

The default `--language auto` detects language; for a known language, specify its code, for example `--language ru`. Detection may fail on short samples. Transcribe the original language without hidden translation. Mono mixing does not verify channel quality: inspect original channels first.

The script decodes the entire selected interval into memory. Estimate RAM, disk, and speed on a sample; process large intervals in chunks. The output folder must be new. The manifest stores the source hash, configuration/weight hashes, library versions, and engine parameters. Python inference warnings are saved in `inference.log` and noted in the manifest; for numerical warnings, check results and library compatibility before a long run. Engine JSON is saved before export; faster-whisper returns a segment generator, which the script fully consumes and serializes from dataclass fields, including word timestamps. VAD is disabled in this route; the timeline is not compressed.

## Long recordings and resumption

Run nonoverlapping chunks with different `--start` / `--duration` values into separate folders. The exporter accepts folders in any order, checks source, model, language, library, and engine-parameter compatibility, reports gaps, and rejects overlaps over 1 ms. Boundary words can be cut: check against the source. If overlaps are needed, resolve duplicates separately; the exporter does not infer text alignment.

Incomplete ASR within a chunk does not automatically resume. Completed folders can be re-exported. On failure, inspect the log and choose a new folder for retry; do not blindly delete results. A folder without `manifest.json` is not considered complete.

Retain decoder warnings. Matching duration does not establish absence of internal defects. The exporter does not claim the source's end was reached: verify that separately against duration and the recording's ending.

## Output

Export creates `transcript.md`, `transcript.json`, `manifest.json`, `review.md`, `context-input.md`, and copies of raw ASR with manifests. Empty segments remain in raw JSON; all nonempty text transfers without semantic editing. Doubtful intervals are retained with flags. Absence of a flag does not mean correct text. The exporter requires neither MLX nor faster-whisper: Python's standard library suffices for saved JSON.
