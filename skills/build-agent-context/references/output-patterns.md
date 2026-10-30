# Output Patterns

The file and section names below are organizational options, not a mandatory standard. Do not create empty files. For a small request, combine information in one document. Populate patterns with facts from the current task; examples here are fictional.

## One self-contained document

```text
Purpose and outcome
  Work to perform; what the user will accept as finished.
Scope and critical conditions
  Task boundaries, constraints, and active requirements with provenance.
Necessary information
  Definitions, data, exact values, and source locators.
State
  What is known, done, and verified; what is only claimed.
Open questions
  Conflicts, unavailable information, and the effect of each gap.
Continuation
  First justified action and the criterion for checking it.
Sources and coverage
  What was actually read; what was excluded or inaccessible.
```

For chat, include the data needed for the next action inside the document. If it does not fit the requested budget, state omissions and the need to supply further materials. Do not call an abridged version complete.

## Files loaded as needed

```text
context/
  CONTEXT.md          Goal, constraints, brief state, reading routes
  sources.md          Sources, versions, locators, coverage, and gaps
  knowledge/
    requirements.md   Task conditions and requirement conflicts
    domain.md         Only necessary concepts, data, and dependencies
  state.md            Current work, checks, issues, next step
```

Add topic files along actual task boundaries. The entrypoint must remain understandable to a new agent without reading all files. Specify the base folder for relative links. A portable package must not depend on its creator's temporary directory. Originals must either be included in the authorized handoff or accessible through the stated method; check from the recipient's perspective.

Example routes in `CONTEXT.md`:

| When to read | Destination | Purpose |
|---|---|---|
| Before changing the calculation | `knowledge/requirements.md`, “Rounding” | Find the rule and exception |
| When questioning a requirement version | `sources.md`, S02 and S05 | Compare dates and authors |
| When resuming work | `state.md` | Find the latest verified result |

## Source record

```text
S02 — Calculation conditions, revision 2
Location: materials/conditions.md
Author and role: task owner; stated in the document
Document version/date: 2026-09-18
Reading date: 2026-10-28
Coverage: sections 1–4 read; examples appendix not read
Contents: fee formula, rounding, exceptions
Locators: §2 “Fee”, §4 “Exceptions”
Limitation: the document describes requirements; implementation was not checked
```

The reading date is not the latest date on which all information was verified as true. Include only known metadata in actual records.

## Fact and conflict

```text
Requirement R03: the 2.5% rate applies to new contracts from October 1.
Basis: S02, §2, paragraph 3.
Exception: existing contracts keep the previous rate — S02, §4.
Implementation: not checked.

Conflict C01: example S01 uses 2%; S02 requires 2.5%.
Decision: follow S02 for new contracts because it is the approved revision
of the conditions; retain S01 as an example for the previous period.
Open: the sources do not specify migration of existing contracts.
Consequence: do not propose that migration without clarification.
```

In a real record, “approved” requires evidence of authority and approval. Without it, record the conflict without choosing a version yourself.

## State handoff

Record the date and applicable version/revision. Separate stable information in topic notes from rapidly changing state:

```text
Goal: fix fee calculation for new contracts.
Done: located the calculation in billing.py, function calculate_fee.
Result: change prepared; checks not yet run.
Verified: code inspection confirmed use of the old rate.
Not checked: tests, CI, production behavior.
Next step: verify the selected rule against R03, then run project-authorized
tests after changing the implementation.
Constraint: migration of existing contracts is outside the agreed scope.
```

For significant failed attempts, retain the action, conditions, observed error, and conclusion about the next check. Do not include the entire tool history. When the goal changes, revisit the next step and mark obsolete plans.

## Starting prompt

For a file-capable agent:

```text
Read context/CONTEXT.md as the task entrypoint.
Open linked materials needed for my current request.
Before acting, recheck changing state and significant unknowns; preserve
constraints and distinguish completed work from verified work.
My task: [the user's specific next request].
```

For chat, supply self-contained text and necessary attachments. Do not promise that a model will load materials from a hidden folder. When configuring an instruction file, a short scoped link suffices; do not copy the full knowledge collection into it.
