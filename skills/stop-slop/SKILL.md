---
name: stop-slop
description: Review the assistant's own draft reply before sending it. Use when asked to remove AI boilerplate, make an assistant response sound natural, or make a reply understandable without decoding vague references or unexplained jargon.
---

# Stop Slop

Review your draft against the user's question and the relevant conversation. Reply in the user's language unless requested otherwise, and use the language required for any artifact.

- Start with what answers the question. Cut opening ceremony, inflated claims, invented objections, and endings that repeat what the reader just saw.
- Follow references from the reader's seat. If “these skills,” “the claims,” or “the next step” leaves the reader wondering which ones, recover the names, evidence, or action from the conversation. Explain an unfamiliar name or abbreviation briefly where it matters. Keep shared context implicit when the reader can already identify it.
- For a message to a colleague, write a message the sender could plausibly say to that person. Use the sender's perspective only when the facts support it. Group related facts naturally. Avoid turning each fact into a report heading.
- Preserve what happened, who did it, what is still uncertain, and what was proposed versus agreed. If a detail is unavailable, leave the uncertainty visible or ask if it changes the answer. Do not invent specifics to make the prose sound livelier.
- Keep ordinary technical subjects, meaningful repetition, useful lists, and punctuation that helps the reader. Leave good sentences alone. Return the revised reply without a score or a report on your edits unless requested.

## Examples

The draft “Потом займёмся защитой и проверим утверждения по источникам” needs context. If the conversation identifies lab defenses and report evidence, write: “Потом я бы попробовал помощника для подготовки к защите лабораторных. Ещё можно проверить, подтверждаются ли выводы отчёта расчётами, тестами или документами, на которые он ссылается.” If discussing Superpowers or TDD, explain the relevant practice in plain words, such as agreeing on a plan or writing a test before changing code.

When the sender ran 22 tests locally and plans one real scenario in the working environment, a message can read: “У меня локально все 22 теста прошли. В рабочем окружении ещё не проверял. Дальше прогоню там один реальный сценарий.”

## Editorial influences

These instructions and examples are original. The focus on filler and formulaic structures comes from the approach in Hardik Pandya's stop-slop. Compare [blader/humanizer](https://github.com/blader/humanizer) for paragraph-level patterns, [OzeroHAX/humanize-writing](https://github.com/OzeroHAX/humanize-writing) for preserving claims and voice, and [fockus/writing-clearly](https://github.com/fockus/writing-clearly) for writing from concrete information. The examples reflect user feedback on a blind comparison.
