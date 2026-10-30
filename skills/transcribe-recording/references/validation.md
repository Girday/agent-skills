# Sources and Validation

## Basis for route selection

Primary sources (reviewed when preparing the route; recheck compatibility and access conditions during environment setup):

- [Faster-whisper](https://github.com/SYSTRAN/faster-whisper): portable CPU route, NVIDIA CUDA, segment generator, and word timestamps. Native Windows/Linux runs were not performed in this environment.
- [MLX Whisper](https://github.com/ml-explore/mlx-examples/tree/main/whisper): local Apple Silicon recognition, model selection, and API.
- [Whisper model card](https://github.com/openai/whisper/blob/main/model-card.md): limitations, invented and repeated phrases. These effects require checking actual audio.
- [Sherpa-ONNX speaker diarization](https://k2-fsa.github.io/sherpa/onnx/speaker-diarization/index.html) and [API example](https://github.com/k2-fsa/sherpa-onnx/blob/master/python-api-examples/offline-speaker-diarization.py): separate segmentation, voice-feature, and clustering stages.
- [WeSpeaker pretrained models](https://github.com/wenet-e2e/wespeaker/blob/master/docs/pretrained.md): alternative features and model conditions.
- [Pyannote community-1](https://huggingface.co/pyannote/speaker-diarization-community-1): local option with separate access conditions.

The helpers were written for this skill. Third-party implementations, models, and private recordings are not bundled. The repository license does not replace their licenses or terms.

## What was checked

An earlier practical run on an approximately 75-minute Russian technical recording confirmed ALAC decoding from M4A, local ASR with MLX Whisper small and large-v3-turbo, Sherpa-ONNX execution, and alternative WeSpeaker voice clustering. Turbo produced more readable sample text, without WER measurement or full listening review. Automatic diarization did not reliably separate known participants: fragmentation and excessive merging persisted. This run tested the approach and APIs, not every line of the new helpers. It does not establish universal model suitability.

The new helpers were tested separately: synthetic export inputs, absolute offsets, text and raw-byte preservation, gaps, and rejection of overlaps, invalid timestamps, and overwrites. An actual machine result tested the new exporter without publishing the source. The local runner was tested on a saved WAV sample with MLX Whisper large-v3-turbo, disabled networking, and previously downloaded weights. The new exporter preserved all 1078 nonempty segments of earlier full ASR and copied raw JSON byte for byte. The original M4A was no longer available at its former path. Full ASR was not repeated with the new helper.

Not validated as a ready universal route: reliable speaker separation in noisy classrooms, WER/CER/DER metrics, cloud processing, other operating systems and all video variants, audio review of the entire transcript, and end-to-end use of prepared context. The skill does not promise these outcomes without validation.

## Behavioral scenarios for further validation

1. User chooses local mode; model is unavailable: do not transmit the recording to a service; name the blocker and completed stages.
2. Six participants are known; the model returns 114 clusters or one: do not declare a participant count or force the result; inspect dialogues and report status separately from ASR.
3. A phrase contains an unclear negation or deadline: preserve uncertainty and a locator; do not create a confident context requirement.
4. Audio was not heard: distinguish structural checks from content review.
5. Long recording split into chunks: retain offsets, detect gaps and duplicates, and do not conflate local speaker IDs.

These scenarios are a behavioral validation plan, not a claim that an independent agent has already passed them.

## Broader purpose

The skill applies to meetings, talks, interviews, classes, and other speech recordings. Checking purpose should change information selection, not raw transcript content: proposals do not become decisions, discussing a deadline does not establish a commitment, and questions are not statements. Classroom trial observations remain a specific experiment and do not establish quality for all recording types.

## Portable helper validation

A short Mac CPU sample with faster-whisper, CTranslate2, and the tiny model passed decoding, feature computation, inference, and generator serialization with word timestamps. This environment produced RuntimeWarning messages during mel-feature computation; machine text was inaccurate. This is an execution-path smoke check, not quality validation. The helper retains Python warnings in inference.log, and the exporter carries that log into the package. The sample does not justify relying on tiny for technical speech accuracy.

Tests separately check CPU settings for Windows/Linux/macOS, MLX rejection on unsupported hosts, and transfer of word timestamps from the generator. They model environment selection and the adapter contract; they **are not native Windows/Linux or CUDA runs**. Those runs remain unperformed; the previously tested MLX route remains a separate option.
