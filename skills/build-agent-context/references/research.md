# Rationale and Sources

Reviewed: October 28, 2026. This is a targeted review of 12 primary publications and original author analyses, not an exhaustive literature list or popularity ranking. Selection covers working context organization, retrieval, compression, state handoff, and outcome validation. Source texts, code, and illustrations are not distributed; the following is an original brief synthesis with attribution. Third-party publications retain their authors' rights.

## Decision map

| Skill decision | Basis | Transfer limitation |
|---|---|---|
| Short entrypoint with details loaded as needed | S01, S02, S03 | One file may suffice for a small request |
| Separate knowledge, requirements, and current state | S02, S04, S05 | No particular SDK or memory store is required |
| Preserve sources and significant failed attempts | S03, S05 | Full logs need not occupy the working context |
| Explicit conflicts and rechecking compressed text | S04, S06, S07 | Compression may distort source information |
| Preserve individual passage context | S08 | Does not require embeddings or a vector database |
| Budgeting and checking retrieval of important information | S09, S10 | No universal token threshold across models |
| Evidence-backed readiness and next-step handoff | S05, S12 | Programming experience does not fully transfer to other domains |
| Validate outcomes on realistic tasks | S11, S12 | One run does not measure stability or efficiency gains |

## Publications

### S01. Anthropic — Effective context engineering for AI agents

[Publication, 2025](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents).

The authors discuss limited attention, selection of meaningful information, retrieval through lightweight pointers, and progressive loading. For long tasks, they describe compaction and structured notes.

Application: short entrypoints, explicit reading routes, and preservation of important conditions during compression. These are engineering recommendations, not a single prescribed context format.

### S02. LangChain — Context Engineering

[Publication, July 2, 2025](https://www.langchain.com/blog/context-engineering-for-agents).

The analysis groups approaches into writing, selecting, compressing, and isolating context. It separately considers instructions, knowledge, and tool results.

Application: choose a layer for each information type and select for the current step. Topic isolation is useful, but creating an agent team is not mandatory for context preparation.

### S03. Manus — Context Engineering for AI Agents: Lessons from Building Manus

[Yichao Ji, July 18, 2025](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus).

The author describes the filesystem as external storage, recoverable compression with paths/URLs retained, goal retention, and learning from errors for later decisions. Caching and tool management are also discussed.

Application: retain original access and briefly describe significant failures. KV-cache and tool-masking advice concerns runtime implementation; a Markdown package does not provide those mechanisms itself.

### S04. OpenAI — Context Engineering: Short-Term Memory Management with Sessions

[Emre Okcular, September 9, 2025](https://developers.openai.com/cookbook/examples/agents_sdk/session_memory).

The guide compares trimming recent history with summarizing older history. Trimming loses distant information; summarization retains it compactly but may introduce and reinforce errors.

Application: retain constraints, identifiers, and decisions separately from conversation history; recheck compressed state. SDK code, model parameters, and example window sizes are not requirements of this skill.

### S05. Anthropic — Effective harnesses for long-running agents

[Publication, 2025](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents).

The article examines state loss between sessions and premature completion claims. Its example uses feature descriptions, progress notes, and behavioral checks.

Application: record completed work, verification results, and continuation. Commits, startup scripts, and rigid feature-list structure belong to the demonstration environment; context preparation does not authorize automatically creating or running them.

### S06. Drew Breunig — How Long Contexts Fail

[Author analysis, June 22, 2025](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html).

The author identifies persistence of erroneous information, distraction, influence of extraneous information, and context conflicts.

Application: explicit claim statuses, exclusion of unrelated data, and preserved disagreements. This is a useful taxonomy discussing other research, not independent evidence for universal numerical thresholds.

### S07. Drew Breunig — How to Fix Your Context

[Author analysis, June 26, 2025](https://www.dbreunig.com/2025/06/26/how-to-fix-your-context.html).

Describes knowledge and tool selection, task isolation, pruning, summarization, and external storage.

Application: choose minimally sufficient organization. Numerical results from cited individual studies and tool-set sizes should not become general rules for all agents.

### S08. Anthropic — Introducing Contextual Retrieval

[Publication, September 19, 2024](https://www.anthropic.com/research/contextual-retrieval).

An isolated document passage may lose information about the subject, period, and meaning of a metric. The publication proposes adding explanatory context to chunks before retrieval, combining retrieval methods, and evaluating results.

Application: retain subject, period, definitions, and units alongside extracted facts. Experimental percentage improvements do not predict the effectiveness of an arbitrary file package.

### S09. Liu et al. — Lost in the Middle: How Language Models Use Long Contexts

[Research, arXiv:2307.03172, 2023](https://arxiv.org/abs/2307.03172).

Multi-document question-answering and value-retrieval experiments show dependence on where relevant information occurs; tested models often retrieved it less effectively from the middle of the input.

Application: do not hide key conditions; check retrieval from the final package. Results on the paper's models and tasks do not establish the same effect size for current models or every agent scenario.

### S10. Chroma — Context Rot: How Increasing Input Tokens Impacts LLM Performance

[Kelly Hong, Anton Troynikov, Jeff Huber, July 14, 2025](https://www.trychroma.com/research/context-rot).

The report studies quality changes with longer inputs, distractors, and varying similarity between the question and target passage. The authors study 18 models; the participating set differs between experiments.

Application: conserve working context and test actual recipient questions rather than keyword matching alone. Synthetic trials do not establish one safe size for all models.

### S11. Google — Architecting efficient context-aware multi-agent framework for production

[Hangfei Lin, December 4, 2025](https://developers.googleblog.com/architecting-efficient-context-aware-multi-agent-framework-for-production/).

The publication separates current model input, session, long-term information, and artifacts. Working context is treated as a view assembled from stored state.

Application: separate storage from loading and source versions from concise views. ADK architecture is an example; the skill does not require installing it or promise session management through Markdown.

### S12. Anthropic — Demystifying evals for AI agents

[Publication, January 9, 2026](https://www.anthropic.com/research/demystifying-evals-for-ai-agents).

The article distinguishes claimed responses from actual environment outcomes, recommending realistic tasks, inspection of actions, and accounting for nondeterminism.

Application: check that work can continue, trace facts to sources, and describe trial limits honestly. This skill's criteria are an original adaptation; the publication does not certify generated packages.

## Reconciling recommendations

- **More or less information:** include enough for correct action, then check which details are actually needed. Window capacity is not a target size.
- **Summarize or preserve errors:** keep the verified conclusion and significant failure cause in current state; keep full raw results available separately. Erroneous hypotheses must remain labeled.
- **Examples or freedom:** add examples when they resolve real ambiguity; do not fill context with a long list of special cases.
- **Files or RAG:** start with a recipient-accessible format and simple search. Consider more complex systems for measurable retrieval problems and a corresponding user task.

Source catalogs, coverage statuses, file patterns, and review rubrics are design choices of this skill. They synthesize the reviewed material and context-preparation experience; they are not an official company standard. Update guidance after observed failures or changed environment capabilities, without adding prohibitions merely to increase length.
