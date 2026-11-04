# Procedure validation and limits

## Scope

Initial validation: 2026-11-04. This is an instruction-only skill with no required runtime. It has not been tested in an actual student lesson, instructor defense, or longitudinal learning study. No grade prediction or demonstrated learning-effectiveness claim is supported.

The examples are original synthetic fixtures. Course repositories and selected defense-history messages were inspected read-only to select realistic topics. No personal identifiers, student code, chat exports, or course documents are distributed in this skill.

## Reusable evaluation cases

For a future revision, give an evaluator the skill, the selected case, and only the raw artifacts needed. Request actual assistant responses rather than a checklist of intended behavior. Do not expose answer keys to an evaluator acting as a strict examiner until debrief. Use temporary files for persistence checks, not a student's submission directory.

| Case | Observable behavior to check |
|---|---|
| Task/code absent | Ask for essential sources, offer explicitly general explanations, invent no variant or file locators |
| Complete beginner asks for explanation | Begin with task, inputs, and expected result, then one small taught step; no required diagnostic answer |
| “I don't know” after explanation | Rephrase and work through a smaller example; offer supported application rather than repeat an entrance quiz |
| Experienced student requests strict mock immediately | Start one unassisted exam question, without forcing a beginner lesson or redundant consent |
| Guided misconception | Correct one concrete error, ask a small application question, then wait |
| Ready answer in guided mode | Supply a model when requested, record it as supplied, offer a later independent attempt |
| Ready answer in strict mock | Offer to end the round for explanation; disclose no answer while the choice is pending |
| Prior hinted answer, unknown delay | Establish elapsed time and ask unassisted; claim neither prior mastery nor delayed retention |
| Wrong stopping condition in code | Present exact evidence and effect; do not edit the lab under preparation authorization |
| Session close with agreed destination | Write concise evidence and help levels, preserve history, do not silently create tracked submission notes |
| Changed implementation | Refresh affected source locators and assumptions before reusing old explanations |

## Initial checks performed

A bounded independent agent pass produced four Russian response simulations: missing materials, a projection misconception, a ready-answer request during strict mock, and review with unknown elapsed time. The responses requested necessary sources, corrected the specific misconception with a small follow-up, withheld the strict-mode answer pending a mode choice, and avoided claiming delayed retention. No material procedural deviation was found in these four short samples; they do not cover a complete lesson.

The numerical example was executed: iteration 8 returns x = 1.9921875, bound = 0.0078125, and substitution residual magnitude = 0.00390625. A one-iteration limit raises rather than returning success. Transform arithmetic was checked for the stated column-vector convention: T*S maps the sample coordinate to 3; S*T maps it to 4. Graphics reasoning was independently reviewed, but the pseudocode was not compiled or rendered.

An additional isolated synthetic session-close check wrote a preparation note to its agreed temporary destination. It preserved the initial error and subsequent help, and did not claim independent mastery. A defective iteration x → x + 0.001 returned (0.001, 1) under a small-step test despite having no fixed point; the evaluator showed the contradiction and verified the source hash stayed unchanged. This was a scripted scenario, not an actual student exchange.

Catalog presence was checked once in the root README and each of ten translations. Metadata, local-link/privacy checks, the repository unittest suite, and Ruff lint/format passed. All 22 repository tests passed, including existing XeLaTeX integration tests. The skill-creator quick validator and diff whitespace check also passed. These checks cannot establish tutoring quality. No existing skill implementation was changed.

## Beginner-support revision

The initial optional-familiarity requirement replaces mandatory diagnostic answers. Guided learning explicitly starts with the lab task, input data, and expected output, then teaches notation, method, and actual code in small fragments. Numerical and graphics fixtures include beginner openings and worked help after “I don't know.” Mock defense requires a request or agreement; an explicit strict-mode request starts directly. A successful retelling alone does not trigger examination.

A new independent read-only pass produced actual Russian replies for three scenarios: a complete numerical beginner, a graphics learner still confused after an example, and an experienced student requesting strict examination immediately. The first two included another simulated “I don't know” turn. The numerical opening explained task, inputs, and outputs, worked 0 → 1, then helped with 1 → 1.5. The graphics replies isolated translation on a number line and reduced the next step after another difficulty. The strict reply asked one task question directly, without preliminary teaching or an extra consent request. No material contradiction was observed in these short openings; arithmetic was checked manually.

The revision passed the skill-creator quick validator, collection validation, all 22 repository tests, Ruff lint/format, and the diff whitespace check. The simulations did not test a full progression into actual code explanation, the point at which repeated confusion needs a different kind of clarification, or later independent recall. They provide procedural evidence only.

## Still to try with a student

- A complete guided lesson with actual student replies and code navigation.
- A full strict round and evidence-based debrief, including demonstrations.
- A later unassisted explanation and a transfer question after an established delay.
- Whether pace, explanation size, and note length suit the student over multiple sessions.
- Real course-document conflicts, missing assets, and changes between sessions.

Use observed failures to improve the narrow procedure involved. Do not replace student evidence with simulated replies, repeated wording checks, or large costly experiment batches.
