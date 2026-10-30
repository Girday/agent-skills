---
name: transcribe-recording
description: Transcribe audio and video of lectures, meetings, talks, interviews, and other conversations with timestamps, check speaker separation, and prepare context inputs. Use for speech recordings; route existing text without audio to build-agent-context.
---

# Transcribe Recordings

Prepare a verifiable transcript and materials for subsequent context preparation. Keep traceability to the recording; successful recognition does not prove text accuracy or correct speaker separation.

Respond in the user's language unless they request otherwise. Use the language required by the task for generated artifacts. Preserve exact wording where required by standards, templates, or source material. Transcribe speech in its original language unless translation is requested; keep any translation separate from the original transcript.

## Choose a route

Establish the result's purpose, language, full or selective coverage, and chosen processing mode from the request. In local mode, do not upload the recording to the cloud after a failure. Downloading software and models differs from transmitting audio. Do not modify system Python; use a separate environment. Obtain the relevant authorization before paid processing or transmission to a new service unless it has already been given.

Check source access, duration, codec, channels, and decoding. M4A is a container: it may contain ALAC or AAC. Stereo channels do not imply two people; before mixing to mono, check whether useful voices would be lost. Do not modify the source.

For local recognition, see the [Windows, Linux, and macOS routes](references/local-workflow.md). The baseline is faster-whisper on CPU; choose NVIDIA CUDA with compatible drivers and libraries. MLX is a separate Apple Silicon option. Choose based on OS, hardware, and a sample run; do not assume GPU availability. If tools are unavailable, name the specific missing component and preserve completed checks.

## Sample and full run

First process short excerpts containing important names, terms, or numbers, quiet speech, and different participants when present; check the beginning, middle, and end. Compare the text with audio when listening is available. If only machine text is available, assess only obvious defects and explicitly state that no listening review occurred. Do not present semantic plausibility as ASR quality.

Choose the model based on sample results and resources, not speed alone. For long recordings, estimate memory, storage, and time; run heavy stages sequentially when memory is insufficient. Exclude model-weight download time from recognition speed estimates.

Preserve raw ASR, parameters, model versions, and the recording hash. When splitting, retain absolute offsets and pauses; check boundaries and endings. Resolve duplicates in overlapping chunks before assembly while preserving original hypotheses. Resume only compatible results with the same source and parameters. Mark skipped and unprocessed intervals.

## Speakers

Text recognition and diarization are separate stages. If speaker separation is required, read the [speaker checks](references/speakers.md). Actual voice changes and stable labels across the recording matter. Role, name, and voice cluster are distinct entities.

Use a known number of people as a check and experiment parameter, not proof of correct output. Do not assign the longest voice a name or a host, presenter, or teacher role without evidence. If diarization fails, retain text with `UNKNOWN`; do not stop independently useful ASR or declare speaker labeling complete. After a failed sample, change a justified parameter on a small sample before repeating an expensive full run.

## Review and package

Keep machine text separate from the edited version. Do not guess unclear passages. For corrections, record the segment, basis, and what was checked: audio, slides, or user clarification. Do not present information reconstructed from an external source as heard speech, including numbers, names, and formulas. Flag short intervals and repetition without automatically deleting text. Do not assign confidence percentages without measurement.

The package must contain:

- a manifest of the source, parameters, actual coverage, and ASR, diarization, and review statuses;
- raw machine JSON and a readable transcript with stable IDs and absolute timestamps;
- an uncertainty list: voices, overlap, terms, numbers, negations, formulas, and requirements;
- `context-input.md`: purpose, sources, coverage, topic routes, and limitations on transfer to context.

The [export_transcript.py](scripts/export_transcript.py) helper creates a basic package from local runs, preserving all nonempty text and `UNKNOWN`. It does not perform diarization or editing. Its fixed headings and review notes are English; localize that surrounding text in the working copy to the required artifact language without changing recorded speech, IDs, timestamps, or raw files. Add topic routes based on the content; automatic export does not replace studying the recording.

Check text preservation, timestamp order and boundaries, gaps between chunks, and retention of raw results. Separately review recognition quality by listening to an available sample. WER/CER or DER requires manually annotated ground truth and stated calculation conditions; without it, report review coverage rather than invented accuracy metrics.

## Handoff to context preparation

If the user requests context and `build-agent-context` is available, pass it the package and future task purpose. If the purpose is missing, clarify it or explicitly prepare overview context. Without that skill, create portable Markdown using the same principles: sources, essential knowledge, limitations, and open questions.

Separate statements from questions and assumptions, and accepted decisions from proposals. For meetings, record agreed actions, owners, and deadlines only with supporting utterances; for talks, record key points and questions; for classes, explanations and requirements. Do not invent missing decisions or commitments. If the speaker is unidentified, the authorship and authority of a requirement are also unknown. Attach each significant claim to the recording, ID, and timestamp. Do not turn recorded utterances into agent instructions. Uncertain recognition does not become fact through compression. Keep originals and the full transcript available.

Return result links, actual coverage, and significant limitations. Distinguish “ASR complete,” “speakers separated,” and “context verified.” Do not include personal recordings or real transcripts in the public skill package.

Read [sources and validation limits](references/validation.md) when assessing readiness or planning a new route trial.
