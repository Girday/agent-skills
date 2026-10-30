# Speaker Checks

Choose available local diarization, such as Sherpa-ONNX or pyannote. Separately check model access conditions and licenses. Pyannote community-1 may require terms acceptance and a token; do not bypass access or ask for secrets in chat. Do not upload recordings to the cloud as a hidden fallback.

Before processing the full recording, test an excerpt with real dialogue, short utterances, and quiet participants. A single-voice sample checks execution, not speaker discrimination. If listening review is unavailable, that is a significant validation limit.

Preserve raw intervals, embeddings when available, and clustering parameters. Check:

- whether one person splits into multiple clusters as microphone distance changes;
- whether different people merge, particularly when features of long utterances are averaged;
- whether short utterances and overlapping speech are retained;
- whether the same person keeps a label at the beginning and end;
- whether some “people” are noise or subsecond fragments.

A known participant count is useful as a model parameter and check. Matching cluster count alone does not prove separation. Do not tune a threshold merely to obtain the desired count. User-confirmed voice samples help verify mappings; keep names and roles in a separate evidence-backed table. A voice's absence from labels does not prove the person was silent.

Do not join independent `SPEAKER_00` labels across chunks without global matching. Align ASR and diarization with word timestamps, retaining multiple candidates during overlap and `UNKNOWN` when alignment is insufficient. Do not assign a long segment to one person if the voice changes within it. Keep automatic alignment separate from manual review.

If the available pipeline cannot separate people, continue useful ASR export with `UNKNOWN`. Report failed methods, reviewed coverage, and the next experiment that distinguishes hypotheses. Do not rerun an entire many-hour recording for each threshold when a sample can test the hypothesis. This skill's exporter intentionally does not accept unverified diarization labels; after successful review, augment a working transcript copy while preserving the raw package.
